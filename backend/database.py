import os
import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2 import pool
from typing import Optional, Dict, List
from datetime import datetime
import redis
import json
from functools import lru_cache

class Database:
    def __init__(self):
        self.database_url = os.getenv("DATABASE_URL")
        self.redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
        
        # Create connection pool for better performance
        self.connection_pool = psycopg2.pool.ThreadedConnectionPool(
            minconn=1,
            maxconn=10,
            dsn=self.database_url
        )
        
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
            print("Redis not available, caching disabled")
            self.redis_client = None
            self.cache_enabled = False
    
    def get_connection(self):
        """Get connection from pool"""
        return self.connection_pool.getconn()
    
    def return_connection(self, conn):
        """Return connection to pool"""
        self.connection_pool.putconn(conn)
    
    def init_db(self):
        """Initialize database tables with indexes"""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            
            # Users table with indexes
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    email VARCHAR(255) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                
                -- Create indexes for performance
                CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
                CREATE INDEX IF NOT EXISTS idx_users_created_at ON users(created_at);
            """)
            
            # Conversations table with indexes
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS conversations (
                    id SERIAL PRIMARY KEY,
                    session_id VARCHAR(255) NOT NULL,
                    role VARCHAR(50) NOT NULL,
                    content TEXT NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                
                -- Create indexes for performance
                CREATE INDEX IF NOT EXISTS idx_conversations_session_id ON conversations(session_id);
                CREATE INDEX IF NOT EXISTS idx_conversations_timestamp ON conversations(timestamp);
                CREATE INDEX IF NOT EXISTS idx_conversations_session_timestamp ON conversations(session_id, timestamp DESC);
            """)
            
            conn.commit()
            print("✅ Database initialized with indexes")
        except Exception as e:
            conn.rollback()
            print(f"❌ Database initialization error: {e}")
        finally:
            cursor.close()
            self.return_connection(conn)
    
    def _get_cache(self, key: str) -> Optional[Dict]:
        """Get data from cache"""
        if not self.cache_enabled:
            return None
        try:
            cached = self.redis_client.get(key)
            if cached:
                return json.loads(cached)
        except:
            pass
        return None
    
    def _set_cache(self, key: str, value: Dict, ttl: int = 300):
        """Set data in cache with TTL (default 5 minutes)"""
        if not self.cache_enabled:
            return
        try:
            self.redis_client.setex(key, ttl, json.dumps(value))
        except:
            pass
    
    def _invalidate_cache(self, pattern: str):
        """Invalidate cache by pattern"""
        if not self.cache_enabled:
            return
        try:
            keys = self.redis_client.keys(pattern)
            if keys:
                self.redis_client.delete(*keys)
        except:
            pass
    
    def create_user(self, name: str, email: str, password: str) -> int:
        """Create a new user"""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (name, email, password) VALUES (%s, %s, %s) RETURNING id",
                (name, email, password)
            )
            user_id = cursor.fetchone()[0]
            conn.commit()
            
            # Invalidate email cache
            self._invalidate_cache(f"user:email:{email}")
            
            return user_id
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            self.return_connection(conn)
    
    def get_user_by_email(self, email: str) -> Optional[Dict]:
        """Get user by email with caching"""
        # Check cache first
        cache_key = f"user:email:{email}"
        cached_user = self._get_cache(cache_key)
        if cached_user:
            return cached_user
        
        conn = self.get_connection()
        try:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            row = cursor.fetchone()
            
            if row:
                user_dict = dict(row)
                # Cache for 10 minutes
                self._set_cache(cache_key, user_dict, ttl=600)
                return user_dict
            return None
        finally:
            cursor.close()
            self.return_connection(conn)
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict]:
        """Get user by ID with caching"""
        # Check cache first
        cache_key = f"user:id:{user_id}"
        cached_user = self._get_cache(cache_key)
        if cached_user:
            return cached_user
        
        conn = self.get_connection()
        try:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
            row = cursor.fetchone()
            
            if row:
                user_dict = dict(row)
                # Cache for 10 minutes
                self._set_cache(cache_key, user_dict, ttl=600)
                return user_dict
            return None
        finally:
            cursor.close()
            self.return_connection(conn)
    
    def __del__(self):
        """Clean up connection pool"""
        try:
            self.connection_pool.closeall()
        except:
            pass
