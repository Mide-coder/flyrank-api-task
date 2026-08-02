from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
import os
import psycopg
from dotenv import load_dotenv

env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
load_dotenv(dotenv_path=env_path)
DATABASE_URL = os.getenv("DATABASE_URL")
print(f"Loaded DATABASE_URL: {DATABASE_URL is not None}")

def get_db_connection():
    return psycopg.connect(DATABASE_URL)

def init_db():
    print("Initializing database...")
    conn = get_db_connection()
    cursor = conn.cursor()
    
    print("Creating tasks table if it doesn't exist...")
    cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (
        id SERIAL PRIMARY KEY,
        title TEXT NOT NULL,
        done BOOLEAN DEFAULT FALSE
    )''')
    
    print("Checking for existing tasks...")
    cursor.execute("SELECT COUNT(*) FROM tasks")
    count = cursor.fetchone()[0]
    print(f"Number of tasks: {count}")
    
    if count == 0:
        print("Inserting default tasks...")
        cursor.execute("INSERT INTO tasks (title, done) VALUES (%s, %s)", ("Code", True))
        cursor.execute("INSERT INTO tasks (title, done) VALUES (%s, %s)", ("Test", False))
        cursor.execute("INSERT INTO tasks (title, done) VALUES (%s, %s)", ("Deploy", False))
    
    conn.commit()
    cursor.close()
    conn.close()
    print("Database initialization complete.")

init_db()

class TaskCreate(BaseModel):
    title: str | None = None
    done: bool | None = None

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None

app = FastAPI()

@app.get("/", summary="API Root")
def read_root():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/", "/health", "/tasks", "/tasks/{id}"]
    }

@app.get("/health", summary="Health Check")
def health_check():
    return {"status": "ok"}

@app.get("/tasks", summary="Get All Tasks")
def get_tasks():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    rows = cursor.fetchall()
    conn.close()
    task_list = [
        {"id": row[0], "title": row[1], "done": row[2]} for row in rows
    ]
    return task_list

@app.get("/tasks/{task_id}", summary="Get Task by ID")
def get_task(task_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
    row = cursor.fetchone()
    conn.close()
    if row is None:
        return JSONResponse(status_code=404, content={"error": f"Task {task_id} not found"})
    return {"id": row[0], "title": row[1], "done": row[2]}

@app.post("/tasks", summary="Create Task")
def create_task(task: TaskCreate):
    if not task.title or task.title.strip() == "":
        return JSONResponse(status_code=400, content={"error": "Title is required"})
    
    done_val = True if task.done else False 
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (title, done) VALUES (%s, %s) RETURNING id", (task.title, done_val))
    new_task_id = cursor.fetchone()[0]
    conn.commit()
    conn.close()

    return JSONResponse(status_code=201, content={"id": new_task_id, "title": task.title, "done": task.done if task.done is not None else False})

@app.put("/tasks/{task_id}", summary="Update Task")
def update_task(task_id: int, task: TaskUpdate):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
    row = cursor.fetchone()
    if row is None:
        conn.close()
        return JSONResponse(status_code=404, content={"error": f"Task {task_id} not found"})
    
    if task.title is not None:
        if task.title.strip() == "":
            conn.close()
            return JSONResponse(status_code=400, content={"error": "Title cannot be empty"})
        cursor.execute("UPDATE tasks SET title = %s WHERE id = %s", (task.title, task_id))
    
    if task.done is not None:
        done_val = True if task.done else False
        cursor.execute("UPDATE tasks SET done = %s WHERE id = %s", (done_val, task_id))
    
    conn.commit()
    conn.close()
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
    updated = cursor.fetchone()
    conn.close()
    return {"id": updated[0], "title": updated[1], "done": updated[2]}

@app.delete("/tasks/{task_id}", summary="Delete Task")
def delete_task(task_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
    row = cursor.fetchone()
    if row is None:
        conn.close()
        return JSONResponse(status_code=404, content={"error": f"Task {task_id} not found"})
    
    cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
    conn.commit()
    conn.close()
    return JSONResponse(status_code=204, content={})