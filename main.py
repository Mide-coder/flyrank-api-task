from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
import sqlite3

def init_db():
    print("Initializing database...")
    conn = sqlite3.connect("tasks.db")  
    print("Connected to the database.")
    cursor = conn.cursor()
    print("Creating tasks table if it doesn't exist...")
    cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        done BOOLEAN NOT NULL CHECK (done IN (0, 1))
                    )''')
    print("Tasks table created or already exists.")
    cursor.execute("SELECT COUNT(*) FROM tasks")
    count = cursor.fetchone()[0]
    print("Checking for existing tasks in the database...")
    print(f"Number of tasks in the database: {count}")
    if count == 0:
        print("No tasks found. Inserting default tasks...")
        cursor.execute("INSERT INTO tasks (title, done) VALUES (?, ?)", ("Code", 1))
        cursor.execute("INSERT INTO tasks (title, done) VALUES (?, ?)", ("Test", 0))
        cursor.execute("INSERT INTO tasks (title, done) VALUES (?, ?)", ("Deploy", 0))
    conn.commit()   
    conn.close()
print("Database initialization complete.")
init_db()


def get_db_connection():
    conn = sqlite3.connect("tasks.db")
    conn.row_factory = sqlite3.Row
    return conn

class TaskCreate(BaseModel):
    title: str | None = None
    done: bool | None = None
class TaskUpdate(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None
tasks = [
    {"id": 1, "title": "Code", "done": 1},
    {"id": 2, "title": "Test", "done": 0},
    {"id": 3, "title": "Deploy", "done": 0}
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
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    rows = cursor.fetchall()
    conn.close()
    tasks = [
        {"id": row["id"], "title": row["title"], "done": bool(row["done"])} for row in rows
    ] 
    return tasks

@app.get("/tasks/{task_id}", summary="Get Task by ID", description="Returns a specific task by its ID")
# This endpoint retrieves a specific task based on the provided task ID. If the task is found, it returns the task object; otherwise, it returns a 404 error indicating that the task was not found.")
def get_task(task_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    row = cursor.fetchone()
    conn.close()
    if row is not None:
        task = {"id": row["id"], "title": row["title"], "done": bool(row["done"])}
        return task
    else:
        return JSONResponse(status_code=404, content={"error": f"Task {task_id} not found"})


@app.post("/tasks", summary="Create Task", description="Creates a new task")
# This endpoint allows the creation of a new task. It expects a JSON payload containing the task title and an optional done status. If the title is missing or empty, it returns a 400 error. Upon successful creation, it returns the newly created task with a 201 status code.")
def create_task(task: TaskCreate):
    if not task.title or task.title.strip() == "":
        return JSONResponse(status_code=400, content={"error": "Title is required"})
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (title, done) VALUES (?, ?)", (task.title, 1 if task.done else False))
    conn.commit()
    new_task_id = cursor.lastrowid
    conn.close()

    return JSONResponse(status_code=201, content={"id": new_task_id, "title": task.title, "done": task.done if task.done is not None else False})

@app.put("/tasks/{task_id}", summary="Update Task", description="Updates an existing task")
# This endpoint allows updating an existing task based on the provided task ID. It expects a JSON payload containing the fields to be updated (title and/or done status). If the task is not found, it returns a 404 error. If the title is provided but is empty, it returns a 400 error. Upon successful update, it returns the updated task object.")
@app.put("/tasks/{task_id}", summary="Update Task", description="Updates an existing task")
def update_task(task_id: int, task: TaskUpdate):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    row = cursor.fetchone()
    if row is None:
        conn.close()
        return JSONResponse(status_code=404, content={"error": f"Task {task_id} not found"})
    
    if task.title is not None:
        if task.title.strip() == "":
            conn.close()
            return JSONResponse(status_code=400, content={"error": "Title cannot be empty"})
        cursor.execute("UPDATE tasks SET title = ? WHERE id = ?", (task.title, task_id))
    
    if task.done is not None:
        done_int = 1 if task.done else 0
        cursor.execute("UPDATE tasks SET done = ? WHERE id = ?", (done_int, task_id))
    
    conn.commit()
    conn.close()
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    updated = cursor.fetchone()
    conn.close()
    return {"id": updated["id"], "title": updated["title"], "done": bool(updated["done"])}

@app.delete("/tasks/{task_id}", summary="Delete Task", description="Deletes an existing task")
# This endpoint allows deleting an existing task based on the provided task ID. If the task is not found, it returns a 404 error. Upon successful deletion, it returns a 204 status code with no content.")
@app.delete("/tasks/{task_id}", summary="Delete Task", description="Deletes an existing task")
def delete_task(task_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    row = cursor.fetchone()
    if row is None:
        conn.close()
        return JSONResponse(status_code=404, content={"error": f"Task {task_id} not found"})
    
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    return JSONResponse(status_code=204, content={})

