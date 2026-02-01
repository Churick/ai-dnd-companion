from pydantic import BaseModel, EmailStr, constr
from datetime import datetime
from typing import Optional, Dict, Any

# ----- User Schemas -----
class UserBase(BaseModel):
    email: EmailStr
    username: constr(min_length=3, max_length=50)

class UserCreate(UserBase):
    password: constr(min_length=6)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(UserBase):
    id: int
    credits: int
    subscription_tier: str
    created_at: datetime
    
    class Config:
        from_attributes = True  # Ранее orm_mode = True

# ----- Game Session Schemas -----
class GameSessionBase(BaseModel):
    title: Optional[str] = "Новое приключение"
    character_data: Optional[Dict[str, Any]] = {}
    world_context: Optional[str] = ""

class GameSessionCreate(GameSessionBase):
    pass

class GameSessionResponse(GameSessionBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# ----- Message Schemas -----
class MessageBase(BaseModel):
    content: str
    role: str  # 'user', 'assistant', 'system'

class MessageCreate(MessageBase):
    pass

class MessageResponse(MessageBase):
    id: int
    session_id: int
    image_url: Optional[str] = None
    timestamp: datetime
    
    class Config:
        from_attributes = True

# ----- Token Schemas -----
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

# ----- Chat Schemas -----
class ChatRequest(BaseModel):
    """Схема для запроса к AI Мастеру"""
    session_id: int
    player_input: str
    generate_image: Optional[bool] = False  # Будем использовать позже для генерации изображений

class ChatResponse(BaseModel):
    """Схема ответа от AI Мастера"""
    message: MessageResponse
    session_updated: bool = True