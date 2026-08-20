import logging

logger = logging.getLogger(__name__)

def calculate_skill_match_score(resume_skills: list[str], job_skills: list[str]) -> float:
    """
    Calculates the percentage of job skills that are present in the resume.
    Returns a score between 0.0 and 1.0.
    """
    if not job_skills:
        # If the job requires no specific skills, we can't penalize the resume
        return 1.0
    
    if not resume_skills:
        return 0.0
    
    # Convert to sets for easy comparison
    resume_set = set([skill.lower() for skill in resume_skills])
    job_set = set([skill.lower() for skill in job_skills])
    
    # Find matching skills
    matched_skills = job_set.intersection(resume_set)
    
    # Calculate the ratio
    score = len(matched_skills) / len(job_set)
    return float(score)