from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class ChatMessage(BaseModel):
    content: str = Field(..., min_length=1, max_length=4000)
    timestamp: Optional[datetime] = None

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=4000)
    conversation_id: Optional[str] = None
    temperature: Optional[float] = Field(0.7, ge=0.1, le=2.0)
    max_tokens: Optional[int] = Field(1024, ge=10, le=2048)

class ChatResponse(BaseModel):
    response: str
    conversation_id: str
    processing_time: float
    model_info: Dict[str, Any]
    timestamp: datetime

class ModelStatus(BaseModel):
    status: str
    model_name: str
    model_loaded: bool
    memory_usage: Optional[Dict[str, str]] = None
    last_updated: datetime

class ErrorResponse(BaseModel):
    error: str
    detail: str
    timestamp: datetime
