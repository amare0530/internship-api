from app.database import engine
from sqlalchemy import text

print("🚀 測試資料庫連線...")

try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT version();"))
        version = result.fetchone()[0]
        print("✅ PostgreSQL 連線成功！")
        print(f"版本：{version}")
        
        # 測試資料表是否建立
        result = conn.execute(text("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema='public'
        """))
        tables = result.fetchall()
        print(f"\n📊 已建立的資料表：")
        for table in tables:
            print(f"  - {table[0]}")
            
except Exception as e:
    print(f"❌ 發生錯誤：{e}")