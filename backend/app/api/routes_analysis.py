from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

# --- NEW IMPORTS REQUIRED FOR HISTORY AND COVER LETTER ---
from app.models.analysis import Analysis
from app.models.job import Job
from app.models.resume import Resume
from app.llm.recommender import generate_cover_letter
# ---------------------------------------------------------

# Import the correct ANALYSIS schemas and services
from app.schemas.analysis import AnalysisCreate, AnalysisResponse
from app.services import analysis_service
from app.core.database import get_db

router = APIRouter()

@router.post("/", response_model=AnalysisResponse)
def perform_match_analysis(analysis_req: AnalysisCreate, db: Session = Depends(get_db)):
    """
    Receives the resume_id and job_id from the frontend, 
    and sends them to the NLP service for processing.
    """
    try:
        # Pass the data into your analysis engine
        return analysis_service.create_analysis(db=db, analysis=analysis_req)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis Engine Fault: {str(e)}")

# --- FEATURE 1: GET MATCH HISTORY ---
@router.get("/history")
def get_match_history(db: Session = Depends(get_db)):
    """Fetches all past matches from the database."""
    try:
        # Queries the database for all past analysis results, ordered by newest first
        analyses = db.query(Analysis).order_by(Analysis.id.desc()).all()
        return analyses
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database Fetch Fault: {str(e)}")

# --- FEATURE 2: GENERATE COVER LETTER ---
@router.post("/cover-letter")
def create_cover_letter(job_id: int, resume_id: int, db: Session = Depends(get_db)):
    """Generates a cover letter using the saved job and resume."""
    try:
        job = db.query(Job).filter(Job.id == job_id).first()
        resume = db.query(Resume).filter(Resume.id == resume_id).first()
        
        if not job or not resume:
            raise HTTPException(status_code=404, detail="Job or Resume not found in database.")
            
        cover_letter_text = generate_cover_letter(job.description, resume.extracted_text)
        
        return {"cover_letter": cover_letter_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Cover Letter Generation Fault: {str(e)}")