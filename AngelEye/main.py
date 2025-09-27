"""
Backend logic for the HybridBrain Agent.
Contains functions for interacting with local and cloud AI models for text and image generation.
"""
import base64
import io
import requests
import os
from dotenv import load_dotenv
import google.generativeai as genai
import vertexai
from vertexai.vision_models import ImageGenerationModel

# --- Configuration ---
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GCLOUD_PROJECT_ID = os.getenv("GCLOUD_PROJECT_ID")
genai.configure(api_key=GOOGLE_API_KEY)


# --- AI Specialist Functions ---

def query_local_model(prompt):
    """Sends a prompt to the local Ollama model."""
    print("AI is thinking (using Local Model)...")
    url = "http://localhost:11434/api/generate"
    data = {"model": "llama3.1:8b", "prompt": prompt, "stream": False}
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            return response.json().get("response")
        else:
            return f"Error from local model: {response.text}"
    except requests.exceptions.RequestException as e:
        return f"Error connecting to Ollama. Is it running? Details: {e}"

def query_gemini_model(prompt):
    """Sends a prompt to the Google Gemini Pro model."""
    print("AI is thinking (using Google Gemini)...")
    try:
        model = genai.GenerativeModel('gemini-1.5-pro-latest')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error connecting to Gemini: {e}"

# In main.py, replace the entire generate_image function

def generate_image(prompt: str):
    """
    Generates an image by sending a prompt to the local Stable Diffusion WebUI API.
    """
    print("Sending prompt to local Stable Diffusion WebUI...")
    # This is the default address for the API
    url = "http://127.0.0.1:7860/sdapi/v1/txt2img"

    # This is the data payload we send to the API
    payload = {
        "prompt": prompt,
        "steps": 25
    }

    try:
        # Send the request to the WebUI API
        response = requests.post(url=url, json=payload)
        response.raise_for_status() # Raise an exception for bad status codes

        response_data = response.json()

        # The API returns the image as a Base64 encoded string
        image_data = response_data['images'][0]
        image_bytes = base64.b64decode(image_data)

        print("Image received from WebUI.")
        return image_bytes

    except requests.exceptions.ConnectionError:
        return "Error: Could not connect to the Stable Diffusion WebUI. Is it running with the --api flag?"
    except Exception as e:
        return f"An error occurred: {e}"