"""
Vidhik AI — Government Blue Dashboard (Streamlit)
Complete redesigned dashboard layout in "Government Blue" theme.

Features:
- Top navigation bar
- Collapsible sidebar with icons
- Grid layout with cards (metrics)
- Centered uploader & editor
- Audit run flow integrated with vidhik_engine.analyze_policy()
- Charts (matplotlib) and raw JSON viewer
- Download audit JSON
- Graceful fallback if vidhik_engine is missing (demo mode)

Run: streamlit run this_file.py
"""

import streamlit as st
import json
import io
import tempfile
from datetime import datetime
import pandas as pd
# import matplotlib.pyplot as plt
import numpy as np

# Try import of real engine; if missing, fallback to demo analyzer
try:
    from vidhik_engine import analyze_policy  # your real function
except Exception:
    def analyze_policy(text):
        # Demo fallback — returns structured example report
        now = datetime.utcnow().isoformat() + "Z"
        return {
            "Overall Status": "Medium Risk",
            "Executive Summary": "Automated demo analysis: medium risk identified — PII & accessibility concerns.",
            "Actionable Recommendations": (
                "### ⚖️ Recommendations for Legal Conflicts\n"
                "- Remove mandatory Aadhar enrollment clause.\n"
                "- Add retention limits (e.g., 3 years) and purpose specification.\n\n"
                "### 🌍 Recommendations for Inclusive Language\n"
                "- Avoid hardware/internet requirements that exclude rural users.\n\n"
                "### 🔒 Recommendations for PII Risk\n"
                "- Remove cleartext names/addresses from policy body; redact before storage.\n"
            ),
            "Raw Reports": {
                "Conflict Report": {
                    "Conflicting Laws": [
                        {"Rank": 1, "Similarity Score": 0.92, "Risk Level": "High",
                         "Legal Provision": "Right to privacy & Data Minimization (DPDP)"},
                    ]
                },
                "Bias Report": {
                    "flagged_phrases": [
                        {"phrase": "must register their personal details and bank account numbers", "lexicon": "exclusionary"},
                        {"phrase": "only citizens with high-speed fiber-optic internet", "lexicon": "accessibility"}
                    ]
                },
                "PII Report": {
                    "status": "PII Found",
                    "detected_items": [
                        {"type": "Name", "value": "Mr. Rajesh Kumar"},
                        {"type": "Address", "value": "Mandi Road, Dehradun 248001"},
                        {"type": "Aadhar", "value": "XXXXXXXXXXXX"}
                    ]
                }
            },
            "generated_at": now
        }

