import os
import json
import pandas as pd
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient
from utils.blob_utils import load_ml_dataframe

# 환경변수 로드
load_dotenv()
blob_connection_string = os.getenv("STORAGE_CONNECT_STRING")
container_name = os.getenv("ML_CONTAINER_NAME")
blob_file_name = "ml_data_lines.json"  # 파일명도 .jsonl 형식으로 변경

# 컬럼명 매핑
column_map = {
    "년월": "year_month", "고객ID": "customer_id", "성별": "gender",
    "연령대": "age_group", "가입일": "join_date", "해지일": "cancel_date",
    "요금제": "plan", "단말기기종": "device_model", "상태": "status",
    "상태사유": "status_reason", "신용등급": "credit_grade",
    "선택약정여부": "contract_option", "요금제가격": "plan_price",
    "월평균요금": "avg_monthly_fee", "데이터사용량(GB)": "data_usage_gb",
    "가입자수": "subscriber_count", "M+1": "m_plus_1"
}

# 데이터 로드 및 컬럼명 변경
df = load_ml_dataframe().rename(columns=column_map)

# summary 필드 포함한 JSON Lines 문서 생성
def build_json_lines(df):
    lines = []
    for idx, row in df.iterrows():
        doc = {k: (None if pd.isnull(v) else v) for k, v in row.items()}
        doc["id"] = str(idx)
        doc["summary"] = (
            f"{doc.get('year_month', '')}월 기준, 고객 {doc.get('customer_id', '')}은 "
            f"{doc.get('plan', '')} 요금제를 사용 중입니다. "
            f"단말기는 {doc.get('device_model', '')}이며, 상태는 {doc.get('status', '')}입니다. "
            f"월 평균 요금은 {doc.get('avg_monthly_fee', '')}원이고, "
            f"데이터 사용량은 {doc.get('data_usage_gb', '')}GB입니다."
        )
        lines.append(json.dumps(doc, ensure_ascii=False))
    return "\n".join(lines)

# Blob 업로드 함수 (JSON Lines 형식)
def upload_json_lines_to_blob(jsonl_str, connection_string, container, blob_name):
    blob_service = BlobServiceClient.from_connection_string(connection_string)
    blob_client = blob_service.get_blob_client(container=container, blob=blob_name)

    blob_client.upload_blob(jsonl_str, overwrite=True)
    print(f"✅ JSON Lines 파일이 Blob에 업로드되었습니다: {blob_name}")

# 실행
if __name__ == "__main__":
    jsonl_data = build_json_lines(df)
    upload_json_lines_to_blob(jsonl_data, blob_connection_string, container_name, blob_file_name)
