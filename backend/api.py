from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import jwt
from passlib.context import CryptContext

try:
    # Try relative imports first (when run as module)
    from backend.agent import create_agent, query_agent
    from backend.memory import ConversationMemory
    from backend.database import Database
except ImportError:
    # Fall back to direct imports (when run directly)
    from agent import create_agent, query_agent
    from memory import ConversationMemory
    from database import Database

load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="SearchMind API",
    description="AI Research Assistant with persistent memory",
    version="2.0.0"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://*.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-this-in-production")
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Initialize services
print("Initializing services...")
try:
    memory = ConversationMemory()
    db = Database()
    agent_instance = None
    print("✅ Services initialized")
except Exception as e:
    print(f"❌ Service initialization error: {e}")
    raise

# Pydantic Models
class UserRegister(BaseModel):
    name: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class QueryRequest(BaseModel):
    message: str
    session_id: Optional[str] = "default"

class MessageResponse(BaseModel):
    role: str
    content: str
    timestamp: str

class ChatResponse(BaseModel):
    response: str
    session_id: str

# Helper Functions
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=7)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Routes
@app.on_event("startup")
async def startup_event():
    global agent_instance
    print("Starting up...")
    try:
        agent_instance = create_agent()
        db.init_db()
        print("✅ Startup complete")
    except Exception as e:
        print(f"❌ Startup error: {e}")

@app.get("/")
async def root():
    return {
        "message": "SearchMind API is running",
        "version": "2.0.0",
        "status": "active"
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.post("/api/auth/register")
async def register(user: UserRegister):
    try:
        print(f"Register attempt: {user.email}")
        # Check if user exists
        existing_user = db.get_user_by_email(user.email)
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Hash password (truncate to 72 bytes for bcrypt)
        password_truncated = user.password.encode('utf-8')[:72].decode('utf-8', errors='ignore')
        hashed_password = pwd_context.hash(password_truncated)
        
        # Create user
        user_id = db.create_user(user.name, user.email, hashed_password)
        print(f"✅ User created: {user_id}")
        
        # Create token
        token = create_access_token({"user_id": user_id, "email": user.email, "name": user.name})
        
        return {
            "token": token,
            "user": {
                "id": user_id,
                "name": user.name,
                "email": user.email
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Register error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/auth/login")
async def login(user: UserLogin):
    try:
        print(f"Login attempt: {user.email}")
        # Get user
        db_user = db.get_user_by_email(user.email)
        if not db_user:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        # Verify password (truncate to 72 bytes for bcrypt)
        password_truncated = user.password.encode('utf-8')[:72].decode('utf-8', errors='ignore')
        if not pwd_context.verify(password_truncated, db_user["password"]):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        # Create token
        token = create_access_token({
            "user_id": db_user["id"],
            "email": db_user["email"],
            "name": db_user["name"]
        })
        
        print(f"✅ Login successful: {user.email}")
        return {
            "token": token,
            "user": {
                "id": db_user["id"],
                "name": db_user["name"],
                "email": db_user["email"]
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Login error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/auth/me")
async def get_current_user(token: str):
    payload = verify_token(token)
    return {
        "user": {
            "id": payload.get("user_id"),
            "name": payload.get("name"),
            "email": payload.get("email")
        }
    }

@app.post("/api/chat/query", response_model=ChatResponse)
async def chat_query(request: QueryRequest, token: Optional[str] = None):
    try:
        # Verify user if token provided
        user_id = "guest"
        if token:
            payload = verify_token(token)
            user_id = payload.get("user_id")
        
        # Create session ID based on user
        session_id = f"{user_id}_{request.session_id}"
        
        # Query agent
        response = query_agent(agent_instance, request.message, session_id)
        
        return {
            "response": response,
            "session_id": request.session_id
        }
    except Exception as e:
        print(f"❌ Chat error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/chat/history")
async def get_history(session_id: str = "default", token: Optional[str] = None):
    try:
        # Verify user if token provided
        user_id = "guest"
        if token:
            payload = verify_token(token)
            user_id = payload.get("user_id")
        
        full_session_id = f"{user_id}_{session_id}"
        history = memory.get_conversation_history(full_session_id, limit=50)
        
        return history
    except Exception as e:
        print(f"❌ History error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/chat/history")
async def clear_history(session_id: str = "default", token: Optional[str] = None):
    try:
        user_id = "guest"
        if token:
            payload = verify_token(token)
            user_id = payload.get("user_id")
        
        full_session_id = f"{user_id}_{session_id}"
        memory.clear_history(full_session_id)
        
        return {"message": "History cleared successfully"}
    except Exception as e:
        print(f"❌ Clear history error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting SearchMind API...")
    uvicorn.run(app, host="0.0.0.0", port=8001)