# -------------------------
# Page config
# -------------------------
st.set_page_config(
    page_title="Vidhik AI — Governance Gateway",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------
# THEME/CSS
# -------------------------
st.markdown(
    """
    <style>
    /* Page background */
    .reportview-container, .main {
        background-color: #F4F7FB;
    }

    /* Top nav */
    .top-nav {
        background: linear-gradient(90deg, #0D47A1 0%, #1976D2 40%, #2196F3 100%);
        color: white;
        padding: 14px 22px;
        border-radius: 8px;
        box-shadow: 0 6px 18px rgba(13,71,161,0.12);
        margin-bottom: 12px;
    }

    .top-nav h1 {
        margin: 0;
        font-size: 20px;
        font-weight: 700;
    }
    .top-nav .subtitle {
        font-size: 13px;
        opacity: 0.92;
    }

    /* glass card */
    .card {
        background: white;
        border-radius: 10px;
        padding: 16px;
        box-shadow: 0 6px 18px rgba(14,30,70,0.06);
    }

    /* uploader center */
    .center {
        display:flex;
        justify-content:center;
        align-items:center;
        margin-top:6px;
        margin-bottom:6px;
    }

    /* small muted text */
    .muted {
        color: #5f6f86;
        font-size:13px;
    }

    /* metrics */
    .metric-title { font-size:13px; color:#556; }
    .metric-value { font-size:22px; font-weight:700; color:#0D47A1; }

    /* compact table */
    .stDataFrame table { border-collapse: collapse; }
    </style>
    """,
    unsafe_allow_html=True
)

# -------------------------
# Top Navigation Bar
# -------------------------
top_left, top_center, top_right = st.columns([1, 6, 2])
with top_left:
    st.markdown("<div class='top-nav'><h1>⚖️ Vidhik AI</h1><div class='subtitle'>Governance Gateway — Government of Uttarakhand</div></div>", unsafe_allow_html=True)

with top_center:
    # intentionally empty - makes layout centered
    pass

with top_right:
    # small utility buttons
    if st.button("📄 Sample Policy", key="sample"):
        # insert a sample into session_state
        st.session_state["policy_text"] = (
            "[Sample policy - replace me]\n\n"
            "Clause 3.0: Citizens may voluntarily register; data collection must be minimised.\n"
        )

# -------------------------
# Sidebar (Collapsible toggle handled by Streamlit)
# -------------------------
with st.sidebar:
    st.markdown("## 🧭 Navigation")
    nav = st.radio(
        "",
        options=["Dashboard", "New Audit", "Knowledge Base", "Settings", "About"],
        index=0
    )
    st.markdown("---")
    st.markdown("### 🔎 Quick Tools")
    st.button("Run last audit", key="run_last")
    st.button("Download last report", key="dl_last")
    st.markdown("---")
    st.markdown("**Phases**")
    st.write("- Privacy Gatekeeper (DPDP)")
    st.write("- Legal Analyzer (FAISS)")
    st.write("- Fairness Auditor")

# -------------------------
# Main content: Dashboard or New Audit views
# -------------------------
if nav == "Dashboard":
    # Dashboard overview
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Overview")
    st.markdown("<div class='muted'>At-a-glance metrics and recent audit history.</div>", unsafe_allow_html=True)

    # top metrics row
    col1, col2, col3, col4 = st.columns(4)
    # sample dynamic numbers — replace with real stored state in production
    total_audits = st.session_state.get("total_audits", 42)
    high_risk = st.session_state.get("high_risk_count", 7)
    medium_risk = st.session_state.get("medium_risk_count", 18)
    low_risk = total_audits - high_risk - medium_risk

    with col1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div class='metric-title'>Total Audits</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='metric-value'>{total_audits}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div class='metric-title'>High Risk</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='metric-value'>{high_risk}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col3:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div class='metric-title'>Medium Risk</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='metric-value'>{medium_risk}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col4:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div class='metric-title'>Low Risk</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='metric-value'>{low_risk}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # Charts row
    st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)
    chart_col1, chart_col2 = st.columns([2, 1])

    # Trend chart (audits over months) - matplotlib
    months = pd.date_range(end=pd.Timestamp.today(), periods=6, freq='M').strftime('%b %Y')
    audits_by_month = np.random.randint(2, 12, size=6)
    fig1, ax1 = plt.subplots(figsize=(7, 2.6))
    ax1.plot(months, audits_by_month, marker='o')
    ax1.set_title("Audits — last 6 months")
    ax1.set_ylabel("Count")
    ax1.grid(axis='y', alpha=0.25)
    st.pyplot(fig1, use_container_width=True)

    # Pie chart: risk distribution
    fig2, ax2 = plt.subplots(figsize=(3.5, 2.6))
    labels = ["High", "Medium", "Low"]
    sizes = [high_risk, medium_risk, low_risk]
    ax2.pie(sizes, labels=labels, autopct='%1.0f%%', startangle=140)
    ax2.set_title("Risk distribution")
    st.pyplot(fig2, use_container_width=True)

    # Recent audits table
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Recent Audits")
    recent = [
        {"policy_name": "DSDP Draft v1", "status": "High Risk", "date": "2025-10-30"},
        {"policy_name": "Citizen Portal A", "status": "Medium Risk", "date": "2025-09-12"},
        {"policy_name": "Procurement Policy", "status": "Low Risk", "date": "2025-08-03"},
    ]
    st.table(pd.DataFrame(recent))
    st.markdown("</div>", unsafe_allow_html=True)

