import os
from openai import AzureOpenAI

def get_openai_client():
    openai_endpoint = os.getenv("OPENAI_ENDPOINT")
    openai_api_key = os.getenv("OPENAI_API_KEY")
    return AzureOpenAI(
        api_version="2024-12-01-preview",
        azure_endpoint=openai_endpoint,
        api_key=openai_api_key,
    )

def get_openai_response(chat_client, chat_model, embedding_model, search_endpoint, search_api_key, index_name, messages, use_rag):
    if use_rag:
        rag_params = {
            "data_sources": [
                {
                    "type": "azure_search",
                    "parameters": {
                        "endpoint": search_endpoint,
                        "index_name": index_name,
                        "authentication": {
                            "type": "api_key",
                            "key": search_api_key,
                        },
                        "query_type": "vector",
                        "embedding_dependency": {
                            "type": "deployment_name",
                            "deployment_name": embedding_model,
                        },
                    }
                }
            ],
        }
        response = chat_client.chat.completions.create(
            model=chat_model,
            messages=messages,
            extra_body=rag_params,
        )
    else:
        response = chat_client.chat.completions.create(
            model=chat_model,
            messages=messages,
        )
    return response.choices[0].message.content