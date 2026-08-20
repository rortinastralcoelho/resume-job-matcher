from sqlalchemy import Column, Integer, Float, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer, ForeignKey("resumes.id"))
    job_id = Column(Integer, ForeignKey("jobs.id"))
    
    # The scores from Phase 3
    overall_score = Column(Float)
    semantic_score = Column(Float)
    skill_score = Column(Float)
    
    # Store the exact skills found/missing as JSON lists
    matched_skills = Column(JSON)
    missing_skills = Column(JSON)
    feedback = Column(Text)
    
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships to easily grab the connected resume or job data
    resume = relationship("Resume")
    job = relationship("Job")