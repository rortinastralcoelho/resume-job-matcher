from pydantic import BaseModel
from datetime import datetime

class JobBase(BaseModel):
    title: str
    description: str

class JobCreate(JobBase):
    pass

class JobResponse(JobBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True