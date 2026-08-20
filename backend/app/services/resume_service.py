from sqlalchemy.orm import Session
from app.models.resume import Resume
from app.schemas.resume import ResumeCreate

def create_resume(db: Session, resume: ResumeCreate):
    # THE FIX: We changed 'content' to 'extracted_text' to perfectly match your database!
    db_resume = Resume(filename=resume.filename, extracted_text=resume.content)
    
    db.add(db_resume)
    db.commit()
    db.refresh(db_resume)
    return db_resume

def get_resumes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Resume).offset(skip).limit(limit).all()

def get_resume(db: Session, resume_id: int):
    return db.query(Resume).filter(Resume.id == resume_id).first()