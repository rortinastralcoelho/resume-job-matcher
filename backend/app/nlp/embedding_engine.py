import logging
import requests
import os

logger = logging.getLogger(__name__)

# Hugging Face's free Serverless API URL for the exact same model you were using
API_URL = "https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2"

def get_embedding(text: str) -> list[float]:
    """
    Converts text into a high-dimensional vector (embedding) representing its semantic meaning
    by calling Hugging Face's remote API instead of running locally.
    """
    if not text:
        return []
    
    # (Optional) If you get rate-limited later, you can add a HUGGINGFACE_API_KEY to your Render environment variables
    headers = {}
    hf_token = os.getenv("HUGGINGFACE_API_KEY")
    if hf_token:
        headers["Authorization"] = f"Bearer {hf_token}"
        
    try:
        response = requests.post(API_URL, headers=headers, json={"inputs": text})
        
        # If the API hasn't been used in a while, it takes a few seconds to wake up
        if response.status_code == 503:
            logger.error("Hugging Face API is waking up. Try again in 20 seconds.")
            return []
            
        response.raise_for_status()
        embedding = response.json()
        
        # Format the response into a flat list of floats
        if isinstance(embedding, list) and len(embedding) > 0 and isinstance(embedding[0], list):
             return embedding[0]
             
        return embedding
    except Exception as e:
        logger.error(f"Error generating embedding via API: {e}")
        return []