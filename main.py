from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional

class TaskCreate(BaseModel):
    title: str | None = None
    done: bool | None = None
class TaskUpdate(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None
tasks = [
    {"id": 1, "title": "Code", "done": True},
    {"id": 2, "title": "Test", "done": False},
    {"id": 3, "title": "Deploy", "done": False}
]
app = FastAPI()

@app.get("/", summary="API Root", description="Returns basic information about the API and its endpoints")
# The root endpoint provides basic information about the API, including its name, version, and available endpoints.")
def read_root():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": [
             "/",  "/health",
         ]
    }
@app.get("/health", summary="Health Check", description="Returns the health status of the API")
#checks the health of the API and returns a status message indicating whether the API is operational or not.")
def health_check():
    return {"status": "ok"}

@app.get("/tasks", summary="Get All Tasks", description="Returns a list of all tasks")
# This endpoint retrieves all tasks currently stored in the system and returns them as a list of task objects.")
def get_tasks():
    return tasks

@app.get("/tasks/{task_id}", summary="Get Task by ID", description="Returns a specific task by its ID")
# This endpoint retrieves a specific task based on the provided task ID. If the task is found, it returns the task object; otherwise, it returns a 404 error indicating that the task was not found.")
def get_task(task_id: int):
    task = next((task for task in tasks if task["id"] == task_id), None)
    if task:
        return task
    return JSONResponse(status_code=404, content={"error": f"Task {task_id} not found"})

@app.post("/tasks", summary="Create Task", description="Creates a new task")
# This endpoint allows the creation of a new task. It expects a JSON payload containing the task title and an optional done status. If the title is missing or empty, it returns a 400 error. Upon successful creation, it returns the newly created task with a 201 status code.")
def create_task(task: TaskCreate):
    if not task.title or task.title.strip() == "":
        return JSONResponse(status_code=400, content={"error": "Title is required"})
    
    next_id = max(t["id"] for t in tasks) + 1 if tasks else 1
    
    new_task = {"id": next_id, "title": task.title, "done": False}
    tasks.append(new_task)
    
    return JSONResponse(status_code=201, content=new_task)

@app.put("/tasks/{task_id}", summary="Update Task", description="Updates an existing task")
# This endpoint allows updating an existing task based on the provided task ID. It expects a JSON payload containing the fields to be updated (title and/or done status). If the task is not found, it returns a 404 error. If the title is provided but is empty, it returns a 400 error. Upon successful update, it returns the updated task object.")
def update_task(task_id: int, task: TaskUpdate):
    existing_task = next((t for t in tasks if t["id"] == task_id), None)
    if not existing_task:
        return JSONResponse(status_code=404, content={"error": f"Task {task_id} not found"})
    
    # Only update fields that were actually sent
    if task.title is not None:
        if task.title.strip() == "":
            return JSONResponse(status_code=400, content={"error": "Title cannot be empty"})
        existing_task["title"] = task.title
    
    if task.done is not None:
        existing_task["done"] = task.done
    
    return existing_task

@app.delete("/tasks/{task_id}", summary="Delete Task", description="Deletes an existing task")
# This endpoint allows deleting an existing task based on the provided task ID. If the task is not found, it returns a 404 error. Upon successful deletion, it returns a 204 status code with no content.")
def delete_task(task_id: int):
    global tasks
    task = next((t for t in tasks if t["id"] == task_id), None)
    if not task:
        return JSONResponse(status_code=404, content={"error": f"Task {task_id} not found"})
    
    tasks = [t for t in tasks if t["id"] != task_id]
    return JSONResponse(status_code=204, content={})