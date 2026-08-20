import numpy as np
import logging

logger = logging.getLogger(__name__)

def calculate_cosine_similarity(vec1: list[float], vec2: list[float]) -> float:
    """
    Calculates the cosine similarity between two vectors.
    Returns a value between -1.0 and 1.0 (higher is more similar).
    """
    if not vec1 or not vec2:
        return 0.0
    
    try:
        v1 = np.array(vec1)
        v2 = np.array(vec2)
        
        # Check for zero vectors to avoid division by zero
        if np.all(v1 == 0) or np.all(v2 == 0):
            return 0.0

        dot_product = np.dot(v1, v2)
        norm_v1 = np.linalg.norm(v1)
        norm_v2 = np.linalg.norm(v2)
        
        similarity = dot_product / (norm_v1 * norm_v2)
        return float(similarity)
    except Exception as e:
        logger.error(f"Error calculating similarity: {e}")
        return 0.0