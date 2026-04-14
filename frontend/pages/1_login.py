import streamlit as st
from services.auth_service import login
from utils.session import save_token, is_logged_in

if "token" not in st.session_state:
    st.session_state["token"] = None

st.set_page_config(page_title="Login — ResearchMind", page_icon="🔑", layout="centered")

st.markdown("""
<style>
    .block-container { max-width: 450px; margin: auto; padding-top: 3rem; }
    .stButton > button { border-radius: 8px; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

if is_logged_in():
    st.switch_page("pages/3_research.py")

st.markdown("## 🔑 Login")
st.markdown("Welcome back to ResearchMind")
st.markdown("---")

email = st.text_input("Email", placeholder="your@email.com")
password = st.text_input("Password", type="password", placeholder="••••••••")

st.markdown("<br>", unsafe_allow_html=True)

if st.button("Login", use_container_width=True, type="primary"):
    if not email or not password:
        st.error("⚠️ Please fill all fields.")
    else:
        with st.spinner("Logging in..."):
            result = login(email, password)
        
        if "error" in result:
            st.error(f"❌ {result['error']}")
        else:
            st.session_state["token"] = result["access_token"]
            st.success("✅ Logged in successfully!")
            st.switch_page("pages/3_research.py")

st.markdown("---")
st.markdown("Don't have an account?")
if st.button("Create Account →", use_container_width=True):
    st.switch_page("pages/2_register.py")