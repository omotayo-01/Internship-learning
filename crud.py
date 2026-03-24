from sqlalchemy.orm import Session
from . import models, schemas
from typing import Optional

# Company CRUD
def get_company(db: Session, company_id: int):
    return db.query(models.Company).filter(models.Company.id == company_id).first()

def get_companies(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Company).offset(skip).limit(limit).all()

def create_company(db: Session, company: schemas.CompanyCreate):
    db_company = models.Company(**company.model_dump())
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company

def update_company(db: Session, company_id: int, company_update: schemas.CompanyUpdate):
    db_company = db.query(models.Company).filter(models.Company.id == company_id).first()
    if db_company:
        update_data = company_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_company, field, value)
        db.commit()
        db.refresh(db_company)
    return db_company

def delete_company(db: Session, company_id: int):
    db_company = db.query(models.Company).filter(models.Company.id == company_id).first()
    if db_company:
        db.delete(db_company)
        db.commit()
    return db_company

# Job CRUD
def get_job(db: Session, job_id: int):
    return db.query(models.Job).filter(models.Job.id == job_id).first()

def get_jobs(db: Session, skip: int = 0, limit: int = 100, location: Optional[str] = None, job_type: Optional[str] = None):
    query = db.query(models.Job)
    if location:
        query = query.filter(models.Job.location.ilike(f"%{location}%"))
    if job_type:
        query = query.filter(models.Job.job_type.ilike(f"%{job_type}%"))
    return query.offset(skip).limit(limit).all()

def create_job(db: Session, job: schemas.JobCreate):
    db_job = models.Job(**job.model_dump())
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

def update_job(db: Session, job_id: int, job_update: schemas.JobUpdate):
    db_job = db.query(models.Job).filter(models.Job.id == job_id).first()
    if db_job:
        update_data = job_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_job, field, value)
        db.commit()
        db.refresh(db_job)
    return db_job

def delete_job(db: Session, job_id: int):
    db_job = db.query(models.Job).filter(models.Job.id == job_id).first()
    if db_job:
        db.delete(db_job)
        db.commit()
    return db_job