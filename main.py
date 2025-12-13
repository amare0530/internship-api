from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
# --- 【重要】確保這是您後端專案中 database 檔案的正確匯入路徑 ---
from app import database # 假設 database.py 在 app 資料夾內

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

# ----------------------------------------------------
# 1. 職缺列表 (用於搜尋、列表和滑卡)
# 整合了滑卡的分頁功能 (skip=0, limit=10)
# ----------------------------------------------------
@app.get("/jobs")
def get_jobs(skip: int = 0, limit: int = 10): 
    # **調用 database.py 中的函數**
    # 這裡的 database.fetch_job_list 必須能接受 skip 和 limit 參數
    jobs = database.fetch_job_list(skip=skip, limit=limit)
    return {"jobs": jobs, "count": len(jobs)}

# --- 2. 移除 /jobs/swipe 路由，避免衝突 ---
# 舊的 /jobs/swipe 路由已移除，因為前端已改為 /jobs?skip=0&limit=10

# ----------------------------------------------------
# 3. 根據 ID 獲取單一職缺詳情
# ----------------------------------------------------
@app.get("/jobs/{job_id}")
def get_job_by_id(job_id: int):
    # **調用 database.py 中的函數**
    job = database.fetch_job_by_id(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

# ----------------------------------------------------
# 4. 喜歡職缺 (POST /jobs/1/like)
# 5. 不喜歡職缺 (POST /jobs/1/dislike)
# 將這兩個 POST 路由放在後面，減少與 /jobs/{job_id} GET 路由的衝突
# ----------------------------------------------------
@app.post("/jobs/{job_id}/like")
def like_job_by_id(job_id: int):
    # **調用 database.py 中的函數**
    database.record_like(job_id)
    return {"status": "ok", "job_id": job_id, "message": f"Job {job_id} liked recorded"}

@app.post("/jobs/{job_id}/dislike")
def dislike_job_by_id(job_id: int):
    # **調用 database.py 中的函數**
    database.record_dislike(job_id)
    return {"status": "ok", "job_id": job_id, "message": f"Job {job_id} disliked recorded"}