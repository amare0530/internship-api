import pandas as pd
import os
import random

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CSV_PATH = os.path.join(BASE_DIR, "dataAPPsource.csv")

try:
    df = pd.read_csv(CSV_PATH).fillna("")
    print(f"CSV Loaded: {len(df)} rows")
except:
    df = pd.DataFrame()

def format_job(row, index):
    return {
        "id": index + 1,
        "title": str(row.get("OCCU_DESC", "")),
        "company": str(row.get("COMPNAME", "")),
        "location": str(row.get("CITYNAME", "")),
        "skills": [str(row.get("EDGRDESC", "不拘")), "實習"],
        "description": str(row.get("JOB_DETAIL", ""))[:100],
        "url": str(row.get("URL_QUERY", ""))
    }

# 修正：加入 keyword 參數，讓「搜尋」功能動起來！
def fetch_job_list(skip: int = 0, limit: int = 10, keyword: str = None):
    data = df
    if keyword:
        # 在職稱或公司名稱中搜尋關鍵字
        mask = data['OCCU_DESC'].str.contains(keyword, na=False) | data['COMPNAME'].str.contains(keyword, na=False)
        data = data[mask]
    
    subset = data.iloc[skip : skip + limit]
    return [format_job(row, i) for i, row in subset.iterrows()]

def fetch_swipe_jobs(limit: int = 10):
    if df.empty: return []
    sample_indices = random.sample(range(len(df)), min(limit, len(df)))
    return [format_job(df.iloc[i], i) for i in sample_indices]

# ... 其餘 record_like 等維持原樣 ...