from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(title="Internship API - Demo")

# 開發階段允許所有 CORS（生產要鎖 domain）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

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
