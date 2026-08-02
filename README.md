arkdown
Copy
Code
Preview
# Task API

A simple CRUD API for managing to-do tasks.

## Installation & Run


pip install -r requirements.txt
uvicorn main:app --reload
Server runs on http://localhost:8000
Endpoints
Table
Method	Path	Description
GET	/	API info
GET	/health	Health check
GET	/tasks	List all tasks
GET	/tasks/{id}	Get one task
POST	/tasks	Create a task
PUT	/tasks/{id}	Update a task
DELETE	/tasks/{id}	Delete a task
Example Request
curl -i http://localhost:8000/tasks
Swagger UI
Interactive docs at http://localhost:8000/docs

 # Why PostgreSQL?

PostgreSQL is a production-grade relational database. Unlike SQLite (single file), Postgres runs as a separate server process, handles concurrent connections, and scales for real applications.

 # Database Setup

- **Local (Docker):** `docker compose up` starts both app and database
- **Cloud (Render):** Set `DATABASE_URL` in `.env` from your Render dashboard
- **Driver:** `psycopg` (Python PostgreSQL adapter)

# Environment Variables

Copy `.env.example` to `.env` and fill in your `DATABASE_URL`:
```bash
cp .env.example .env
Run with Docker Compose
bash
docker compose up
Run Locally (without Docker)
bash
pip install -r requirements.txt
python -m uvicorn main:app --reload