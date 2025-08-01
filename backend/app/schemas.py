from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

status_regex = r"^(applied|interview|offer|rejected)$"

class JobApplicationBase(BaseModel):
    company: str
    position: str
    status: str = Field(..., pattern=status_regex)
    link: Optional[str] = None
    notes: Optional[str] = None
    applied_date: Optional[date] = None
    updated_date: Optional[date] = None

class JobApplicationCreate(JobApplicationBase):
    pass

class JobApplicationUpdate(BaseModel):
    company: Optional[str] = None
    position: Optional[str] = None
    status: Optional[str] = Field(None, pattern=status_regex)
    link: Optional[str] = None
    notes: Optional[str] = None
    applied_date: Optional[date] = None
    updated_date: Optional[date] = None

class JobApplicationResponse(JobApplicationBase):
    id: int

    class Config:
        from_attributes = True  # Pydantic v2: replaces orm_mode