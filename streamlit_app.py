import streamlit as st
import json
import io

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

# ==========================
# CENTERED TITLE
# ==========================

st.markdown(
    """
    <div style='text-align: center;'>
        <h1>⚖️ Vidhik AI</h1>
        <h3>The Governance Gateway for the Government of Uttarakhand</h3>
    </div>
    """,
    unsafe_allow_html=True
)

st.info("Upload your policy draft (or use the sample text) and click 'Run Audit' to instantly check for legal conflicts, PII risks, and policy bias.")

# ==========================
# SIMPLIFIED PDF GENERATOR (with fallbacks)
# ==========================

def create_pdf(report):
    try:
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.units import cm
        
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
        summary = report.get("Executive Summary", "No summary available").replace("\n", "<br/>")
        story.append(Paragraph(summary, styles["Normal"]))
        story.append(Spacer(1, 12))

        # Actionable Recommendations
        story.append(Paragraph("<b>Actionable Recommendations</b>", styles["Heading2"]))
        recommendations = report.get("Actionable Recommendations", "None").replace("\n", "<br/>")
        story.append(Paragraph(recommendations, styles["Normal"]))
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
        
    except ImportError:
        st.error("PDF generation libraries not available. Please install reportlab.")
        return None
    except Exception as e:
        st.error(f"PDF generation failed: {e}")
        return None

# ==========================
# MOCK ANALYSIS FUNCTION (in case vidhik_engine is missing)
# ==========================

def analyze_policy(policy_text):
    """Mock analysis function if the real engine isn't available"""
    return {
        "Overall Status": "PASS with Recommendations",
        "Executive Summary": "Policy analysis completed successfully. No critical legal conflicts detected, but some improvements recommended for data privacy and inclusivity.",
        "Actionable Recommendations": "1. Limit data retention period\n2. Remove mandatory Aadhar requirement\n3. Add alternative authentication methods\n4. Specify data sharing protocols",
        "Raw Reports": {
            "Conflict Report": {"status": "PASS", "issues_found": 2},
            "Bias Report": {"status": "WARNING", "issues_found": 1},
            "PII Report": {"status": "FAIL", "issues_found": 3}
        }
    }

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
# PLACEHOLDER POLICY (ORIGINAL FROM FIRST CODE)
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
# FILE PROCESSING FUNCTIONS
# ==========================

def process_text_file(uploaded_file):
    """Process text files"""
    try:
        return str(uploaded_file.read(), "utf-8")
    except Exception as e:
        st.error(f"Error reading text file: {e}")
        return None

def process_pdf_file(uploaded_file):
    """Process PDF files"""
    try:
        import PyPDF2
        reader = PyPDF2.PdfReader(uploaded_file)
        text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
        return text
    except ImportError:
        st.error("PyPDF2 not installed. Please install it to process PDF files.")
        return None
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
        return None

def process_docx_file(uploaded_file):
    """Process DOCX files"""
    try:
        import docx
        doc = docx.Document(uploaded_file)
        text = "\n".join([p.text for p in doc.paragraphs if p.text])
        return text
    except ImportError:
        st.error("python-docx not installed. Please install it to process Word documents.")
        return None
    except Exception as e:
        st.error(f"Error reading Word document: {e}")
        return None

# ==========================
# MAIN TEXT AREA (ORIGINAL FROM FIRST CODE)
# ==========================

st.subheader("Policy Draft to Audit")
policy_input = st.text_area(
    "Policy Draft to Audit:",
    value=placeholder_policy,
    height=400,
    label_visibility="collapsed"
)

# ==========================
# UPLOAD BUTTON AND RUN BUTTON SECTION (IMPROVED ALIGNMENT)
# ==========================

st.markdown("### Actions")
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    st.markdown("#### 📁 Upload Document")
    uploaded_file = st.file_uploader(
        "Choose a file",
        type=['txt', 'pdf', 'docx', 'doc'],
        help="Upload your policy document",
        label_visibility="collapsed"
    )
    if uploaded_file:
        st.success(f"✅ {uploaded_file.name}")

