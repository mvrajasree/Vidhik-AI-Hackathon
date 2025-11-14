import streamlit as st
import json
import tempfile
import os

# Import engine logic
from vidhik_engine import analyze_policy

# ==========================
# PDF GENERATOR
# ==========================

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
import io

def create_pdf(report):
    buffer = io.BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=2 * cm,
        rightMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm
    )

    styles = getSampleStyleSheet()
    story = []

    # Title
    story.append(Paragraph("<b>Vidhik AI – Policy Audit Report</b>", styles["Title"]))
    story.append(Spacer(1, 16))

    # Overall Status
    status = report.get("Overall Status", "Unknown")
    story.append(Paragraph(f"<b>Overall Status:</b> {status}", styles["Heading2"]))
    story.append(Spacer(1, 12))

    # Executive Summary
    story.append(Paragraph("<b>Executive Summary</b>", styles["Heading2"]))
    story.append(Paragraph(report.get("Executive Summary", "No summary").replace("\n", "<br/>"), styles["Normal"]))
    story.append(Spacer(1, 12))

    # Actionable Recommendations
    story.append(Paragraph("<b>Actionable Recommendations</b>", styles["Heading2"]))
    story.append(Paragraph(report.get("Actionable Recommendations", "None").replace("\n", "<br/>"), styles["Normal"]))
    story.append(Spacer(1, 12))

    # Raw Reports
    story.append(Paragraph("<b>Raw Reports</b>", styles["Heading2"]))

    for title, section in report.get("Raw Reports", {}).items():
        story.append(Spacer(1, 10))
        story.append(Paragraph(f"<b>{title}</b>", styles["Heading3"]))
        raw_json = json.dumps(section, indent=2).replace("\n", "<br/>")
        story.append(Paragraph(raw_json, styles["Code"]))

    doc.build(story)
    pdf_data = buffer.getvalue()
    buffer.close()
    return pdf_data


# ==========================
# PAGE CONFIG
# ==========================

st.set_page_config(
    page_title="Vidhik AI: Governance Gateway",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

FAIL_COLOR = "#FF4B4B"
PASS_COLOR = "#00BFA5"

st.title("⚖️ Vidhik AI: The Compliance-First Policy Audit")
st.markdown("### The Governance Gateway for the Government of Uttarakhand")
st.info("Upload your policy draft (or use the sample text) and click 'Run Audit' to instantly check for legal conflicts, PII risks, and policy bias.")

# ==========================
# SIDEBAR
# ==========================

st.sidebar.title("Navigation")

# Option 1: Vidhik AI Architecture
st.sidebar.subheader("1. Vidhik AI Architecture")
st.sidebar.markdown("**Phase 1: The Security Gatekeeper**")
st.sidebar.markdown("✅ PII Redaction & Data Privacy Check (DPDP Act)")
st.sidebar.markdown("**Phase 2: The Legal Analyzer**")
st.sidebar.markdown("✅ Semantic Conflict Detection (FAISS DB)")
st.sidebar.markdown("**Phase 3: The Fairness Auditor**")
st.sidebar.markdown("✅ Linguistic Bias & Inclusivity Check")

st.sidebar.markdown("---")

# Upload option on the left sidebar
st.sidebar.subheader("📁 Upload Policy Document")

uploaded_file = st.sidebar.file_uploader(
    "Choose a file",
    type=['txt', 'pdf', 'docx', 'doc'],
    help="Upload your policy document"
)

# ==========================
# PLACEHOLDER POLICY
# ==========================

placeholder_policy = """
[Draft Policy: GO for Digital Service Delivery Platform (DSDP)]

[Clause 3.0: Citizen Enrollment]
All citizens of the state must register their personal details and bank account numbers on the DSDP. Citizens shall, in all instances, only use their Aadhar ID and provide scanned copies of their current utility bill. Mr. Rajesh Kumar, residing at Mandi Road, Dehradun 248001, will be the initial contact for technical queries.

[Clause 4.1: Data Handling Protocol]
Data collected via the DSDP will be stored on a private server maintained by the department. Personal data, including the Aadhar ID, may be retained indefinitely and shared with any other state department upon simple request.

[Clause 5.0: Access and Availability]
Access to DSDP services is restricted solely to citizens who can reliably interface using dedicated, high-speed fiber-optic internet connections and advanced desktop computing hardware.
"""

# ==========================
# FILE PROCESSING
# ==========================

input_text = ""
if uploaded_file:
    try:
        st.sidebar.success(f"Uploaded: {uploaded_file.name}")

        if uploaded_file.type == "text/plain":
            input_text = str(uploaded_file.read(), "utf-8")

        elif uploaded_file.type == "application/pdf":
            import PyPDF2
            reader = PyPDF2.PdfReader(uploaded_file)
            input_text = "\n".join([page.extract_text() for page in reader.pages])

        elif uploaded_file.type in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                                    "application/msword"]:
            import docx
            doc = docx.Document(uploaded_file)
            input_text = "\n".join([p.text for p in doc.paragraphs])

    except Exception as e:
        st.sidebar.error(f"File error: {e}")
        input_text = placeholder_policy

else:
    input_text = placeholder_policy

# ==========================
# MAIN TEXT AREA
# ==========================

policy_input = st.text_area(
    "Policy Draft to Audit:",
    value=input_text,
    height=400
)

# ==========================
# RUN BUTTON
# ==========================

if st.button("🚀 Run Vidhik AI Audit", type="primary"):
    if not policy_input.strip():
        st.error("Enter policy text first.")
        st.stop()

    with st.spinner("Analyzing..."):
        try:
            final_report = analyze_policy(policy_input)
            st.session_state["report"] = final_report
            st.success("Audit Complete!")
        except Exception as e:
            st.error(f"Error: {e}")
            st.stop()

# ==========================
# REPORT DISPLAY + PDF EXPORT
# ==========================

if "report" in st.session_state:
    report = st.session_state["report"]

    st.markdown("---")
    st.header("Audit Report")

    st.subheader("📌 Overall Status")
    st.write(report.get("Overall Status", "Unknown"))

    st.subheader("Executive Summary")
    st.write(report.get("Executive Summary", ""))

    # ---- Tabs ----
    tab1, tab2, tab3 = st.tabs(["⚖ Legal Conflicts", "🌍 Policy Bias", "🔐 PII Risk"])

    with tab1:
        st.write(report.get("Raw Reports", {}).get("Conflict Report", {}))

    with tab2:
        st.write(report.get("Raw Reports", {}).get("Bias Report", {}))

    with tab3:
        st.write(report.get("Raw Reports", {}).get("PII Report", {}))

    # ---- PDF DOWNLOAD BUTTON ----

    pdf_bytes = create_pdf(report)

    st.markdown("### 📄 Download PDF Report")
    st.download_button(
        label="Download PDF",
        data=pdf_bytes,
        file_name="VidhikAI_Audit_Report.pdf",
        mime="application/pdf"
    )

    # ---- RAW JSON VIEW ----
    with st.expander("View Raw JSON"):
        st.json(report)

# ==========================
# FOOTER
# ==========================
st.markdown("---")
st.caption("Vidhik AI • Government of Uttarakhand • DPDP Act • IT Act • 2025")
