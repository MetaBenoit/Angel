import requests
import time
import logging
import os
from typing import Dict, Any, Optional
import psutil

logger = logging.getLogger(__name__)

class DAOModelService:
    """Enhanced DAO Model Service for Angel project - Qwen DAO Professional"""
    
    def __init__(self, model_name: str = "dao_professional"):
        self.model_name = model_name
        self.ollama_url = os.getenv("OLLAMA_HOST", "http://localhost:11434")
        self.model_path = os.getenv("MODEL_PATH", "../dao_training_dojo/outputs/qwen_dao_gguf/unsloth.F16.gguf")
        self.is_loaded = False
        self.last_health_check = None
        
    def load_model(self) -> bool:
        """Check if Ollama model is available and ready"""
        try:
            logger.info(f"Loading DAO Professional (Qwen): {self.model_name}")
            
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=10)
            if response.status_code == 200:
                models = response.json().get("models", [])
                model_names = [model["name"] for model in models]
                
                # Check for exact match or :latest variant
                target_names = [self.model_name, f"{self.model_name}:latest"]
                if any(name in model_names for name in target_names):
                    self.is_loaded = True
                    self.last_health_check = time.time()
                    logger.info(f"✅ DAO Professional (Qwen) model ready: {self.model_name}")
                    return True
                else:
                    logger.error(f"❌ DAO Professional model not found. Available: {model_names}")
                    return False
            else:
                logger.error(f"❌ Ollama service error: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error loading DAO Professional: {str(e)}")
            return False
    
    def generate_response(self, user_message: str, conversation_id: str = None, 
                         temperature: float = 0.75, max_tokens: int = 1024) -> str:
        """Generate response using trained Qwen DAO model"""
        
        if not self.is_loaded:
            if not self.load_model():
                raise RuntimeError("DAO Professional (Qwen) model is not available.")
        
        if not user_message or not user_message.strip():
            raise ValueError("User message cannot be empty")
        
        # Format for your trained Qwen model
        formatted_prompt = f"Human: {user_message.strip()}\n\nDao:"
        
        payload = {
        "model": self.model_name,
        "prompt": formatted_prompt,
        "stream": False,
        "keep_alive": "5m",  # Keep model loaded longer
        "options": {
             "temperature": temperature,
                "num_predict": max_tokens,
            "num_ctx": 2048,  # Reduce context window if not needed
            "top_p": 0.9,
            "repeat_penalty": 1.1,
            "stop": ["Human:", "User:"]
        }
    }
        
        try:
            start_time = time.time()
            response = requests.post(f"{self.ollama_url}/api/generate", json=payload, timeout=120)
            processing_time = time.time() - start_time
            
            if response.status_code == 200:
                result = response.json()
                dao_response = result.get("response", "").strip()
                dao_response = self._clean_response(dao_response)
                logger.info(f"✅ DAO Professional response in {processing_time:.2f}s")
                return dao_response
            else:
                logger.error(f"❌ Ollama error: {response.status_code}")
                raise RuntimeError(f"DAO service error: {response.status_code}")
                
        except Exception as e:
            logger.error(f"💥 Generation error: {str(e)}")
            raise RuntimeError(f"DAO Professional error: {str(e)}")
    
    def _clean_response(self, response: str) -> str:
        """Clean up model response"""
        if not response:
            return "I apologize, but I'm having trouble responding. Could you try again?"
        
        response = response.strip()
        
        # Remove prompt artifacts
        if response.startswith("Dao:"):
            response = response[4:].strip()
        if response.startswith("Human:"):
            response = response[6:].strip()
            
        return response
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get DAO Professional (Qwen) model information"""
        return {
            "agent_name": "Dao",
            "role": "LifeStyle Broker - Bangkok to Pattaya Expert",
            "company": "Ires Thailand", 
            "model_name": self.model_name,
            "model_path": self.model_path,
            "service_url": self.ollama_url,
            "loaded": self.is_loaded,
            "last_health_check": self.last_health_check,
            "trained_base": "Qwen2-7B-Instruct",
            "quantization": "F16 (15.2GB)",
            "training_method": "QLoRA + Unsloth",
            "project": "Angel - DAO Professional (Qwen)",
            "architecture": "dao_model_server"
        }
    
    def get_memory_usage(self) -> Dict[str, str]:
        """Get system memory usage"""
        memory_info = {}
        
        try:
            memory = psutil.virtual_memory()
            memory_info.update({
                "system_total": f"{memory.total / 1024**3:.2f} GB",
                "system_used": f"{memory.used / 1024**3:.2f} GB",
                "system_percent": f"{memory.percent:.1f}%"
            })
            
            try:
                response = requests.get(f"{self.ollama_url}/api/ps", timeout=5)
                if response.status_code == 200:
                    running_models = response.json().get("models", [])
                    if running_models:
                        memory_info["ollama_models"] = f"{len(running_models)} active"
                        for model in running_models:
                            if self.model_name in model.get("name", ""):
                                size_gb = model.get("size", 0) / 1024**3
                                memory_info["dao_model_size"] = f"{size_gb:.1f} GB"
                    else:
                        memory_info["ollama_models"] = "No models loaded"
            except:
                memory_info["ollama_status"] = "Cannot query"
                
        except Exception as e:
            logger.warning(f"Memory info unavailable: {e}")
            
        return memory_info
    
    def health_check(self) -> bool:
        """Health check for DAO Professional"""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
            healthy = response.status_code == 200
            if healthy:
                self.last_health_check = time.time()
            return healthy
        except:
            return False
    
    def unload_model(self):
        """Unload model for reloading"""
        self.is_loaded = False
        self.last_health_check = None
        logger.info("DAO Professional marked for reload")

# Initialize with your trained Qwen model
model_service = DAOModelService(
    model_name=os.getenv("MODEL_NAME", "dao_professional")
)

# Load on import
if not model_service.load_model():
    logger.warning("⚠️ DAO Professional (Qwen) not immediately available. Will retry on first request.")