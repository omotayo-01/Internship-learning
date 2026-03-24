from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Company schemas
class CompanyBase(BaseModel):
    name: str
    location: str
    industry: str

class CompanyCreate(CompanyBase):
    pass

class CompanyUpdate(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    industry: Optional[str] = None

class Company(CompanyBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Job schemas
class JobBase(BaseModel):
    title: str
    description: str
    job_type: str
    location: str
    salary: str
    company_id: int

class JobCreate(JobBase):
    pass

class JobUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    job_type: Optional[str] = None
    location: Optional[str] = None
    salary: Optional[str] = None
    company_id: Optional[int] = None

class Job(JobBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True