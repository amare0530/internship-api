import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
# 匯入我們剛剛在 models.py 定義的模型
from .models import Job

# 1. 配置資料庫連線
# Render 會自動將 PostgreSQL 連線字串設置在 DATABASE_URL 環境變數中
DATABASE_URL = os.environ.get("DATABASE_URL")

# 建立 SQLAlchemy Engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

# 建立 Session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 獲取資料庫 Session 的上下文管理器
@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- 2. CRUD 函數：供 main.py 調用 ---

# 1. 獲取列表職缺 (Get Jobs List)
def fetch_job_list(limit: int = 10):
    with get_db() as db:
        jobs = db.query(Job).limit(limit).all()
        return [job.to_dict() for job in jobs]

# 2. 獲取滑卡職缺 (Get Swipe Jobs)
def fetch_swipe_jobs(limit: int = 10):
    with get_db() as db:
        jobs = db.query(Job).order_by(Job.id).limit(limit).all()
        return [job.to_dict() for job in jobs]

# 3. 根據 ID 獲取單一職缺詳情
def fetch_job_by_id(job_id: int):
    with get_db() as db:
        job = db.query(Job).filter(Job.id == job_id).first()
        return job.to_dict() if job else None

# 4. 喜歡職缺 (Like Job) - 模擬操作
def record_like(job_id: int):
    # 這是 Demo 終點
    return True

# 5. 不喜歡職缺 (Dislike Job) - 模擬操作
def record_dislike(job_id: int):
    # 這是 Demo 終點
    return True