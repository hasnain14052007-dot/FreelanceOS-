import streamlit as st
import os
import time
from dotenv import load_dotenv
from fpdf import FPDF
from main import FreelanceCopilot

load_dotenv()

# --- Page Config & Styling ---
st.set_page_config(page_title="FreelanceOS Copilot", page_icon="🚀", layout="wide")

st.markdown("""
<style>
    .hero { background: linear-gradient(90deg, #4f46e5 0%, #7c3aed 100%); padding: 2rem; border-radius: 10px; text-align: center; margin-bottom: 2rem; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    .hero h1 { color: white; margin: 0; font-size: 2.5rem; }
    .hero p { color: #e0e7ff; font-size: 1.2rem; }
    .metric-card { background: #1e293b; padding: 1.5rem; border-radius: 10px; border-left: 4px solid #6366f1; box-shadow: 0 4px 6px rgba(0,0,0,0.2); }
</style>
""", unsafe_allow_html=True)

# --- State Management & Limits ---
if "runs_left" not in st.session_state: st.session_state.runs_left = 5
if "last_run" not in st.session_state: st.session_state.last_run = 0
if "history" not in st.session_state: st.session_state.history = []
if "job_input" not in st.session_state: st.session_state.job_input = ""

def get_api_key():
    """Securely fetches API key without exposing it in UI."""
    if st.session_state.get("custom_key"):
        return st.session_state.custom_key
    try:
        return st.secrets["GEMINI_API_KEY"]
    except Exception:
        return os.environ.get("GEMINI_API_KEY", "")

# --- PDF Generation ---
def create_pdf(result_dict):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Helvetica", size=12)
    
    sections = [
        ("FreelanceOS Report", ""),
        ("Proposal", result_dict['proposal']),
        ("Analysis", result_dict['analysis']),
        ("Project Plan", result_dict['plan'])
    ]
    
    for title, content in sections:
        pdf.set_font("Helvetica", style="B", size=16)
        pdf.cell(0, 10, title, ln=True)
        pdf.set_font("Helvetica", size=11)
        # Encode/decode to safely handle unicode characters in basic FPDF
        safe_content = content.encode('latin-1', 'replace').decode('latin-1')
        pdf.multi_cell(0, 7, safe_content)
        pdf.ln(5)
        
    return pdf.output(dest='S').encode('latin-1')

# --- Sidebar ---
with st.sidebar:
    st.title("⚙️ Settings & Info")
    st.info("**How it works:**\n1. Paste job desc.\n2. AI analyzes fit.\n3. Generates proposal.\n4. Builds plan & pricing.")
    
    st.text_input("Use own Gemini Key (Optional)", type="password", key="custom_key", 
                  help="Session only. Overrides the server key.")
    
    st.metric("Free Runs Left", st.session_state.runs_left)
    st.caption("Developed securely. Keys are never logged or stored.")

# --- Main UI ---
st.markdown("<div class='hero'><h1>🚀 FreelanceOS: Agentic Copilot</h1><p>Vets clients, drafts proposals, and plans projects in seconds.</p></div>", unsafe_allow_html=True)

# Templates
cols = st.columns(4)
if cols[0].button("Load Web Dev Template"):
    st.session_state.job_input = "Need a React developer to build a 5-page dashboard integrating with Stripe. Must be done in 2 weeks. Budget is tight."
if cols[1].button("Load Design Template"):
    st.session_state.job_input = "Looking for a UI/UX designer for a fintech mobile app. Need wireframes and high-fidelity Figma files."

job_desc = st.text_area("Job Description (Max 4000 chars)", value=st.session_state.job_input, height=150, placeholder="Paste the client's job post here...")
tone = st.selectbox("Proposal Tone", ["Professional", "Confident & Bold", "Friendly & Conversational"])

if st.button("🚀 Analyze & Generate", type="primary", use_container_width=True):
    api_key = get_api_key()
    
    if not api_key:
        st.error("Server API key not configured. Please provide your own key in the sidebar.")
        st.stop()
        
    if time.time() - st.session_state.last_run < 60 and not st.session_state.get("custom_key"):
        st.warning("⏱️ Cooldown active to protect free tier. Please wait 60 seconds.")
        st.stop()
        
    if st.session_state.runs_left <= 0 and not st.session_state.get("custom_key"):
        st.error("🛑 Free runs exhausted for this session. Please enter your own API key.")
        st.stop()

    st.session_state.last_run = time.time()
    if not st.session_state.get("custom_key"):
        st.session_state.runs_left -= 1

    try:
        with st.status("Agents at work...", expanded=True) as status:
            st.write("🕵️ Lead Scout analyzing...")
            st.write("✍️ Proposal Architect drafting...")
            st.write("📊 Project Manager planning...")
            st.write("💰 Finance Officer calculating...")
            
            copilot = FreelanceCopilot(api_key)
            # Empty callback for now, could be expanded to update specific UI elements
            results = copilot.run_analysis(job_desc, tone, step_callback=lambda x: None)
            
            st.session_state.history.insert(0, results)
            status.update(label="Complete!", state="complete", expanded=False)

    except Exception as e:
        st.error(f"⚠️ {str(e)}")
        st.stop()

# --- Results Dashboard ---
if st.session_state.history:
    latest = st.session_state.history[0]
    metrics = latest["metrics"]
    
    # Metric Cards
    m1, m2, m3, m4 = st.columns(4)
    m1.markdown(f"<div class='metric-card'><h4>Fit Score</h4><h2>{metrics.fit_score}/10</h2></div>", unsafe_allow_html=True)
    
    decision_color = "green" if metrics.decision.upper() == "GO" else "red"
    m2.markdown(f"<div class='metric-card'><h4>Decision</h4><h2 style='color: {decision_color};'>{metrics.decision}</h2></div>", unsafe_allow_html=True)
    m3.markdown(f"<div class='metric-card'><h4>Est. Hours</h4><h2>{metrics.estimated_hours} hrs</h2></div>", unsafe_allow_html=True)
    m4.markdown(f"<div class='metric-card'><h4>Price</h4><h2>${metrics.recommended_price}</h2></div>", unsafe_allow_html=True)
    
    st.divider()
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["✉️ Proposal", "🕵️ Analysis", "📊 Project Plan", "🚩 Red Flags"])
    
    with tab1:
        st.subheader("Copy-ready Proposal")
        st.code(latest['proposal'], language="markdown")
    with tab2:
        st.write(latest['analysis'])
    with tab3:
        st.write(latest['plan'])
    with tab4:
        for flag in metrics.red_flags:
            st.error(f"🚩 {flag}")

    # Export
    st.divider()
    pdf_bytes = create_pdf(latest)
    st.download_button(label="📥 Download Report as PDF", data=pdf_bytes, file_name="FreelanceOS_Report.pdf", mime="application/pdf")