import pandas as pd
from sqlalchemy import create_engine
import pyodbc
import urllib

# 1. CSV 파일 불러오기
df = pd.read_csv('./data/predicted_sbscr_with_m_plus_1.csv')  # 또는 blob에서 불러온 DataFrame

# 데이터 확인
# print(df.head())  

# 2. SQL 연결 문자열
params = pyodbc.connect(
    "Driver={ODBC Driver 18 for SQL Server};"
    "Server=tcp:lsjsqlserver.database.windows.net,1433;"
    "Database=lsjsqldb;"
    "Uid=sjlee"
    "Pwd=1q2w3e4r!;"
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
)

engine = create_engine("mssql+pyodbc:///?odbc_connect={}".format(params))

# 3. 테이블로 업로드 (기존 데이터 덮어쓰기)
df.to_sql("grafana_table", engine, if_exists='replace', index=False)