elif nav == "New Audit":
    # New audit flow
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.header("New Policy Audit")
    st.markdown("<div class='muted'>Paste the policy or upload a document. Then run Vidhik AI Audit.</div>", unsafe_allow_html=True)

    # text area with session persistence
    if "policy_text" not in st.session_state:
        st.session_state["policy_text"] = ""

    policy_input = st.text_area(
        "Policy Draft to Audit:",
        value=st.session_state.get("policy_text", ""),
        height=300,
        max_chars=20000,
        help="Edit policy text here before running audit."
    )
    st.session_state["policy_text"] = policy_input

    # uploader centered
    st.markdown("<div class='center'>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload policy (txt, pdf, docx)", type=['txt', 'pdf', 'docx', 'doc'])
    st.markdown("</div>", unsafe_allow_html=True)

    # handle uploaded file (simple)
    if uploaded_file:
        try:
            content_type = uploaded_file.type
            if "text" in content_type or uploaded_file.name.endswith(".txt"):
                raw = str(uploaded_file.read(), "utf-8")
                st.session_state["policy_text"] = raw
                st.success(f"Loaded text file: {uploaded_file.name}")
            elif "pdf" in content_type or uploaded_file.name.endswith(".pdf"):
                try:
                    import PyPDF2
                    reader = PyPDF2.PdfReader(uploaded_file)
                    pages = [p.extract_text() or "" for p in reader.pages]
                    st.session_state["policy_text"] = "\n".join(pages)
                    st.success(f"Loaded PDF: {uploaded_file.name}")
                except Exception:
                    st.warning("PyPDF2 not available or PDF extraction failed. Please paste text.")
            else:
                try:
                    import docx
                    doc = docx.Document(uploaded_file)
                    st.session_state["policy_text"] = "\n".join([p.text for p in doc.paragraphs])
                    st.success(f"Loaded DOCX: {uploaded_file.name}")
                except Exception:
                    st.warning("python-docx not available. Please paste text.")
        except Exception as e:
            st.error(f"Error reading uploaded file: {e}")

    # run audit button row with reason input
    reason = st.text_input("Short note / reason for audit (optional)")
    run_col1, run_col2 = st.columns([1, 3])
    with run_col1:
        run_now = st.button("🚀 Run Vidhik AI Audit")
    with run_col2:
        st.markdown("<div class='muted'>Tip: include a short reason so reports are traceable.</div>", unsafe_allow_html=True)

    if run_now:
        if not st.session_state["policy_text"].strip():
            st.error("Please paste policy text or upload a file before running the audit.")
        else:
            with st.spinner("Running Vidhik AI analysis..."):
                try:
                    report = analyze_policy(st.session_state["policy_text"])
                    # store report in session and increment counters
                    st.session_state["report"] = report
                    st.success("Audit completed.")
                    st.session_state["total_audits"] = st.session_state.get("total_audits", 42) + 1
                    # update risk counters heuristically from report
                    overall = (report.get("Overall Status") or "").lower()
                    if "high" in overall:
                        st.session_state["high_risk_count"] = st.session_state.get("high_risk_count", 7) + 1
                    elif "medium" in overall:
                        st.session_state["medium_risk_count"] = st.session_state.get("medium_risk_count", 18) + 1
                except Exception as e:
                    st.error(f"Analysis failed: {e}")

    # if there is a report, provide quick view
    if "report" in st.session_state:
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        st.subheader("Latest Audit Snapshot")
        rep = st.session_state["report"]
        st.markdown(f"**Status:** {rep.get('Overall Status', 'Unknown')}")
        st.markdown("**Executive summary**")
        st.write(rep.get("Executive Summary", ""))

        # download json
        json_bytes = json.dumps(rep, indent=2).encode("utf-8")
        st.download_button("Download Audit JSON", data=json_bytes, file_name="vidhik_audit.json", mime="application/json")

elif nav == "Knowledge Base":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.header("Knowledge Base")
    st.markdown("Searchable legal provisions, DPDP notes, and policy templates.")
    # simple static list for demo
    kb = [
        {"title": "DPDP — Data Minimisation", "snippet": "Collect only what is necessary."},
        {"title": "Right to Privacy — Constitutional Note", "snippet": "Privacy is a fundamental right."},
        {"title": "Retention policy template", "snippet": "Retention: 3 years unless legal hold."},
    ]
    for item in kb:
        st.markdown(f"**{item['title']}**")
        st.markdown(f"<div class='muted'>{item['snippet']}</div>", unsafe_allow_html=True)
        st.markdown("---")
    st.markdown("</div>", unsafe_allow_html=True)

elif nav == "Settings":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.header("Settings")
    st.markdown("Minimal settings for demo mode.")
    if st.checkbox("Enable demo fallback analyzer (if vidhik_engine missing)", value=("analyze_policy" not in globals())):
        st.info("Demo analyzer enabled.")
    st.markdown("</div>", unsafe_allow_html=True)

elif nav == "About":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.header("About Vidhik AI")
    st.markdown("A compliance-first policy auditing assistant tailored for public sector use.")
    st.markdown("**Frameworks referenced:** DPDP Act 2023, IT Act 2000, Constitutional principles.")
    st.markdown("Built for prototyping and government pilots.")
    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------
# Footer (global)
# -------------------------
st.markdown("---")
st.markdown("**Vidhik AI** • Government of Uttarakhand • DPDP Act 2023 • IT Act 2000")

# -------------------------
# Helpful dev note (not shown to users) — keep for your codebase
# -------------------------
# End of file
