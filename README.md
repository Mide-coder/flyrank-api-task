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
