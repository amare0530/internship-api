# routers/job.py
from fastapi import APIRouter, HTTPException
from app import database

# 設置 router 的標籤 (tags)，讓 FastAPI 知道這些路由屬於 'Jobs'
router = APIRouter(tags=["Jobs"])


# 1. 職缺列表 (URL 將是 /jobs)
@router.get("/") 
def get_jobs(skip: int = 0, limit: int = 10): 
    jobs = database.fetch_job_list(skip=skip, limit=limit)
    return {"jobs": jobs, "count": len(jobs)}

# 2. 根據 ID 獲取單一職缺詳情 (URL 將是 /jobs/{job_id})
@router.get("/{job_id}") 
def get_job_by_id(job_id: int):
    job = database.fetch_job_by_id(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

# 3. 喜歡職缺 (POST /jobs/{job_id}/like)
@router.post("/{job_id}/like")
def like_job_by_id(job_id: int):
    database.record_like(job_id)
    return {"status": "ok", "job_id": job_id, "message": f"Job {job_id} liked recorded"}

# 4. 不喜歡職缺 (POST /jobs/{job_id}/dislike)
@router.post("/{job_id}/dislike")
def dislike_job_by_id(job_id: int):
    database.record_dislike(job_id)
    return {"status": "ok", "job_id": job_id, "message": f"Job {job_id} disliked recorded"}