import streamlit as st
from services.research_service import get_reports, get_report
from utils.session import is_logged_in, get_token, logout

st.set_page_config(
    page_title="My Reports — ResearchMind",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    .stButton > button { border-radius: 8px; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

if not is_logged_in():
    st.switch_page("pages/1_login.py")

# --- Header ---
col1, col2, col3 = st.columns([3, 1, 1])
with col1:
    st.markdown("## 📚 My Reports")
with col2:
    if st.button("🔬 New Research", use_container_width=True, type="primary"):
        st.switch_page("pages/3_research.py")
with col3:
    if st.button("🚪 Logout", use_container_width=True):
        logout()
        st.switch_page("pages/1_login.py")

st.markdown("---")

# --- Load Reports ---
with st.spinner("Loading your reports..."):
    reports = get_reports(get_token())

if not reports:
    st.info("📭 No reports yet. Start your first research!")
    if st.button("Start Research →", type="primary"):
        st.switch_page("pages/3_research.py")
else:
    st.markdown(f"**{len(reports)} report(s) found**")
    st.markdown("<br>", unsafe_allow_html=True)
    
    for report in reports:
        with st.expander(f"📄 {report['topic']} — {report['created_at'][:10]}"):
            if st.button("View Full Report", key=f"view_{report['id']}", use_container_width=True):
                with st.spinner("Loading..."):
                    full = get_report(get_token(), report["id"])
                if full:
                    st.markdown(full.get("final_report", ""))
                else:
                    st.error("Could not load report.")