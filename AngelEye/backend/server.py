from fastapi import FastAPI
from pydantic import BaseModel
import requests
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import base64
import io
import json # New import for reading the personality file

# --- Load Personalities at Startup ---
with open("personalities.json", "r") as f:
    PERSONALITIES = json.load(f)

# --- Pydantic Models ---
# Updated to include personality and chat history
class ChatRequest(BaseModel):
    prompt: str
    personality: str = "Default" # Use "Default" if none is provided
    history: list = []

# --- FastAPI App ---
app = FastAPI(title="Angel Agent API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)

# --- AI Specialist Functions (Updated for Personality & Memory) ---

def query_local_model(prompt: str, system_prompt: str, history: list):
    """Sends a prompt to the local Ollama model with personality and history."""
    print("AI is thinking (using Local Model)...")
    url = "http://localhost:11434/api/generate"
    
    # Format the conversation history for the model
    full_prompt = ""
    for message in history:
        full_prompt += f"{message['role']}: {message['content']}\n"
    full_prompt += f"user: {prompt}"

    data = {
        "model": "llama3.1:8b",
        "prompt": full_prompt,
        "system": system_prompt, # Pass the personality here
        "stream": False
    }
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            return response.json().get("response", "No response content found.")
        else:
            return f"Error from local model: {response.text}"
    except requests.exceptions.RequestException as e:
        return f"Error connecting to Ollama. Is it running? Details: {e}"

# NOTE: We will update the other functions (Gemini, Image Gen) later.
# For now, we focus on the core local chat functionality.

# --- API Endpoints ---
@app.get("/")
async def root():
    return {"message": "Angel Agent API is running."}

@app.post("/api/chat/local")
async def chat_local(request: ChatRequest):
    """Receives a prompt and personality, returns a response from the local model."""
    try:
        system_prompt = PERSONALITIES[request.personality]["prompt"]
    except KeyError:
        return {"response": "Error: Personality not found."}
        
    response_text = query_local_model(request.prompt, system_prompt, request.history)
    return {"response": response_text}