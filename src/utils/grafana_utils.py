import streamlit as st

def render_grafana_sidebar(grafana_endpoint):
    st.sidebar.title("📊 추가 정보")
    st.sidebar.header("📈 대시보드 보기")
    st.sidebar.markdown(f"👉 [Grafana 대시보드 바로가기]({grafana_endpoint})", unsafe_allow_html=True)