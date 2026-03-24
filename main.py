from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from . import models, schemas, crud
from .database import SessionLocal, engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="CRUD API for Jobs and Companies")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Company endpoints
@app.post("/companies/", response_model=schemas.Company)
def create_company(company: schemas.CompanyCreate, db: Session = Depends(get_db)):
    return crud.create_company(db=db, company=company)

@app.get("/companies/", response_model=List[schemas.Company])
def read_companies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    companies = crud.get_companies(db, skip=skip, limit=limit)
    return companies

@app.get("/companies/{company_id}", response_model=schemas.Company)
def read_company(company_id: int, db: Session = Depends(get_db)):
    db_company = crud.get_company(db, company_id=company_id)
    if db_company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    return db_company

@app.put("/companies/{company_id}", response_model=schemas.Company)
def update_company(company_id: int, company: schemas.CompanyUpdate, db: Session = Depends(get_db)):
    db_company = crud.update_company(db, company_id=company_id, company_update=company)
    if db_company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    return db_company

@app.delete("/companies/{company_id}")
def delete_company(company_id: int, db: Session = Depends(get_db)):
    db_company = crud.delete_company(db, company_id=company_id)
    if db_company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    return {"message": "Company deleted"}

# Job endpoints
@app.post("/jobs/", response_model=schemas.Job)
def create_job(job: schemas.JobCreate, db: Session = Depends(get_db)):
    return crud.create_job(db=db, job=job)

@app.get("/jobs/", response_model=List[schemas.Job])
def read_jobs(
    skip: int = 0,
    limit: int = 100,
    location: Optional[str] = Query(None, description="Filter by location"),
    job_type: Optional[str] = Query(None, description="Filter by job type"),
    db: Session = Depends(get_db)
):
    jobs = crud.get_jobs(db, skip=skip, limit=limit, location=location, job_type=job_type)
    return jobs

@app.get("/jobs/{job_id}", response_model=schemas.Job)
def read_job(job_id: int, db: Session = Depends(get_db)):
    db_job = crud.get_job(db, job_id=job_id)
    if db_job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return db_job

@app.put("/jobs/{job_id}", response_model=schemas.Job)
def update_job(job_id: int, job: schemas.JobUpdate, db: Session = Depends(get_db)):
    db_job = crud.update_job(db, job_id=job_id, job_update=job)
    if db_job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return db_job

@app.delete("/jobs/{job_id}")
def delete_job(job_id: int, db: Session = Depends(get_db)):
    db_job = crud.delete_job(db, job_id=job_id)
    if db_job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return {"message": "Job deleted"}