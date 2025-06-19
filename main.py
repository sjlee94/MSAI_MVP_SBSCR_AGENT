import os
from dotenv import load_dotenv
from openai import AzureOpenAI # Azure openai로 활용할 경우 OpenAI 대신 AzureOpenAI를 import합니다.
import streamlit as st
import streamlit.components.v1 as components  # 추가
import pandas as pd
from io import StringIO
from azure.storage.blob import BlobServiceClient

from message_utils import init_messages
from blob_utils import load_data_from_blob

load_dotenv()  # Load environment variables from .env file

# Get environment variables
openai_endpoint = os.getenv("OPENAI_ENDPOINT")
openai_api_key = os.getenv("OPENAI_API_KEY")
chat_model = os.getenv("CHAT_MODEL")
embedding_model = os.getenv("EMBEDDING_MODEL")
search_endpoint = os.getenv("SEARCH_ENDPOINT")
search_api_key = os.getenv("SEARCH_API_KEY")
index_name = os.getenv("INDEX_NAME")

# initialize Azure OpenAI client
chat_client = AzureOpenAI(
    api_version="2024-12-01-preview",
    azure_endpoint=openai_endpoint,
    api_key=openai_api_key,
)

st.set_page_config(layout="wide")

init_messages()  # Initialize messages in session state

# if "messages" not in st.session_state:
#     # initialize prompt with system message
#     st.session_state.messages = [
#         {
#             "role": "system",
#             "content": """You are an agent that summarizes and explains subscriber performance data, 
#                         or provides detailed explanations about pricing plans."""
#         },
#     ]

def get_openai_response(messages):
    # Additional parameters to apply RAG pattern using the AI Search index
    if use_rag:
        rag_params = {
            "data_sources": [
                {
                    # he following params are used to search the index
                    "type": "azure_search",
                    "parameters": {
                        "endpoint": search_endpoint,
                        "index_name": index_name,
                        "authentication": {
                            "type": "api_key",
                            "key": search_api_key,
                        },
                        # The following params are used to vectorize the query
                        "query_type": "vector",
                        "embedding_dependency": {
                            "type": "deployment_name",
                            "deployment_name": embedding_model,
                        },
                    }
                }
            ],
        }

        #submit the chat reqest with RAG parameters
        response = chat_client.chat.completions.create(
            model=chat_model,
            messages=messages,
            extra_body=rag_params,  # Include RAG parameters
        )
    
    # If RAG is not used, just send the messages    
    else:
        response = chat_client.chat.completions.create(
            model=chat_model,
            messages=messages,
        )

    conpletion = response.choices[0].message.content
    return conpletion
    
# Handle user input
user_input = st.chat_input("질문을 입력하세요")    
    
# space devide for user input
col1, col2 = st.columns([2, 1])

with col1:
    st.header("월 가입자 현황")
    
    df = load_data_from_blob()
    st.markdown("CSV Viewer")
    st.dataframe(df)

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
        
with col2:
    st.header("가입자 실적 예측 요약 Agent")
    st.markdown("가입자 실적 익월 예측 및 이를 통한 Insights를 제공합니다.  \n"
            "또한, 모바일 요금제에 대해 자세한 답변도 드릴 수 있어요.")
    
    if user_input != None:
        # Display message history
        for message in st.session_state.messages[1:]:
            st.chat_message(message["role"]).write(message["content"])
        
        # Save and display user message
        st.session_state.messages.append({"role": "user", "content": user_input})
        # user_message
        st.chat_message("user").write(user_input)
        
        # 특정 키워드가 포함되어 있으면 RAG 사용
        rag_keywords = ["요금제", "요금", "플랜", "plan", "가격", "price"]
        use_rag = any(keyword in user_input for keyword in rag_keywords)
        
        # Generate and display assistant response
        with st.spinner("응답을 기다리는 중..."):
            assistant_response = get_openai_response(st.session_state.messages)
        st.session_state.messages.append({"role": "assistant", "content": assistant_response})
        # assistant_message
        st.chat_message("assistant").write(assistant_response)
        


# 그라파나 대시보드
grafana_endpoint = os.getenv("GRAFANA_ENDPOINT")

st.sidebar.title("📊 추가 정보")

st.sidebar.header("📈 대시보드 보기")
st.sidebar.markdown(f"👉 [Grafana 대시보드 바로가기]({grafana_endpoint})", unsafe_allow_html=True)

