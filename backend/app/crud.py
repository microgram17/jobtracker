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

def create_application(db: Session, schema: schemas.JobApplicationCreate):
    obj = models.JobApplication(**schema.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def update_application(db: Session, id: int, schema: schemas.JobApplicationUpdate):
    app = db.query(models.JobApplication).filter(models.JobApplication.id == id).first()
    if not app:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found")
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