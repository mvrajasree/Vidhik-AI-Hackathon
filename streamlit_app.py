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

# Collapsible Vidhik AI Architecture section
with st.sidebar.expander("🔧 Vidhik AI Architecture", expanded=False):
    st.markdown("**Phase 1: The Security Gatekeeper**")
    st.markdown("✅ PII Redaction & Data Privacy Check (DPDP Act)")
    st.markdown("**Phase 2: The Legal Analyzer**")
    st.markdown("✅ Semantic Conflict Detection (FAISS DB)")
    st.markdown("**Phase 3: The Fairness Auditor**")
    st.markdown("✅ Linguistic Bias & Inclusivity Check")

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
# MAIN TEXT AREA
# ==========================

st.subheader("Policy Draft to Audit:")
policy_input = st.text_area(
    "Policy Text",
    value=placeholder_policy,
    height=400,
    label_visibility="collapsed"
)

# ==========================
# FILE UPLOAD SECTION (BELOW TEXT AREA)
# ==========================

st.markdown("---")
st.subheader("📁 Upload Policy Document")

uploaded_file = st.file_uploader(
    "Choose a file to replace the current policy text",
    type=['txt', 'pdf', 'docx', 'doc'],
    help="Upload your policy document to replace the text above"
)

# ==========================
# FILE PROCESSING
# ==========================

if uploaded_file:
    try:
        st.success(f"Uploaded: {uploaded_file.name}")

        if uploaded_file.type == "text/plain":
            input_text = str(uploaded_file.read(), "utf-8")
            # Update the text area with uploaded content
            st.session_state.uploaded_text = input_text

        elif uploaded_file.type == "application/pdf":
            import PyPDF2
            reader = PyPDF2.PdfReader(uploaded_file)
            input_text = "\n".join([page.extract_text() for page in reader.pages])
            st.session_state.uploaded_text = input_text

        elif uploaded_file.type in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                                    "application/msword"]:
            import docx
            doc = docx.Document(uploaded_file)
            input_text = "\n".join([p.text for p in doc.paragraphs])
            st.session_state.uploaded_text = input_text

        # Update the text area
        if 'uploaded_text' in st.session_state:
            policy_input = st.session_state.uploaded_text
            st.rerun()

    except Exception as e:
        st.error(f"File error: {e}")

# ==========================
# RUN BUTTON SECTION
# ==========================

st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    if st.button("🚀 Run Vidhik AI Audit", type="primary", use_container_width=True):
        # Use uploaded text if available, otherwise use text area content
        if 'uploaded_text' in st.session_state:
            final_text = st.session_state.uploaded_text
        else:
            final_text = policy_input
            
        if not final_text.strip():
            st.error("Enter policy text first.")
            st.stop()

        with st.spinner("Analyzing policy document..."):
            try:
                final_report = analyze_policy(final_text)
                st.session_state["report"] = final_report
                st.session_state["report_generated"] = True
                st.success("Audit Complete!")
            except Exception as e:
                st.error(f"Error during analysis: {e}")
                st.stop()

# ==========================
# REPORT DISPLAY + PDF EXPORT
# ==========================

if "report" in st.session_state and st.session_state.get("report_generated", False):
    report = st.session_state["report"]

    st.markdown("---")
    st.header("📊 Audit Report")
    
    # Overall Status with color coding
    status = report.get("Overall Status", "Unknown")
    if "FAIL" in status.upper():
        st.error(f"### 📌 Overall Status: {status}")
    elif "PASS" in status.upper():
        st.success(f"### 📌 Overall Status: {status}")
    else:
        st.warning(f"### 📌 Overall Status: {status}")

    st.subheader("Executive Summary")
    st.write(report.get("Executive Summary", ""))

    # ---- Tabs for Detailed Reports ----
    tab1, tab2, tab3 = st.tabs(["⚖️ Legal Conflicts", "🌍 Policy Bias", "🔐 PII Risk"])

    with tab1:
        conflict_report = report.get("Raw Reports", {}).get("Conflict Report", {})
        if conflict_report:
            st.json(conflict_report)
        else:
            st.info("No legal conflicts detected")

    with tab2:
        bias_report = report.get("Raw Reports", {}).get("Bias Report", {})
        if bias_report:
            st.json(bias_report)
        else:
            st.info("No bias issues detected")

    with tab3:
        pii_report = report.get("Raw Reports", {}).get("PII Report", {})
        if pii_report:
            st.json(pii_report)
        else:
            st.info("No PII risks detected")

    # ---- PDF DOWNLOAD SECTION ----
    st.markdown("---")
    st.header("📄 Export Report")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Download PDF Report")
        st.markdown("Get a formatted PDF version of the complete audit report for official records and sharing.")
        
        # Generate PDF
        pdf_bytes = create_pdf(report)
        
        st.download_button(
            label="📥 Download PDF Report",
            data=pdf_bytes,
            file_name="VidhikAI_Audit_Report.pdf",
            mime="application/pdf",
            use_container_width=True,
            help="Download a PDF version of the complete audit report"
        )
    
    with col2:
        st.subheader("Additional Options")
        
        # Download JSON
        json_str = json.dumps(report, indent=2)
        st.download_button(
            label="📥 Download JSON Data",
            data=json_str,
            file_name="VidhikAI_Audit_Data.json",
            mime="application/json",
            use_container_width=True,
            help="Download raw JSON data for further analysis"
        )
        
        # Clear report button
        if st.button("🗑️ Clear Report", use_container_width=True):
            st.session_state.pop("report", None)
            st.session_state.pop("report_generated", None)
            st.session_state.pop("uploaded_text", None)
            st.rerun()

    # ---- RAW JSON VIEW ----
    with st.expander("🔍 View Raw JSON Data"):
        st.json(report)

# ==========================
# FOOTER
# ==========================
st.markdown("---")
st.caption("Vidhik AI • Government of Uttarakhand • DPDP Act • IT Act • 2025")
