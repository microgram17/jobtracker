from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app import models, schemas

def get_applications(db: Session):
    return db.query(models.JobApplication).all()

def get_application_by_id(db: Session, id: int):
    app = db.query(models.JobApplication).filter(models.JobApplication.id == id).first()
    if not app:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found")
    return app

def get_application_by_company_position(db: Session, company: str, position: str):
    return db.query(models.JobApplication).filter(
        models.JobApplication.company == company,
        models.JobApplication.position == position
    ).first()

def create_application(db: Session, schema: schemas.JobApplicationCreate):
    # Check for duplicates first
    existing = get_application_by_company_position(db, schema.company, schema.position)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="A job application for this company and position already exists"
        )
    
    obj = models.JobApplication(**schema.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def update_application(db: Session, id: int, schema: schemas.JobApplicationUpdate):
    app = db.query(models.JobApplication).filter(models.JobApplication.id == id).first()
    if not app:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found")
    
    # If company or position is being updated, check for duplicates
    if (schema.company is not None and schema.company != app.company) or \
       (schema.position is not None and schema.position != app.position):
        # Only check if both fields are provided in the update
        if schema.company is not None and schema.position is not None:
            company_to_check = schema.company
            position_to_check = schema.position
        elif schema.company is not None:
            company_to_check = schema.company
            position_to_check = app.position
        else:
            company_to_check = app.company
            position_to_check = schema.position
            
        existing = get_application_by_company_position(db, company_to_check, position_to_check)
        if existing and existing.id != id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="A job application for this company and position already exists"
            )
    
    for field, value in schema.dict(exclude_unset=True).items():
        setattr(app, field, value)
    db.commit()
    db.refresh(app)
    return app

def delete_application(db: Session, id: int):
    app = db.query(models.JobApplication).filter(models.JobApplication.id == id).first()
    if not app:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found")
    db.delete(app)
    db.commit()
    return app