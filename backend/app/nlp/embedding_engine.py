import logging
from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)

try:
    # Load a lightweight, fast, and highly accurate pre-trained model
    model = SentenceTransformer('all-MiniLM-L6-v2')
except Exception as e:
    logger.error(f"Failed to load SentenceTransformer model: {e}")
    model = None

def get_embedding(text: str) -> list[float]:
    """
    Converts text into a high-dimensional vector (embedding) representing its semantic meaning.
    """
    if not text or model is None:
        return []
    
    try:
        # Generate and return the embedding as a list of floats
        embedding = model.encode(text)
        return embedding.tolist()
    except Exception as e:
        logger.error(f"Error generating embedding: {e}")
        return []