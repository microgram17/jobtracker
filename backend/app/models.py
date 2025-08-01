from sqlalchemy import Column, Integer, String, Enum, Date
from sqlalchemy.ext.declarative import declarative_base
import enum

Base = declarative_base()

class ApplicationStatus(enum.Enum):
    applied = "applied"
    interview = "interview"
    offer = "offer"
    rejected = "rejected"

class JobApplication(Base):
    __tablename__ = "job_applications"

    id = Column(Integer, primary_key=True, index=True)
    company = Column(String, nullable=False)
    position = Column(String, nullable=False)
    status = Column(Enum(ApplicationStatus), nullable=False)
    link = Column(String, nullable=True)
    notes = Column(String, nullable=True)
    applied_date = Column(Date, nullable=True)
    updated_date = Column(Date, nullable=True)  # New column

    def __repr__(self):
        return (
            f"<JobApplication(id={self.id}, company='{self.company}', "
            f"position='{self.position}', status='{self.status.name}', "
            f"link='{self.link}', notes='{self.notes}', applied_date={self.applied_date}, "
            f"updated_date={self.updated_date})>"
        )