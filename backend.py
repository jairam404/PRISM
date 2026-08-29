from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
from typing import List

app = FastAPI(title="PRISM Backend API", version="1.0")

# --- Database Setup ---
DB_FILE = "prism_notes.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    # Table for student CRUD operations (managing study notes/formulas)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            subject TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()

# --- Pydantic Models for Request Validation ---
class NoteCreate(BaseModel):
    title: str
    content: str
    subject: str

class NoteUpdate(BaseModel):
    title: str
    content: str
    subject: str

# --- RESTful API Endpoints (CRUD) ---

# 1. CREATE (POST)
@app.post("/notes/", status_code=201)
def create_note(note: NoteCreate):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO notes (title, content, subject) VALUES (?, ?, ?)", 
                   (note.title, note.content, note.subject))
    conn.commit()
    note_id = cursor.lastrowid
    conn.close()
    return {"id": note_id, "message": "Note created successfully", **note.dict()}

# 2. READ ALL (GET)
@app.get("/notes/")
def get_notes():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM notes")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

# 3. READ SINGLE (GET)
@app.get("/notes/{note_id}")
def get_note(note_id: int):
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM notes WHERE id = ?", (note_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Note not found")
    return dict(row)

# 4. UPDATE (PUT)
@app.put("/notes/{note_id}")
def update_note(note_id: int, note: NoteUpdate):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("UPDATE notes SET title = ?, content = ?, subject = ? WHERE id = ?", 
                   (note.title, note.content, note.subject, note_id))
    conn.commit()
    changes = cursor.rowcount
    conn.close()
    if changes == 0:
        raise HTTPException(status_code=404, detail="Note not found")
    return {"id": note_id, "message": "Note updated successfully", **note.dict()}

# 5. DELETE (DELETE)
@app.delete("/notes/{note_id}")
def delete_note(note_id: int):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM notes WHERE id = ?", (note_id,))
    conn.commit()
    changes = cursor.rowcount
    conn.close()
    if changes == 0:
        raise HTTPException(status_code=404, detail="Note not found")
    return {"message": f"Note {note_id} deleted successfully"}