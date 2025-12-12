<<<<<<< HEAD
# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Internship API - Mock")

=======
# main.py - Internship API (demo)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(title="Internship API - Demo")

# 開發階段允許所有 CORS（生產要鎖 domain）
>>>>>>> 2946b70bd3ed778a6e5f4dfa8bd2a80ef0fbd4fa
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

<<<<<<< HEAD
@app.get("/")
def root():
    return {"status":"Server OK","message":"Internship API (mock) running"}

@app.get("/jobs")
def jobs(limit: int = 10, offset: int = 0, q: str = None):
    sample = [
        {"id":1,"title":"資料分析實習生","company":"數據坊","location":"遠端"},
        {"id":2,"title":"前端實習生","company":"XYZ 新創","location":"台北"}
    ]
    return {"count": len(sample), "jobs": sample}

@app.post("/like")
def like(payload: dict):
    return {"ok": True, "payload": payload}

@app.post("/match")
def match(payload: dict):
    return {"user_id": payload.get("user_id"), "matches":[{"job_id":1,"score":0.89,"title":"資料分析實習生","company":"數據坊"}]}

# Optional: simple health route for readiness checks
@app.get("/health")
def health():
    return {"status":"ok"}
=======
fake_jobs = [
    {"id": 1, "title": "行銷實習生", "company": "ABC 公司", "location": "台北", "skills": ["行銷", "企劃"]},
    {"id": 2, "title": "前端工程實習生", "company": "XYZ 新創", "location": "台中", "skills": ["HTML", "CSS", "JavaScript"]},
    {"id": 3, "title": "資料分析實習生", "company": "數據坊", "location": "遠端", "skills": ["Python", "Pandas", "SQL"]},
]

@app.get("/")
def root():
    return {"status": "Server OK", "message": "Internship API is running"}

@app.get("/jobs")
def get_jobs(limit: int = 10):
    # 未配置 DB 時回傳假資料
    return {"jobs": fake_jobs[:limit], "count": len(fake_jobs[:limit])}

@app.post("/like")
def like_job(user_id: int, job_id: int):
    # demo：僅回傳收到的 like（之後會寫入 DB）
    return {"status": "ok", "user_id": user_id, "job_id": job_id, "message": "liked recorded (demo)"}
>>>>>>> 2946b70bd3ed778a6e5f4dfa8bd2a80ef0fbd4fa
