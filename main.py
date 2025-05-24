from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import csv
from typing import List, Optional
from pathlib import Path

app = FastAPI()

# Enable CORS to allow GET requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)

DATA_FILE = Path("students.csv")

def read_students() -> List[dict]:
    with DATA_FILE.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return [{"studentId": int(row["studentId"]), "class": row["class"]} for row in reader]

@app.get("/api")
async def get_students(class_: Optional[List[str]] = Query(None, alias="class")):
    students = read_students()
    if class_:
        students = [s for s in students if s["class"] in class_]
    return {"students": students}
