from sqlalchemy.orm import Session
from app.models.analysis import Analysis
from app.schemas.analysis import AnalysisCreate
from app.models.job import Job
from app.models.resume import Resume
from app.nlp.scoring_engine import calculate_final_score
from app.nlp.skill_extractor import extract_skills

# IMPORT THE LLM RECOMMENDER
from app.llm.recommender import generate_resume_recommendations

def create_analysis(db: Session, analysis: AnalysisCreate):
    resume = db.query(Resume).filter(Resume.id == analysis.resume_id).first()
    job = db.query(Job).filter(Job.id == analysis.job_id).first()

    if not resume or not job:
        raise Exception("Database Error: Could not find the Resume or Job.")

    # --- 🛑 THE GIBBERISH FILTER: Fixes the Score to 0% for fake jobs ---
    words = job.description.split()
    
    # Check if the job description is less than 5 words OR contains massive keyboard smashes (>50 chars)
    if len(words) < 5 or any(len(word) > 50 for word in words):
        
        # Bypass the NLP engine and LLM completely. Force scores to 0.0.
        db_analysis = Analysis(
            resume_id=analysis.resume_id,
            job_id=analysis.job_id,
            overall_score=0.0,
            semantic_score=0.0,
            skill_score=0.0,
            matched_skills=[],
            missing_skills=[],
            feedback="### ❌ Invalid Input Detected\nThe job description provided is either too short or contains random characters. Please provide a real job description so the AI can give you an accurate score and feedback."
        )
        
        db.add(db_analysis)
        db.commit()
        db.refresh(db_analysis)
        return db_analysis
    # ------------------------------------------------------

    # 1. Run the NLP Scoring Engine
    resume_skills_list = extract_skills(resume.extracted_text)
    job_skills_list = extract_skills(job.description)
    
    results = calculate_final_score(
        resume_text=resume.extracted_text, 
        job_text=job.description, 
        resume_skills=resume_skills_list, 
        job_skills=job_skills_list
    )

    # --- 🛑 THE RESUME FILTER: Stops the AI if it's a receipt or irrelevant ---
    if results["overall_match_percentage"] == 0:
        llm_feedback = "### ❌ Invalid or Irrelevant Document\nThe uploaded document scored 0%. It either does not appear to be a valid resume, or it contains absolutely no technical overlap with this job description. Please upload a relevant document."
    else:
        # 2. GENERATE DYNAMIC LLM RECOMMENDATIONS (Only runs if score > 0)
        llm_feedback = generate_resume_recommendations(
            job_description=job.description,
            resume_text=resume.extracted_text,
            missing_skills=results["missing_skills"]
        )
    # ------------------------------------------------------

    # 3. Save the comprehensive report to the database
    db_analysis = Analysis(
        resume_id=analysis.resume_id,
        job_id=analysis.job_id,
        overall_score=results["overall_match_percentage"],
        semantic_score=results["semantic_similarity_score"],
        skill_score=results["skill_match_score"],
        matched_skills=results["matched_skills"],
        missing_skills=results["missing_skills"],
        feedback=llm_feedback  # Now protected from 0% scores
    )
    
    db.add(db_analysis)
    db.commit()
    db.refresh(db_analysis)
    return db_analysis

def get_analyses_for_job(db: Session, job_id: int):
    return db.query(Analysis).filter(Analysis.job_id == job_id).all()