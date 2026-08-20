import json
import os
import re
import logging

logger = logging.getLogger(__name__)

# Dynamically locate the taxonomy file in the same directory as this script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TAXONOMY_PATH = os.path.join(BASE_DIR, "skill_taxonomy.json")

def load_taxonomy(path: str = TAXONOMY_PATH) -> dict:
    """
    Loads the skill taxonomy dictionary from the JSON file.
    """
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Failed to load skill taxonomy: {e}")
        return {}

def extract_skills(cleaned_text: str, taxonomy: dict = None) -> list:
    """
    Scans the cleaned text and extracts any skills that exist in the taxonomy.
    Returns a deduplicated list of found skills.
    """
    if taxonomy is None:
        taxonomy = load_taxonomy()

    if not cleaned_text or not taxonomy:
        return []

    found_skills = set()
    
    # Flatten the taxonomy dictionary into a single list of all skills
    all_known_skills = []
    for category_skills in taxonomy.values():
        all_known_skills.extend(category_skills)

    for skill in all_known_skills:
        # Create a regex pattern with word boundaries (\b) to find exact matches
        # re.IGNORECASE ensures "Python" matches "python"
        pattern = r'\b' + re.escape(skill) + r'\b'
        
        if re.search(pattern, cleaned_text, re.IGNORECASE):
            found_skills.add(skill.lower())

    return list(found_skills)