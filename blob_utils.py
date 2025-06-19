import os
import pandas as pd
from io import StringIO
from azure.storage.blob import BlobServiceClient

def load_data_from_blob():
    storage_connect_string = os.getenv("STORAGE_CONNECT_STRING")
    container_name = os.getenv("CONTAINER_NAME")
    blob_name = os.getenv("BLOB_NAME")

    blob_service = BlobServiceClient.from_connection_string(storage_connect_string)
    blob_client = blob_service.get_blob_client(container=container_name, blob=blob_name)
    csv_data = blob_client.download_blob().readall().decode("utf-8")
    df = pd.read_csv(StringIO(csv_data))
    return df


    # # blob storage 데이터 추출
    # storage_connect_string = os.getenv("STORAGE_CONNECT_STRING")
    # container_name = os.getenv("CONTAINER_NAME")
    # blob_name = os.getenv("BLOB_NAME")

    # blob_service = BlobServiceClient.from_connection_string(storage_connect_string)
    # blob_client = blob_service.get_blob_client(container=container_name, blob=blob_name)
    # csv_data = blob_client.download_blob().readall().decode("utf-8")

    # # 데이터프레임 생성 및 출력
    # df = pd.read_csv(StringIO(csv_data))
    # print(df.head())  # 데이터프레임의 첫 5행 출력
    # st.subheader("Blob Storage CSV Viewer")
    # st.dataframe(df)