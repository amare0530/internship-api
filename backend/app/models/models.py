from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# 【重要】請確認您的資料表名稱是否為 'job'
class Job(Base):
    __tablename__ = "job"

    # 欄位定義必須與您匯入 20 萬筆數據的資料表結構匹配
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    company = Column(String)
    location = Column(String)
    skills = Column(String)
    
    # 幫助 FastAPI 將資料庫物件轉換成 JSON
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}