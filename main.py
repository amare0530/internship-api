from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
# --- 【重要】請確保這裡的 import 檔案名稱 (db_service) 是正確的！ ---
from . import db_service

app = FastAPI(title="Internship API - JobTruth")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "Server OK", "message": "Internship API is running (REAL DATA CONNECTED)"}

# 1. 職缺列表 (用於搜尋或列表頁)
@app.get("/jobs")
def get_jobs(limit: int = 10):
    # **替換為真實資料庫讀取邏輯**
    jobs = db_service.fetch_job_list(limit=limit)
    return {"jobs": jobs, "count": len(jobs)}

# 2. 滑卡職缺列表 (修復 Flutter App 崩潰的關鍵)
@app.get("/jobs/swipe")
def get_swipe_jobs(limit: int = 10):
    # **替換為真實資料庫讀取邏輯**
    jobs = db_service.fetch_swipe_jobs(limit=limit)
    return jobs

# 3. 根據 ID 獲取單一職缺詳情
@app.get("/jobs/{job_id}")
def get_job_by_id(job_id: int):
    # **替換為真實資料庫讀取邏輯**
    job = db_service.fetch_job_by_id(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

# 4. 喜歡職缺
@app.post("/jobs/{job_id}/like")
def like_job_by_id(job_id: int):
    # 這是 Demo 終點，在真實應用中，會更新資料庫。
    db_service.record_like(job_id)
    return {"status": "ok", "job_id": job_id, "message": f"Job {job_id} liked recorded"}

# 5. 不喜歡職缺
@app.post("/jobs/{job_id}/dislike")
def dislike_job_by_id(job_id: int):
    # 這是 Demo 終點，在真實應用中，會更新資料庫。
    db_service.record_dislike(job_id)
    return {"status": "ok", "job_id": job_id, "message": f"Job {job_id} disliked recorded"}