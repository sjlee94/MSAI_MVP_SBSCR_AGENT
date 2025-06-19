import os
from dotenv import load_dotenv
from openai import AzureOpenAI

def load_env():
    load_dotenv()
    return {
        "openai_endpoint": os.getenv("OPENAI_ENDPOINT"),
        "openai_api_key": os.getenv("OPENAI_API_KEY"),
        "chat_model": os.getenv("CHAT_MODEL"),
        "embedding_model": os.getenv("EMBEDDING_MODEL"),
        "search_endpoint": os.getenv("SEARCH_ENDPOINT"),
        "search_api_key": os.getenv("SEARCH_API_KEY"),
        "index_name": os.getenv("INDEX_NAME"),
        "pred_index_name": os.getenv("PRED_INDEX_NAME"),
        "grafana_endpoint": os.getenv("GRAFANA_ENDPOINT"),
    }

def init_chat_client(openai_endpoint, openai_api_key):
    return AzureOpenAI(
        api_version="2024-12-01-preview",
        azure_endpoint=openai_endpoint,
        api_key=openai_api_key,
    )