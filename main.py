# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# 匯入新的路由模組
from routers import job

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

# 註冊路由：所有在 job.py 中的路由都會被加入
app.include_router(job.router, prefix="/jobs")