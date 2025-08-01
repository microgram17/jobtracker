# 📋 Job Application Tracker

A full-stack application to help you organize and track your job applications in one place. This project serves as an MVP portfolio demonstration, combining modern backend and frontend technologies to create a practical, user-friendly tool.

## 🛠️ Tech Stack

**Backend:**
- [FastAPI](https://fastapi.tiangolo.com/) - Modern, high-performance web framework
- [SQLAlchemy](https://www.sqlalchemy.org/) - SQL toolkit and ORM
- [SQLite](https://www.sqlite.org/) (development) / PostgreSQL (production ready)
- RESTful API architecture

**Frontend:**
- [Streamlit](https://streamlit.io/) - Rapid UI development framework
- Responsive design with built-in components

**Infrastructure:**
- [Docker](https://www.docker.com/) & Docker Compose
- Hot-reloading development environment

## 🚀 Getting Started

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/)
- Git

### Quick Start

1. Clone the repository:
   ```bash
   git clone https://github.com/microgram17/jobtracker.git
   cd jobtracker
   ```

2. Start the application with Docker Compose:
   ```bash
   docker-compose up
   ```

3. Access the application:
   - Frontend: http://localhost:8501
   - API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Development Setup

The project is configured with hot-reloading for both frontend and backend:

- Backend changes in `./backend/app` will automatically reload
- Frontend changes in `./frontend` will automatically reload
- The SQLite database persists between container restarts

## 📝 Usage Guide

### Managing Job Applications

- **Add new applications** using the form at the top
- **Filter applications** by status using the dropdown menu
- **Edit** your applications by clicking the 'Edit' button
- **Delete** applications with a two-step confirmation process
- **View Notes** by expanding the notes section under each application

### Application Fields

- **Company**: The name of the company (required)
- **Position**: Job title or position (required)
- **Status**: Current application status (applied, interview, offer, rejected)
- **Link**: URL to the job posting or company website (optional)
- **Notes**: Any additional information about the application (optional)
- **Applied Date**: When you submitted the application

## 📄 License

This project is [MIT](./LICENSE) licensed.
