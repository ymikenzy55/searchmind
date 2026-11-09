import os
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
from typing import List, Dict
import redis
import json

class ConversationMemory:
    def __init__(self):
        self.database_url = os.getenv("DATABASE_URL")
        self.redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
        
        # Initialize Redis for caching
        try:
            self.redis_client = redis.from_url(
                self.redis_url,
                decode_responses=True,
                socket_connect_timeout=2
            )
            self.redis_client.ping()
            self.cache_enabled = True
        except:
            print("Redis not available for memory, caching disabled")
            self.redis_client = None
            self.cache_enabled = False
    
    def get_connection(self):
        """Get database connection"""
        return psycopg2.connect(self.database_url)
    
    def add_message(self, role: str, content: str, session_id: str = "default"):
        """Add message to conversation history"""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO conversations (session_id, role, content) VALUES (%s, %s, %s)",
                (session_id, role, content)
            )
            conn.commit()
            
            # Invalidate cache for this session
            if self.cache_enabled:
                try:
                    self.redis_client.delete(f"history:{session_id}")
                except:
                    pass
        finally:
            cursor.close()
            conn.close()
    
    def get_conversation_history(self, session_id: str = "default", limit: int = 50) -> List[Dict]:
        """Get conversation history with caching"""
        # Check cache first
        cache_key = f"history:{session_id}:{limit}"
        if self.cache_enabled:
            try:
                cached = self.redis_client.get(cache_key)
                if cached:
                    return json.loads(cached)
            except:
                pass
        
        conn = self.get_connection()
        try:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute(
                """SELECT role, content, timestamp 
                   FROM conversations 
                   WHERE session_id = %s 
                   ORDER BY timestamp ASC 
                   LIMIT %s""",
                (session_id, limit)
            )
            rows = cursor.fetchall()
            history = [dict(row) for row in rows]
            
            # Cache for 2 minutes
            if self.cache_enabled and history:
                try:
                    self.redis_client.setex(cache_key, 120, json.dumps(history, default=str))
                except:
                    pass
            
            return history
        finally:
            cursor.close()
            conn.close()
    
    def get_recent_context(self, session_id: str = "default", num_messages: int = 6) -> str:
        """Get recent messages as context string with caching"""
        cache_key = f"context:{session_id}:{num_messages}"
        if self.cache_enabled:
            try:
                cached = self.redis_client.get(cache_key)
                if cached:
                    return cached
            except:
                pass
        
        conn = self.get_connection()
        try:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute(
                """SELECT role, content 
                   FROM conversations 
                   WHERE session_id = %s 
                   ORDER BY timestamp DESC 
                   LIMIT %s""",
                (session_id, num_messages)
            )
            rows = cursor.fetchall()
            
            # Reverse to get chronological order
            context_parts = []
            for row in reversed(rows):
                context_parts.append(f"{row['role']}: {row['content']}")
            
            context = "\n".join(context_parts)
            
            # Cache for 1 minute
            if self.cache_enabled and context:
                try:
                    self.redis_client.setex(cache_key, 60, context)
                except:
                    pass
            
            return context
        finally:
            cursor.close()
            conn.close()
    
    def clear_history(self, session_id: str = "default"):
        """Clear conversation history"""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM conversations WHERE session_id = %s", (session_id,))
            conn.commit()
            
            # Invalidate cache
            if self.cache_enabled:
                try:
                    self.redis_client.delete(f"history:{session_id}*")
                    self.redis_client.delete(f"context:{session_id}*")
                except:
                    pass
        finally:
            cursor.close()
            conn.close()
    
    def get_all_messages_count(self, session_id: str = "default") -> int:
        """Get total message count"""
        cache_key = f"count:{session_id}"
        if self.cache_enabled:
            try:
                cached = self.redis_client.get(cache_key)
                if cached:
                    return int(cached)
            except:
                pass
        
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM conversations WHERE session_id = %s", (session_id,))
            count = cursor.fetchone()[0]
            
            # Cache for 1 minute
            if self.cache_enabled:
                try:
                    self.redis_client.setex(cache_key, 60, str(count))
                except:
                    pass
            
            return count
        finally:
            cursor.close()
            conn.close()
    
    def get_user_sessions(self, user_id: str) -> List[str]:
        """Get all session IDs for a user"""
        cache_key = f"sessions:{user_id}"
        if self.cache_enabled:
            try:
                cached = self.redis_client.get(cache_key)
                if cached:
                    return json.loads(cached)
            except:
                pass
        
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """SELECT DISTINCT session_id 
                   FROM conversations 
                   WHERE session_id LIKE %s 
                   ORDER BY MAX(timestamp) DESC""",
                (f"{user_id}_%",)
            )
            rows = cursor.fetchall()
            sessions = [row[0] for row in rows]
            
            # Cache for 5 minutes
            if self.cache_enabled and sessions:
                try:
                    self.redis_client.setex(cache_key, 300, json.dumps(sessions))
                except:
                    pass
            
            return sessions
        finally:
            cursor.close()
            conn.close()
