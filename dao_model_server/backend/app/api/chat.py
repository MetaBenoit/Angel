from fastapi import APIRouter, HTTPException, BackgroundTasks
from app.models import ChatRequest, ChatResponse, ModelStatus, ErrorResponse
from app.services.model_service import model_service
import time
import uuid
from datetime import datetime
import logging
import asyncio

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat_with_model(request: ChatRequest, background_tasks: BackgroundTasks):
    """Chat with DAO Professional (Qwen) - Angel project"""
    try:
        start_time = time.time()
        
        # Validate input
        if not request.message or not request.message.strip():
            raise HTTPException(status_code=400, detail="Message cannot be empty")
        
        # Generate conversation ID
        conversation_id = request.conversation_id or str(uuid.uuid4())
        
        logger.info(f"DAO Professional processing: {request.message[:50]}...")
        
        # Generate response with your trained Qwen model
        response_text = model_service.generate_response(
            user_message=request.message,
            conversation_id=conversation_id,
            temperature=request.temperature or 0.75,
            max_tokens=request.max_tokens or 1024
        )
        
        processing_time = time.time() - start_time
        
        # Background logging
        background_tasks.add_task(
            log_interaction,
            request.message,
            response_text,
            processing_time,
            conversation_id
        )
        
        # Return proper ChatResponse format
        return ChatResponse(
            response=response_text,
            conversation_id=conversation_id,
            processing_time=processing_time,
            model_info=model_service.get_model_info(),
            timestamp=datetime.now()
        )
        
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Invalid input: {str(e)}")
    except RuntimeError as e:
        logger.error(f"DAO Professional error: {str(e)}")
        raise HTTPException(status_code=503, detail=f"DAO service error: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/status", response_model=ModelStatus)
async def get_model_status():
    """Get DAO Professional (Qwen) status"""
    try:
        is_responsive = model_service.health_check() if model_service.is_loaded else False
        
        return ModelStatus(
            status="ready" if (model_service.is_loaded and is_responsive) else "loading",
            model_name="dao_professional",  # Consistent naming
            model_loaded=model_service.is_loaded,
            memory_usage=model_service.get_memory_usage(),
            last_updated=datetime.now()
        )
    except Exception as e:
        logger.error(f"Status error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/reload")
async def reload_model():
    """Reload DAO Professional (Qwen) model"""
    try:
        logger.info("Reloading DAO Professional (Qwen)...")
        model_service.unload_model()
        await asyncio.sleep(2)
        
        success = model_service.load_model()
        
        if success:
            return {
                "message": "DAO Professional (Qwen) reloaded successfully",
                "status": "ready", 
                "model_name": model_service.model_name,
                "timestamp": datetime.now()
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to reload DAO Professional")
            
    except Exception as e:
        logger.error(f"Reload error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def health_check():
    """Health check for DAO Professional system"""
    try:
        model_healthy = model_service.health_check()
        return {
            "status": "healthy" if model_healthy else "degraded",
            "service": "dao-professional-api",
            "version": "1.0.0",
            "model": "dao_professional",
            "model_ready": model_service.is_loaded,
            "timestamp": datetime.now()
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=503, detail="Service unhealthy")

async def log_interaction(user_message: str, bot_response: str, processing_time: float, conversation_id: str):
    """Log DAO Professional interactions"""
    try:
        logger.info(
            f"Angel DAO Professional (Qwen) - "
            f"Conv: {conversation_id[:8]}..., "
            f"Time: {processing_time:.2f}s, "
            f"User: {len(user_message)} chars, "
            f"DAO: {len(bot_response)} chars"
        )
    except Exception as e:
        logger.error(f"Logging error: {str(e)}")