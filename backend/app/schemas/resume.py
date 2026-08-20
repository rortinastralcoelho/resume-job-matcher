from pydantic import BaseModel
from datetime import datetime

class ResumeBase(BaseModel):
    filename: str

class ResumeCreate(ResumeBase):
    # What the API expects coming IN from the frontend
    content: str 

class ResumeResponse(ResumeBase):
    # What the API expects going OUT from the database
    id: int
    extracted_text: str
    created_at: datetime

    class Config:
        from_attributes = True