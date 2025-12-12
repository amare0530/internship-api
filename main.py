from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(title="Internship API - Demo")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 為了方便測試，使用虛擬數據 (fake_jobs)
fake_jobs = [
    {"id": 1, "title": "行銷實習生", "company": "ABC 公司", "location": "台北", "skills": ["行銷", "企劃"]},
    {"id": 2, "title": "前端工程實習生", "company": "XYZ 新創", "location": "台中", "skills": ["HTML", "CSS", "JavaScript"]},
    {"id": 3, "title": "資料分析實習生", "company": "數據坊", "location": "遠端", "skills": ["Python", "Pandas", "SQL"]},
]

@app.get("/")
def root():
    return {"status": "Server OK", "message": "Internship API is running"}

# 1. 【原有的】職缺列表 (用於搜尋或列表頁)
@app.get("/jobs")
def get_jobs(limit: int = 10):
    # Returns the list of jobs for the job list page
    return {"jobs": fake_jobs[:limit], "count": len(fake_jobs[:limit])}


# *******************************************************************
# 【新增/修正】路由：確保與 Flutter App 的 job_service.dart 匹配
# *******************************************************************

# 2. 【新增】滑卡職缺列表 (修復 Flutter App 崩潰的關鍵)
@app.get("/jobs/swipe")
def get_swipe_jobs(limit: int = 10):
    # Returns the list of jobs for the swiping feature
    return fake_jobs[:limit]

# 3. 【新增】根據 ID 獲取單一職缺詳情
@app.get("/jobs/{job_id}")
def get_job_by_id(job_id: int):
    try:
        # Search for the job in the fake data
        job = next(job for job in fake_jobs if job["id"] == job_id)
        return job
    except StopIteration:
        raise HTTPException(status_code=404, detail="Job not found")

# 4. 【新增】喜歡職缺
@app.post("/jobs/{job_id}/like")
def like_job_by_id(job_id: int):
    # 這是 Demo 終點，在真實應用中，會更新資料庫。
    return {"status": "ok", "job_id": job_id, "message": f"Job {job_id} liked recorded (demo)"}

# 5. 【新增】不喜歡職缺
@app.post("/jobs/{job_id}/dislike")
def dislike_job_by_id(job_id: int):
    # 這是 Demo 終點，在真實應用中，會更新資料庫。
    return {"status": "ok", "job_id": job_id, "message": f"Job {job_id} disliked recorded (demo)"}