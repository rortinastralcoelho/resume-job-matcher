import re
import spacy
import logging

logger = logging.getLogger(__name__)

try:
    # Load the pre-trained spaCy model
    nlp = spacy.load("en_core_web_sm")
except OSError:
    logger.error("spaCy model 'en_core_web_sm' not found. Please run: python -m spacy download en_core_web_sm")
    nlp = None

def clean_text(text: str) -> str:
    """
    Standardizes text by removing special characters, normalizing whitespace,
    and using spaCy for lemmatization and stop-word removal.
    """
    if not text:
        return ""

    # Step 1: Basic Regex Cleaning
    # Remove non-alphanumeric characters but keep basic punctuation for context
    text = re.sub(r'[^a-zA-Z0-9\s\.\,\;]', ' ', text)
    
    # Normalize whitespaces
    text = re.sub(r'\s+', ' ', text).strip()

    # Step 2: Advanced NLP Cleaning (if the model loaded successfully)
    if nlp:
        doc = nlp(text)
        
        # Lemmatize tokens and remove stop words / punctuation
        cleaned_tokens = [
            token.lemma_.lower() for token in doc 
            if not token.is_stop and not token.is_punct and token.text.strip()
        ]
        return " ".join(cleaned_tokens)
    
    # Fallback just in case spaCy fails to load
    return text.lower()