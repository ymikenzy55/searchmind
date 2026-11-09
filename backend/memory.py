import os
import json
import sqlite3
from datetime import datetime
from typing import List, Dict

class ConversationMemory:
    """Persistent conversation memory using SQLite"""
    
    def __init__(self, db_path="conversation_history.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the database and create tables if they don't exist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                session_id TEXT DEFAULT 'default'
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_message(self, role: str, content: str, session_id: str = "default"):
        """Add a message to the conversation history"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        timestamp = datetime.now().isoformat()
        cursor.execute(
            "INSERT INTO conversations (timestamp, role, content, session_id) VALUES (?, ?, ?, ?)",
            (timestamp, role, content, session_id)
        )
        
        conn.commit()
        conn.close()
    
    def get_conversation_history(self, session_id: str = "default", limit: int = 50) -> List[Dict]:
        """Retrieve conversation history"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT timestamp, role, content FROM conversations WHERE session_id = ? ORDER BY id DESC LIMIT ?",
            (session_id, limit)
        )
        
        messages = [
            {"timestamp": row[0], "role": row[1], "content": row[2]}
            for row in cursor.fetchall()
        ]
        
        conn.close()
        return list(reversed(messages))  # Return in chronological order
    
    def get_recent_context(self, session_id: str = "default", num_messages: int = 10) -> str:
        """Get recent conversation as context string"""
        messages = self.get_conversation_history(session_id, num_messages)
        
        context = ""
        for msg in messages:
            role = "User" if msg["role"] == "user" else "Assistant"
            context += f"{role}: {msg['content']}\n"
        
        return context
    
    def clear_history(self, session_id: str = "default"):
        """Clear conversation history for a session"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM conversations WHERE session_id = ?", (session_id,))
        
        conn.commit()
        conn.close()
    
    def get_all_messages_count(self, session_id: str = "default") -> int:
        """Get total message count"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM conversations WHERE session_id = ?", (session_id,))
        count = cursor.fetchone()[0]
        
        conn.close()
        return count
