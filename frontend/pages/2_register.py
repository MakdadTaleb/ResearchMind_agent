import streamlit as st
from services.auth_service import register
from utils.session import is_logged_in

if "token" not in st.session_state:
    st.session_state["token"] = None

st.set_page_config(page_title="Register — ResearchMind", page_icon="📝", layout="centered")

st.markdown("""
<style>
    .block-container { max-width: 450px; margin: auto; padding-top: 3rem; }
    .stButton > button { border-radius: 8px; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

if is_logged_in():
    st.switch_page("pages/3_research.py")

st.markdown("## 📝 Create Account")
st.markdown("Join ResearchMind today")
st.markdown("---")

email = st.text_input("Email", placeholder="your@email.com")
password = st.text_input("Password", type="password", placeholder="Min. 8 characters")
confirm_password = st.text_input("Confirm Password", type="password", placeholder="••••••••")

st.markdown("<br>", unsafe_allow_html=True)

if st.button("Create Account", use_container_width=True, type="primary"):
    if not email or not password or not confirm_password:
        st.error("⚠️ Please fill all fields.")
    elif password != confirm_password:
        st.error("❌ Passwords do not match.")
    elif len(password) < 8:
        st.error("❌ Password must be at least 8 characters.")
    else:
        with st.spinner("Creating account..."):
            result = register(email, password)
        
        if "error" in result:
            st.error(f"❌ {result['error']}")
        else:
            st.success("✅ Account created successfully! Please login.")
            st.switch_page("pages/1_login.py")

st.markdown("---")
st.markdown("Already have an account?")
if st.button("Login →", use_container_width=True):
    st.switch_page("pages/1_login.py")