import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import random
from datetime import datetime

# --- 0. 環境設定 ---
load_dotenv() 

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    # 如果 DATABASE_URL 未設定，程式會在此處停止
    raise ValueError("DATABASE_URL 環境變數未設定！請檢查您的 .env 檔案。")

TARGET_ROWS = 200000
# 修正路徑：使用 '../' 指向專案根目錄的 CSV 檔案
BASE_DATA_PATH = "../dataAPPsource.csv" 

# --- 1. 資料擴充功能 (已修正 TypeError) ---

def augment_data_from_csv(base_data_path: str, target_rows: int):
    """
    讀取本地 CSV 數據，並將其擴充到目標筆數。
    """
    print(f"--- 讀取基礎 CSV 檔案：{base_data_path} ---")
    
    try:
        # 使用 UTF-8 編碼讀取 CSV
        base_df = pd.read_csv(base_data_path, encoding='utf-8')
    except FileNotFoundError:
        # 當找不到檔案時拋出錯誤
        raise FileNotFoundError(f"錯誤：找不到基礎 CSV 檔案 {base_data_path}，請確認檔案路徑。")
    except Exception as e:
        print(f"讀取 CSV 發生錯誤：{e}")
        return None

    initial_count = len(base_df)
    print(f"✅ 成功讀取 {initial_count} 筆基礎數據。")
    
    # ------------------ 薪資欄位類型修正 ------------------
    # 將薪資欄位轉換為數字，非數字值（如'面議'）轉為 NaN，再將 NaN 轉為 0
    base_df['NT_L'] = pd.to_numeric(base_df['NT_L'], errors='coerce').fillna(0).astype(int)
    base_df['NT_U'] = pd.to_numeric(base_df['NT_U'], errors='coerce').fillna(0).astype(int)
    # ----------------------------------------------------------------

    if initial_count >= target_rows:
        return base_df.head(target_rows)

    # 計算需要複製的次數以達到目標筆數
    replication_factor = (target_rows // initial_count) + 1
    
    # 擴充數據的隨機變數列表
    common_cities = ['台北市', '新北市', '桃園市', '台中市', '高雄市', '台南市', '新竹市']
    experience_levels = ['無', '1年以上', '2年以上', '3年以上', '5年以上']
    salary_adjustments = [-1000, 0, 1000, 2000, 3000, 5000, 10000]

    augmented_list = []
    
    for i in range(replication_factor):
        temp_df = base_df.copy()
        
        # 隨機調整薪資
        adj = random.choice(salary_adjustments)
        temp_df['NT_L'] = temp_df['NT_L'] + adj
        temp_df['NT_U'] = temp_df['NT_U'] + adj
        temp_df['NT_L'] = temp_df['NT_L'].apply(lambda x: max(0, x)) # 確保最低薪資不為負
        
        # 隨機調整地點
        temp_df['CITYNAME'] = [random.choice(common_cities) for _ in range(len(temp_df))]
        
        # 隨機調整經驗
        temp_df['EXPERIENCE'] = [random.choice(experience_levels) for _ in range(len(temp_df))]
        
        # 輕微修改公司名稱以區分複製的數據
        temp_df['COMPNAME'] = temp_df['COMPNAME'].astype(str) + " (" + str(i % 5) + ")"
        
        augmented_list.append(temp_df)
        
    final_df = pd.concat(augmented_list, ignore_index=True)
    
    print(f"✅ 數據擴充完成，總筆數：{len(final_df)} 筆。")
    # 只取目標筆數
    return final_df.head(target_rows)

# --- 2. 資料庫匯入功能 (已優化分批寫入) ---

def import_data_to_db(df: pd.DataFrame, table_name="jobs"):
    """
    將 DataFrame 數據匯入 PostgreSQL 資料庫，使用 chunksize 分批寫入。
    """
    if df is None or df.empty:
        print("沒有數據可匯入，操作終止。")
        return
    
    # ----------------------------------------------------
    # 執行欄位清理與重命名
    # ----------------------------------------------------
    
    # 數據欄位對應（重命名為資料庫表格欄位名稱）
    df_clean = df.rename(columns={
        'OCCU_DESC': 'title',      
        'JOB_DETAIL': 'detail',    
        'COMPNAME': 'company',     
        'NT_L': 'salary_min',      
        'NT_U': 'salary_max',      
        'CITYNAME': 'location',    
        'EXPERIENCE': 'experience', 
    })
    
    # 增加模擬的 AI 相關欄位
    df_clean['match_score'] = [random.uniform(0.5, 0.95) for _ in range(len(df_clean))]
    df_clean['ai_risk_level'] = [random.choice(['Low', 'Medium', 'High']) for _ in range(len(df_clean))]
    
    # 最終只保留需要的欄位
    cols_to_keep = ['title', 'detail', 'company', 'salary_min', 'salary_max', 'location', 'experience', 'match_score', 'ai_risk_level']
    df_to_import = df_clean.filter(items=cols_to_keep)
    
    # ----------------------------------------------------

    print(f"--- 開始匯入 {len(df_to_import)} 筆數據到資料庫，分批寫入中... ---")
    
    try:
        # 建立資料庫連線引擎
        engine = create_engine(DATABASE_URL)
        
        # 使用 chunksize 分批寫入，降低資料庫壓力。if_exists='replace' 會重建表格。
        df_to_import.to_sql(
            table_name, 
            engine, 
            if_exists='replace', 
            index=False, 
            method='multi',
            chunksize=5000 
        )
        print(f"✅ 數據成功匯入表格 '{table_name}'！總筆數：{len(df_to_import)}")
        
    except Exception as e:
        print(f"❌ 資料庫匯入失敗！錯誤：{e}")
        
# --- 3. 主執行區塊 ---

if __name__ == "__main__":
    final_data_df = augment_data_from_csv(BASE_DATA_PATH, TARGET_ROWS)
    
    if final_data_df is not None:
        import_data_to_db(final_data_df, table_name="jobs")