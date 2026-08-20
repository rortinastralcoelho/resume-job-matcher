from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional, Any

class AnalysisCreate(BaseModel):
    # INBOUND
    resume_id: int
    job_id: int

class AnalysisResponse(BaseModel):
    # OUTBOUND (Perfectly matched to models/analysis.py)
    id: int
    resume_id: int
    job_id: int
    overall_score: float 
    semantic_score: Optional[float] = None
    skill_score: Optional[float] = None
    matched_skills: Optional[list] = []
    missing_skills: Optional[list] = []
    feedback: str
    created_at: datetime

    class Config:
        from_attributes = True