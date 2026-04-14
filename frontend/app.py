import streamlit as st
from utils.session import is_logged_in

st.set_page_config(
    page_title="ResearchMind",
    page_icon="🔬",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- Custom CSS ---
st.markdown("""
<style>
    .main-title {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0;
    }
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.2s;
    }
</style>
""", unsafe_allow_html=True)

if is_logged_in():
    st.switch_page("pages/3_research.py")

st.markdown('<h1 class="main-title">🔬 ResearchMind</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">AI-powered Literature Review Generator</p>', unsafe_allow_html=True)

st.markdown("---")

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("### Welcome")
    st.markdown("Generate comprehensive literature reviews powered by AI in minutes.")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("🔑 Login", use_container_width=True, type="primary"):
        st.switch_page("pages/1_login.py")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("📝 Create Account", use_container_width=True):
        st.switch_page("pages/2_register.py")