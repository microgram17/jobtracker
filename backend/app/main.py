from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import engine, get_db
from app.models import Base
from app import crud, schemas

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/applications", response_model=list[schemas.JobApplicationResponse])
def read_applications(db: Session = Depends(get_db)):
    return crud.get_applications(db)

@app.get("/applications/{id}", response_model=schemas.JobApplicationResponse)
def read_application(id: int, db: Session = Depends(get_db)):
    return crud.get_application_by_id(db, id)

@app.post("/applications", response_model=schemas.JobApplicationResponse, status_code=201)
def create_application(application: schemas.JobApplicationCreate, db: Session = Depends(get_db)):
    return crud.create_application(db, application)

@app.put("/applications/{id}", response_model=schemas.JobApplicationResponse)
def update_application(id: int, application: schemas.JobApplicationUpdate, db: Session = Depends(get_db)):
    return crud.update_application(db, id, application)

@app.delete("/applications/{id}", response_model=schemas.JobApplicationResponse)
def delete_application(id: int, db: Session = Depends(get_db)):
    return crud.delete_application(db, id)