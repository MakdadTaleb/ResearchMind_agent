import streamlit as st
from services.research_service import stream_research
from utils.session import is_logged_in, get_token, logout

st.set_page_config(
    page_title="ResearchMind",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    .stButton > button { border-radius: 8px; font-weight: 600; }
    .status-box {
        border-left: 4px solid #667eea;
        padding: 0.5rem 1rem;
        border-radius: 4px;
        margin: 0.3rem 0;
        font-size: 0.95rem;
    }
</style>
""", unsafe_allow_html=True)

if not is_logged_in():
    st.switch_page("pages/1_login.py")

# --- Header ---
col1, col2, col3 = st.columns([3, 1, 1])
with col1:
    st.markdown("## 🔬 ResearchMind")
with col2:
    if st.button("📚 My Reports", use_container_width=True):
        st.switch_page("pages/4_my_reports.py")
with col3:
    if st.button("🚪 Logout", use_container_width=True):
        logout()
        st.switch_page("pages/1_login.py")

st.markdown("---")

# --- Search ---
topic = st.text_input(
    "Research Topic",
    placeholder="e.g. Deep learning for medical imaging",
    label_visibility="collapsed"
)

if st.button("🚀 Generate Literature Review", use_container_width=True, type="primary"):
    if not topic:
        st.error("⚠️ Please enter a research topic.")
    else:
        st.markdown("---")
        
        # --- Status area ---
        st.markdown("#### ⏳ Progress")
        status_placeholder = st.empty()
        
        st.markdown("#### 📋 Literature Review")
        report_placeholder = st.empty()
        
        full_report = ""
        
        for event_type, content in stream_research(get_token(), topic):
            
            if event_type == "error":
                st.error(f"❌ {content}")
                break
            
            elif event_type == "status":
                status_placeholder.markdown(
                    f'<div class="status-box">{content}</div>',
                    unsafe_allow_html=True
                )
            
            elif event_type == "content":
                full_report += content
                # اعرض بدون markdown أثناء الـ streaming
                report_placeholder.text(full_report + "▌")

            elif event_type == "done":
                status_placeholder.empty()
                report_placeholder.markdown("\n" + full_report)
                st.success("✅ Literature Review completed and saved!")
                break