with col2:
    st.markdown("#### 🚀 Run Analysis")
    run_audit = st.button(
        "Run Vidhik AI Audit", 
        type="primary", 
        use_container_width=True,
        help="Click to analyze the policy document"
    )

with col3:
    st.markdown("#### 🛠️ Tools")
    if st.session_state.get("report"):
        if st.button("🗑️ Clear Report", use_container_width=True, type="secondary"):
            st.session_state.pop("report", None)
            st.session_state.pop("report_text", None)
            st.rerun()

# ==========================
# PROCESS AUDIT WHEN RUN BUTTON IS CLICKED
# ==========================

if run_audit:
    # Process uploaded file if any
    input_text = ""
    if uploaded_file:
        try:
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

            # Use uploaded file content
            final_text = input_text if input_text else policy_input
        except Exception as e:
            st.error(f"File error: {e}")
            final_text = policy_input
    else:
        # Use text area content
        final_text = policy_input

    if not final_text.strip():
        st.error("Please enter policy text first.")
        st.stop()

    with st.spinner("🔍 Analyzing policy document..."):
        try:
            # Try to import the real analyzer, fall back to mock
            try:
                from vidhik_engine import analyze_policy as real_analyze_policy
                final_report = real_analyze_policy(final_text)
            except ImportError:
                st.warning("Using mock analysis - vidhik_engine not available")
                final_report = analyze_policy(final_text)
            
            st.session_state["report"] = final_report
            st.session_state["report_text"] = final_text
            st.success("✅ Audit Complete!")
        except Exception as e:
            st.error(f"Error during analysis: {e}")
            st.stop()

# ==========================
# REPORT DISPLAY + PDF EXPORT
# ==========================

if "report" in st.session_state:
    report = st.session_state["report"]

    st.markdown("---")
    st.header("📊 Audit Report")
    
    # Overall Status with better styling
    status = report.get("Overall Status", "Unknown")
    status_col1, status_col2 = st.columns([1, 3])
    
    with status_col1:
        st.subheader("Overall Status")
    with status_col2:
        if "FAIL" in status.upper():
            st.error(f"**{status}**")
        elif "PASS" in status.upper():
            st.success(f"**{status}**")
        else:
            st.warning(f"**{status}**")

    # Executive Summary
    st.subheader("Executive Summary")
    st.write(report.get("Executive Summary", ""))

    # ---- Tabs for Detailed Reports ----
    tab1, tab2, tab3 = st.tabs(["⚖️ Legal Conflicts", "🌍 Policy Bias", "🔐 PII Risk"])

    with tab1:
        conflict_data = report.get("Raw Reports", {}).get("Conflict Report", {})
        if conflict_data:
            st.json(conflict_data)
        else:
            st.info("No legal conflict data available")

    with tab2:
        bias_data = report.get("Raw Reports", {}).get("Bias Report", {})
        if bias_data:
            st.json(bias_data)
        else:
            st.info("No bias analysis data available")

    with tab3:
        pii_data = report.get("Raw Reports", {}).get("PII Report", {})
        if pii_data:
            st.json(pii_data)
        else:
            st.info("No PII analysis data available")

    # ---- EXPORT SECTION ----
    st.markdown("---")
    st.header("📤 Export Results")
    
    export_col1, export_col2 = st.columns(2)
    
    with export_col1:
        st.subheader("Download PDF Report")
        pdf_bytes = create_pdf(report)
        if pdf_bytes:
            st.download_button(
                label="📥 Download PDF Report",
                data=pdf_bytes,
                file_name="VidhikAI_Audit_Report.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        else:
            st.warning("PDF generation unavailable")

    with export_col2:
        st.subheader("Download Raw Data")
        json_str = json.dumps(report, indent=2)
        st.download_button(
            label="📥 Download JSON",
            data=json_str,
            file_name="VidhikAI_Audit_Data.json",
            mime="application/json",
            use_container_width=True
        )

    # ---- RAW JSON VIEW ----
    with st.expander("🔍 View Raw JSON Data"):
        st.json(report)

# ==========================
# FOOTER (ORIGINAL FROM FIRST CODE)
# ==========================
st.markdown("---")
st.caption("Vidhik AI • Government of Uttarakhand • DPDP Act • IT Act • 2025")
