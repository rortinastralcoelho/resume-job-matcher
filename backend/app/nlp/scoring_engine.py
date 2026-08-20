import logging
from .embedding_engine import get_embedding
from .similarity import calculate_cosine_similarity
from .ats_scorer import calculate_skill_match_score

logger = logging.getLogger(__name__)

def calculate_final_score(resume_text: str, job_text: str, resume_skills: list[str], job_skills: list[str]) -> dict:
    """
    Combines semantic similarity and exact skill matching to generate a final ATS score report.
    """
    # 1. Semantic Similarity Score (Context & Meaning)
    resume_emb = get_embedding(resume_text)
    job_emb = get_embedding(job_text)
    semantic_score = calculate_cosine_similarity(resume_emb, job_emb)
    
    # Normalize score to ensure it is positive
    normalized_semantic_score = max(0.0, semantic_score)

    # 2. Skill Match Score (Exact Keyword Requirements)
    skill_score = calculate_skill_match_score(resume_skills, job_skills)
    
    # 3. Final Weighted Score (60% Semantic, 40% Hard Skills)
    weight_semantic = 0.60
    weight_skills = 0.40
    
    final_score = (normalized_semantic_score * weight_semantic) + (skill_score * weight_skills)
    
    # Deduplicate and format skill lists
    r_skills_set = set([s.lower() for s in resume_skills])
    j_skills_set = set([s.lower() for s in job_skills])
    
    return {
        "overall_match_percentage": round(final_score * 100, 2),
        "semantic_similarity_score": round(normalized_semantic_score * 100, 2),
        "skill_match_score": round(skill_score * 100, 2),
        "matched_skills": list(j_skills_set.intersection(r_skills_set)),
        "missing_skills": list(j_skills_set.difference(r_skills_set))
    }