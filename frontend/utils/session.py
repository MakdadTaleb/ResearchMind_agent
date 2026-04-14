import streamlit as st


def save_token(token: str):
    st.session_state["token"] = token
    st.query_params["token"] = token


def get_token() -> str:
    # أولاً من session_state
    if "token" in st.session_state and st.session_state["token"]:
        return st.session_state["token"]
    # ثانياً من query_params عند الـ refresh
    token = st.query_params.get("token", None)
    if token:
        st.session_state["token"] = token
    return token


def is_logged_in() -> bool:
    return get_token() is not None


def logout():
    st.session_state.clear()
    st.query_params.clear()