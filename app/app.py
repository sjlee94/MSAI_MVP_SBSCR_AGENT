import streamlit as st
import random

st.title("Hello, Streamlit!")
st.write("This is a simple Streamlit app to demonstrate the setup.")

# 임의의 숫자 생성
if 'random_number' not in st.session_state:
    st.session_state.random_number = random.randint(1, 100)

# 사용자 입력
guess = st.number_input("Enter your guess (1-100):", min_value=1, max_value=100, step=1)

# 결과 확인 버튼
if st.button("Check"):
    if guess == st.session_state.random_number:
        st.success("Congratulations! You guessed the correct number!")
        # 새로운 숫자 생성
        st.session_state.random_number = random.randint(1, 100)
    elif guess < st.session_state.random_number:
        st.info("Try a higher number!")
    else:
        st.info("Try a lower number!")