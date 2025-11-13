import streamlit as st
import json
import tempfile
import os

# Import engine
from vidhik_engine import analyze_policy

# ===============================
# PAGE CONFIG + SIDEBAR TOGGLER
# ===============================

# Sidebar toggle session
if "sidebar_state" not in st.session_state:
    st.session_state["sidebar_state"] = "expanded"

# --- SIDEBAR TOGGLE BUTTON ---
with st.container():
    if st.button("☰ Menu"):
        st.session_state["sidebar_state"] = (
            "collapsed" if st.session_state["sidebar_state"] == "expanded" else "expanded"
        )

# Apply sidebar state
st.set_page_config(
    page_title="Vidhik AI: Governance Gateway",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state=st.session_state["sidebar_state"]
)

# ===============================
# HEADER
# ===============================

st.title("⚖️ Vidhik AI: The Compliance-First Policy Audit")
st.markdown("### The Governance Gateway for the Government of Uttarakhand")
st.info("Upload your policy draft (or use the sample text) and click 'Run Audit' to instantly check for legal conflicts, PII risks, and policy bias.")

# ===============================
# SIDEBAR STATIC INFO
# ===============================

with st.sidebar:
    st.title("Vidhik AI Architecture")
    st.markdown("**Phase 1: Privacy & PII Check**")
    st.markdown("• DPDP Act Redaction Layer")
    st.markdown("**Phase 2: Legal Analyzer**")
    st.markdown("• Semantic Conflict Detection (FAISS)")
    st.markdown("**Phase 3: Ethical Auditor**")
    st.markdown("• Bias & Inclusivity Scan")

# ===============================
# PLACEHOLDER POLICY TEXT
# ===============================

placeholder_policy = """
[Draft Policy: GO for Digital Service Delivery Platform (DSDP)]

[Clause 3.0: Citizen Enrollment]
All citizens of the state must register their personal details and bank account numbers on the DSDP. Citizens shall, in all instances, only use their Aadhar ID and provide scanned copies of their current utility bill. Mr. Rajesh Kumar, residing at Mandi Road, Dehradun 248001, will be the initial contact for technical queries.

[Clause 4.1: Data Handling Protocol]
Data collected via the DSDP will be stored on a private server maintained by the department. Personal data, including the Aadhar ID, may be retained indefinitely and shared with any other state department upon simple request.

[Clause 5.0: Access and Availability]
Access to DSDP services is restricted solely to citizens who can reliably interface using dedicated, high-speed fiber-optic internet connections and advanced desktop computing hardware.
"""

# ===============================
# MAIN INPUT TEXT AREA
# ===============================

policy_input = st.text_area(
    "Policy Draft to Audit:",
    value=placeholder_policy,
    height=400,
    help="Review and edit the policy text before running the audit"
)

# ===============================
# FILE UPLOAD (NOW IN MAIN PAGE)
# ===============================

st.markdown("### 📁 Upload Policy Document")

uploaded_file = st.file_uploader(
    "Choose a file",
    type=['txt', 'pdf', 'docx', 'doc'],
    help="Upload your policy document (TXT, PDF, DOCX, DOC)"
)

# Process uploaded file
if uploaded_file:
    try:
        if uploaded_file.type == "text/plain":
            policy_input = str(uploaded_file.read(), "utf-8")

        elif uploaded_file.type == "application/pdf":
            try:
                import PyPDF2
                reader = PyPDF2.PdfReader(uploaded_file)
                pdf_text = ""
                for page in reader.pages:
                    pdf_text += page.extract_text() + "\n"
                policy_input = pdf_text
            except:
                st.warning("Install PyPDF2 to read PDF files.")

        elif uploaded_file.type in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                                    "application/msword"]:
            try:
                import docx
                doc = docx.Document(uploaded_file)
                text = "\n".join([p.text for p in doc.paragraphs])
                policy_input = text
            except:
                st.warning("Install python-docx to read DOCX files.")
    except Exception as e:
        st.error(f"Error reading file: {e}")

# ===============================
# RUN AUDIT BUTTON
# ===============================

if st.button("🚀 Run Vidhik AI Audit", type="primary"):
    if not policy_input.strip():
        st.error("Please enter some policy text to analyze.")
        st.stop()

    try:
        with st.spinner("Analyzing policy..."):
            final_report = analyze_policy(policy_input)
        st.session_state['report'] = final_report
        st.success("Audit completed successfully!")
    except Exception as e:
        st.error(f"Error during audit: {e}")
        st.stop()

# ===============================
# REPORT DISPLAY
# ===============================

if "report" in st.session_state:
    report = st.session_state['report']
    st.markdown("---")

    # Status
    overall_status = report.get("Overall Status", "Unknown")
    if overall_status in ["Clean", "Low Risk"]:
        st.success(f"## Policy Status: {overall_status}")
    elif overall_status in ["High Risk", "Database Error", "Processing Error"]:
        st.error(f"## POLICY ALERT: {overall_status}")
    elif overall_status == "Medium Risk":
        st.warning(f"## Policy Status: {overall_status}")
    else:
        st.info(f"## Policy Status: {overall_status}")

    # Executive Summary
    st.header("Executive Summary")
    st.markdown(report.get("Executive Summary", "No summary provided."))

    st.markdown("---")

    # Tabs
    tab1, tab2, tab3 = st.tabs(["⚖ Legal Conflicts", "🌍 Policy Bias", "🔐 PII & Data Risk"])

    # Tab 1 - Legal
    with tab1:
        st.subheader("Legal Conflicts and Compliance Issues")
        st.markdown(report.get("Actionable Recommendations", ""))

    # Tab 2 - Bias
    with tab2:
        st.subheader("Ethical Audit")
        bias = report.get("Raw Reports", {}).get("Bias Report", {})
        st.json(bias)

    # Tab 3 - PII
    with tab3:
        st.subheader("PII Risk Analysis")
        pii = report.get("Raw Reports", {}).get("PII Report", {})
        st.json(pii)

    # Raw report
    with st.expander("📊 Full Raw Report"):
        st.json(report)

# FOOTER
st.markdown("---")
st.markdown("**Vidhik AI** | Government of Uttarakhand | DPDP Act 2023 | IT Act 2000")
