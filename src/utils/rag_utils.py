def check_use_rag(user_input):
    rag_keywords = ["요금제", "요금", "플랜", "plan", "가격", "price"]
    return any(keyword in user_input for keyword in rag_keywords)