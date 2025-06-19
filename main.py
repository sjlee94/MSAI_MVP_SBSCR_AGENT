import streamlit as st
import streamlit.components.v1 as components

from src.utils.env_utils import load_env, init_chat_client
from src.utils.message_utils import init_messages
from src.utils.blob_utils import load_data_from_blob
from src.utils.openai_utils import get_agent_response
from src.utils.grafana_utils import render_grafana_sidebar

def main():
    env = load_env()  # Load environment variables from .env file
    chat_client = init_chat_client(env["openai_endpoint"], env["openai_api_key"])

    st.set_page_config(layout="wide")
    render_grafana_sidebar(env["grafana_endpoint"])

    # 화면 표시용 데이터프레임
    df = load_data_from_blob()
    if "년월" in df.columns and "가입자수" in df.columns:
        monthly_df = df.groupby("년월")["가입자수"].sum().reset_index()
        monthly_df = monthly_df.rename(columns={"년월": "년월", "가입자수": "전체 가입자수"})
    else:
        monthly_df = None

    # 시스템 프롬프트용 메시지 초기화 (별도 데이터프레임 사용)
    init_messages()

    # 외부 CSS 파일 불러오기
    with open("src/static/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    # Handle user input
    user_input = st.chat_input("질문을 입력하세요")    
    
    # space devide for user input
    col1, col2 = st.columns([2, 1], gap="large")

    with col1:
        st.subheader("월 가입자 현황")
        container = st.container()
        with container:
            if monthly_df is not None:
                st.markdown("월별 전체 가입자수")
                st.dataframe(monthly_df, hide_index=True, width=300)
            else:
                st.warning("데이터프레임에 '년월' 또는 '가입자수' 컬럼이 없습니다.")
            st.markdown("CSV Viewer")
            st.dataframe(df, height=290)

    with col2:
        st.subheader("가입자 실적 예측 요약 Agent")
        container2 = st.container()
        with container2:
            st.markdown(
                "가입자 실적 익월 예측 및 이를 통한 Insights를 제공합니다.  \n"
                "또한, 모바일 요금제에 대해 자세한 답변도 드릴 수 있어요."
            )
            if user_input is not None:
                st.session_state.messages.append({"role": "user", "content": user_input})
                for message in st.session_state.messages[1:]:
                    st.chat_message(message["role"]).write(message["content"])
                with st.spinner("응답을 기다리는 중..."):
                    assistant_response = get_agent_response(st.session_state.messages, env, chat_client)
                st.session_state.messages.append({"role": "assistant", "content": assistant_response})
                st.chat_message("assistant").write(assistant_response)

if __name__ == "__main__":
    main()

