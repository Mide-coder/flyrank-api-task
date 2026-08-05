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

# Task API with Authentication

A secure CRUD API for managing to-do tasks, built with FastAPI, PostgreSQL, and Supabase Auth.

## Features

- Full CRUD for tasks (Create, Read, Update, Delete)
- User authentication via Supabase Auth (Sign Up, Log In, Log Out)
- JWT token verification on protected routes
- Reusable auth middleware with FastAPI dependencies
- Interactive Swagger UI with Bearer token authorization

## Stack

Python · FastAPI · PostgreSQL · Supabase Auth · JWT · Docker

## Setup

1. Clone the repo
2. Copy environment variables:
   ```bash
   cp .env.example .env
Fill in your Supabase URL, Supabase anon key, and PostgreSQL database URL in .env
Install dependencies:
bash
pip install -r requirements.txt
Start the server:
bash
python -m uvicorn main:app --reload
Environment Variables
Table
Variable	Description
SUPABASE_URL	Your Supabase project URL
SUPABASE_KEY	Your Supabase anon key
DATABASE_URL	PostgreSQL connection string
Endpoints
Table
Method	Path	Auth Required	Description
GET	/	No	API info
GET	/health	No	Health check
GET	/public/info	No	Public information
POST	/auth/signup	No	Create new user account
POST	/auth/login	No	Log in, receive JWT
POST	/auth/logout	Yes	Log out
GET	/protected/profile	Yes	View user profile
GET	/protected/dashboard	Yes	View dashboard
GET	/tasks	No	List all tasks
GET	/tasks/{id}	No	Get one task
POST	/tasks	No	Create a task
PUT	/tasks/{id}	No	Update a task
DELETE	/tasks/{id}	No	Delete a task
Authentication Flow
Sign Up: POST /auth/signup with email and password
Log In: POST /auth/login — receive access_token
Call Protected Route: Include Authorization: Bearer <token> header
Log Out: POST /auth/logout with token
Example curl
bash
# Sign up
curl -X POST http://localhost:8000/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password123"}'

# Log in
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password123"}'

# Access protected route
curl http://localhost:8000/protected/profile \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
Swagger UI
Interactive docs at http://localhost:8000/docs
Click the Authorize button and paste your access token to test protected routes.
Docker
bash
docker compose up
Why Supabase Auth?
Supabase handles auth handling 