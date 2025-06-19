import streamlit as st

def init_messages():
    if "messages" not in st.session_state:
        # 인덱스 필드명 설명 (영문명: 한글 의미)
        field_desc = (
            "\nHere is a description of the index fields:\n"
            "- year_month: 년월\n"
            "- customer_id: 고객ID\n"
            "- gender: 성별\n"
            "- age_group: 연령대\n"
            "- join_date: 가입일\n"
            "- cancel_date: 해지일\n"
            "- plan: 요금제\n"
            "- device_model: 단말기기종\n"
            "- status: 상태\n"
            "- status_reason: 상태사유\n"
            "- credit_grade: 신용등급\n"
            "- contract_option: 선택약정여부\n"
            "- plan_price: 요금제가격\n"
            "- avg_monthly_fee: 월평균요금\n"
            "- data_usage_gb: 데이터사용량(GB)\n"
            "- subscriber_count: 가입자수\n"
            "- m_plus_1: M+1(익월 가입자수)\n"
            "- summary: 고객 요약 정보\n"
        )
        system_content = (
            "You are an AI agent that explains subscriber performance data and mobile pricing plans."
            "Always use the provided index field descriptions first." 
            "If the information is not available, you must answer using your general knowledge or external information."
            "Never reply that the information is not in the documents; always provide the best possible answer by selecting only the most appropriate and accurate response, and output it without any explanation."
            f"{field_desc}"
        )
        st.session_state.messages = [
            {"role": "system", "content": system_content}
        ]