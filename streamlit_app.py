import streamlit as st
import json
import os

from vidhik_engine import analyze_policy

# ==========================================
# PAGE CONFIG + SIDEBAR STATE
# ==========================================

if "sidebar_state" not in st.session_state:
    st.session_state["sidebar_state"] = "expanded"

st.set_page_config(
    page_title="Vidhik AI: Governance Gateway",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state=st.session_state["sidebar_state"]
)

# ==========================================
# CUSTOM DYNAMIC CSS
# ==========================================

st.markdown(
    """
    <style>
    /* Smooth UI Styling */

    body {
        background-color: #F7F9FC;
    }

    .main-title {
        font-size: 42px;
        font-weight: 700;
        margin-bottom: -10px;
        color: #1A237E;
    }

    .sub-title {
        font-size: 20px;
        color: #3949AB;
        margin-bottom: 20px;
    }

    /* Glass-card container */
    .glass-card {
        background: rgba(255, 255, 255, 0.55);
        padding: 20px 25px;
        border-radius: 16px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.08);
        backdrop-filter: blur(8px);
        margin-bottom: 20px;
    }

    /* Rounded buttons */
    .stButton > button {
        border-radius: 10px;
        padding: 10px 25px;
        font-size: 17px;
        background-color: #303F9F;
        color: white;
        border: none;
    }

    .stButton > button:hover {
        background-color: #1A237E;
        color: white;
    }

    /* Center file uploader */
    .file-uploader {
        display: flex;
        justify-content: center;
        margin-top: -15px;
        margin-bottom: 15px;
    }

    /* Sidebar toggle button */
    #menu-button {
        position: fixed;
        top: 18px;
        left: 18px;
        z-index: 9999;
        background: #1A237E;
        color: white;
        border-radius: 8px;
        padding: 8px 12px;
        cursor: pointer;
        font-size: 22px;
    }
    #menu-button:hover {
        background: #000051;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ==========================================
# SIDEBAR TOGGLE
# ==========================================

menu_placeholder = st.empty()
if menu_placeholder.button("☰", key="menu", help="Toggle Menu"):
    st.session_state["sidebar_state"] = (
        "collapsed" if st.session_state["sidebar_state"] == "expanded" else "expanded"
    )
    st.rerun()

# ==========================================
# HEADER
# ==========================================

st.markdown("<h1 class='main-title'>⚖️ Vidhik AI: Policy Audit System</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>Governance Gateway for Uttarakhand</p>", unsafe_allow_html=True)
st.info("Upload your policy draft and click Run Audit to check for legal conflicts, PII leakage and policy bias.")

# ==========================================
# SIDEBAR CONTENT
# ==========================================

with st.sidebar:
    st.title("📚 Architecture Overview")
    st.markdown("### 🔐 Phase 1: Privacy Gatekeeper")
    st.markdown("- PII Detection & Redaction (DPDP Act)")
    st.markdown("### ⚖ Phase 2: Legal Analyzer")
    st.markdown("- Semantic Conflict Check (FAISS + Acts DB)")
    st.markdown("### 🌍 Phase 3: Ethical Auditor")
    st.markdown("- Bias & Inclusivity Review")

# ==========================================
# INPUT AREA
# ==========================================

placeholder_policy = """
[Draft Policy: GO for Digital Service Delivery Platform (DSDP)]

[Clause 3.0: Citizen Enrollment]
All citizens of the state must register their personal details and bank account numbers on the DSDP. Citizens shall, in all instances, only use their Aadhar ID and provide scanned copies of their current utility bill. Mr. Rajesh Kumar, residing at Mandi Road, Dehradun 248001, will be the initial contact for technical queries.

[Clause 4.1: Data Handling Protocol]
Data collected via the DSDP will be stored on a private server maintained by the department. Personal data, including the Aadhar ID, may be retained indefinitely and shared with any other state department upon simple request.

[Clause 5.0: Access and Availability]
Access to DSDP services is restricted solely to citizens who can reliably interface using dedicated, high-speed fiber-optic internet connections and advanced desktop computing hardware.
"""

st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
policy_input = st.text_area(
    "Policy Draft to Audit:",
    value=placeholder_policy,
    height=300
)
st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# FILE UPLOADER (CENTERED)
# ==========================================

st.markdown("<div class='file-uploader'>", unsafe_allow_html=True)
uploaded_file = st.file_uploader(
    "",
    type=['txt', 'pdf', 'docx', 'doc'],
)
st.markdown("</div>", unsafe_allow_html=True)

if uploaded_file:
    try:
        if uploaded_file.type == "text/plain":
            policy_input = str(uploaded_file.read(), "utf-8")

        elif uploaded_file.type == "application/pdf":
            import PyPDF2
            reader = PyPDF2.PdfReader(uploaded_file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            policy_input = text

        elif uploaded_file.type in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                                    "application/msword"]:
            import docx
            doc = docx.Document(uploaded_file)
            policy_input = "\n".join([p.text for p in doc.paragraphs])

    except Exception as e:
        st.error(f"Error reading file: {e}")

# ==========================================
# RUN BUTTON
# ==========================================

st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
run_button = st.button("🚀 Run Vidhik AI Audit")
st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# AUDIT PROCESS
# ==========================================

if run_button:
    if not policy_input.strip():
        st.error("Please enter some policy text.")
        st.stop()
    with st.spinner("Analyzing Policy..."):
        report = analyze_policy(policy_input)
        st.session_state["report"] = report
    st.success("Audit Completed!")

# ==========================================
# OUTPUT RESULTS
# ==========================================

if "report" in st.session_state:
    report = st.session_state["report"]

    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)

    status = report.get("Overall Status", "Unknown")

    if status in ["Clean", "Low Risk"]:
        st.success(f"Policy Status: {status}")
    elif status == "Medium Risk":
        st.warning(f"Policy Status: {status}")
    else:
        st.error(f"Policy Status: {status}")

    st.header("Executive Summary")
    st.write(report.get("Executive Summary", "No summary available."))

    st.markdown("</div>", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["⚖ Legal", "🌍 Bias", "🔐 PII"])

    with tab1:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("Legal Conflict Report")
        st.json(report.get("Raw Reports", {}).get("Conflict Report", {}))
        st.markdown("</div>", unsafe_allow_html=True)

    with tab2:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("Bias Analysis")
        st.json(report.get("Raw Reports", {}).get("Bias Report", {}))
        st.markdown("</div>", unsafe_allow_html=True)

    with tab3:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("PII Audit Report")
        st.json(report.get("Raw Reports", {}).get("PII Report", {}))
        st.markdown("</div>", unsafe_allow_html=True)

# FOOTER
st.markdown("---")
st.markdown("**Vidhik AI** • Government of Uttarakhand • DPDP Act 2023 • IT Act 2000")
