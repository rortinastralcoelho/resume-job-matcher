from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.orm import Session
from typing import List
import io
import PyPDF2

from app.schemas.resume import ResumeCreate, ResumeResponse
from app.services import resume_service
from app.core.database import get_db

router = APIRouter()

@router.post("/", response_model=ResumeResponse)
async def create_resume(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # 1. Read the raw physical file data
    contents = await file.read()
    extracted_text = ""

    # 2. Decode the data based on file type
    if file.filename.lower().endswith('.pdf'):
        try:
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(contents))
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    extracted_text += page_text + "\n"
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"PDF extraction failed: {str(e)}")
    else:
        # Fallback for standard .txt files
        try:
            extracted_text = contents.decode('utf-8')
        except:
            extracted_text = str(contents)

    # 3. Package the extracted text into the schema your database expects
    resume_data = ResumeCreate(
        filename=file.filename, 
        content=extracted_text
    )
    
    return resume_service.create_resume(db=db, resume=resume_data)

@router.get("/", response_model=List[ResumeResponse])
def read_resumes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return resume_service.get_resumes(db=db, skip=skip, limit=limit)

@router.get("/{resume_id}", response_model=ResumeResponse)
def read_resume(resume_id: int, db: Session = Depends(get_db)):
    db_resume = resume_service.get_resume(db=db, resume_id=resume_id)
    if db_resume is None:
        raise HTTPException(status_code=404, detail="Resume not found")
    return db_resume