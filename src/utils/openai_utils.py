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
    print("오픈ai에서: ", index_name)
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

def get_agent_response(messages, env, chat_client):
    """
    INDEX_NAME, PRED_INDEX_NAME 모두 RAG 시도,
    두 답변이 모두 있으면 LLM에게 둘 중 더 적합한 답변을 선택하도록 요청
    """
    index_names = [env.get("index_name"), env.get("pred_index_name")]
    rag_responses = []
    for idx_name in index_names:
        if not idx_name:
            continue
        rag_response = get_openai_response(
            chat_client,
            env["chat_model"],
            env["embedding_model"],
            env["search_endpoint"],
            env["search_api_key"],
            idx_name,
            messages,
            use_rag=True
        )
        if rag_response and rag_response.strip() != "":
            rag_responses.append((idx_name, rag_response.strip()))

    if len(rag_responses) == 1:
        return rag_responses[0][1]
    elif len(rag_responses) == 2:
        # 두 답변이 모두 있을 때 LLM에게 비교 프롬프트로 적합한 답변을 선택하도록 요청
        compare_prompt = [
            {"role": "system", "content": "아래 두 답변 중에서 사용자 질문에 더 적합하고 정확한 답변만 골라서 그대로 출력하세요. 이유 설명 없이 답변만 출력하세요."},
            {"role": "user", "content": f"제안1:\n{rag_responses[0][1]}\n\n제안2:\n{rag_responses[1][1]}"}
        ]
        best_response = get_openai_response(
            chat_client,
            env["chat_model"],
            env["embedding_model"],
            env["search_endpoint"],
            env["search_api_key"],
            env["index_name"],  # 인덱스는 아무거나, 일반 답변처럼 사용
            compare_prompt,
            use_rag=False
        )
        return best_response.strip()

    # 둘 다 없으면 일반 답변
    normal_response = get_openai_response(
        chat_client,
        env["chat_model"],
        env["embedding_model"],
        env["search_endpoint"],
        env["search_api_key"],
        env["index_name"],
        messages,
        use_rag=False
    )
    if normal_response and normal_response.strip() != "":
        return normal_response

    return "죄송합니다. 해당 질문에 대해서는 제공된 문서에 존재하지 않거나 현재는 답변 드릴 수 없습니다."