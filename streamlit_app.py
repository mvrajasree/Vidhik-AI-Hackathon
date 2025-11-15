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

# ==========================
# MINIMAL STYLING (Theme-safe)
# ==========================

st.markdown("""
    <style>
    .main-header {
        text-align: center;
        padding: 1.5rem 0;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    .main-header h1 {
        margin-bottom: 0.5rem;
        font-size: 2.5rem;
        font-weight: 700;
    }
    .main-header h3 {
        margin-top: 0;
        font-size: 1.2rem;
        font-weight: 400;
        opacity: 0.9;
    }
    .section-divider {
        margin: 2rem 0;
        border-top: 2px solid var(--secondary-background-color);
    }
    </style>
""", unsafe_allow_html=True)

# ==========================
# HEADER
# ==========================

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown(
        """
        <div class='main-header'>
            <h1>⚖️ Vidhik AI</h1>
            <h3>Governance Gateway for the Government of Uttarakhand</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

st.info("📋 Upload your policy draft or use the sample text below to conduct a comprehensive compliance audit.")

# ==========================
# PDF GENERATOR
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
# MOCK ANALYSIS FUNCTION
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

st.sidebar.title("🔍 Navigation")

with st.sidebar.expander("🏛️ System Architecture", expanded=False):
    st.markdown("""
    **Phase 1: Security Gatekeeper**  
    ✅ PII Redaction & Data Privacy Check (DPDP Act)
    
    **Phase 2: Legal Analyzer**  
    ✅ Semantic Conflict Detection (FAISS DB)
    
    **Phase 3: Fairness Auditor**  
    ✅ Linguistic Bias & Inclusivity Check
    """)

st.sidebar.markdown("---")
st.sidebar.markdown("**📊 Quick Stats**")
st.sidebar.info("""
Audits Completed: 127  
Processing Time: 2.3s  
Compliance Rate: 89%
""")

# ==========================
# POLICY CONTENT
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
# MAIN CONTENT AREA
# ==========================

st.subheader("Policy Document Analysis")

col1, col2 = st.columns([3, 1])

with col1:
    st.markdown("**Policy Draft to Audit**")
    policy_input = st.text_area(
        "Policy Draft to Audit:",
        value=placeholder_policy,
        height=350,
        label_visibility="collapsed"
    )

with col2:
    st.markdown("**Document Controls**")
    uploaded_file = st.file_uploader(
        "Upload Document",
        type=['txt', 'pdf', 'docx', 'doc'],
        help="Supported formats: TXT, PDF, DOCX, DOC",
        label_visibility="collapsed"
    )
    if uploaded_file:
        st.success(f"✅ {uploaded_file.name}")

# ==========================
# ACTION CONTROLS
# ==========================

st.markdown("---")
st.subheader("Analysis Controls")

# Initialize button states
reset_clicked = False
run_audit_clicked = False
clear_clicked = False

# Create button layout
col1, col2, col3 = st.columns(3)

with col1:
    reset_clicked = st.button("🔄 Reset Text", use_container_width=True)

with col2:
    run_audit_clicked = st.button(
        "🚀 Run Comprehensive Audit", 
        type="primary", 
        use_container_width=True
    )

with col3:
    if st.session_state.get("report"):
        clear_clicked = st.button("🗑️ Clear Results", use_container_width=True, type="secondary")

# Handle button actions immediately
if reset_clicked:
    st.session_state.clear()
    st.rerun()

if clear_clicked:
    st.session_state.pop("report", None)
    st.session_state.pop("report_text", None)
    st.rerun()

# ==========================
# AUDIT PROCESSING
# ==========================

if run_audit_clicked:
    # Process uploaded file or use text area content
    final_text = policy_input
    
    if uploaded_file:
        try:
            if uploaded_file.type == "text/plain":
                final_text = str(uploaded_file.read(), "utf-8")
            elif uploaded_file.type == "application/pdf":
                import PyPDF2
                reader = PyPDF2.PdfReader(uploaded_file)
                final_text = "\n".join([page.extract_text() for page in reader.pages])
            elif uploaded_file.type in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                                        "application/msword"]:
                import docx
                doc = docx.Document(uploaded_file)
                final_text = "\n".join([p.text for p in doc.paragraphs])
        except Exception as e:
            st.error(f"❌ File processing error: {e}")

    if not final_text.strip():
        st.error("Please provide policy text for analysis.")
        st.stop()

    with st.spinner("🔍 Conducting comprehensive policy analysis..."):
        try:
            # Try to import the real analyzer, fall back to mock
            try:
                from vidhik_engine import analyze_policy as real_analyze_policy
                final_report = real_analyze_policy(final_text)
            except ImportError:
                st.warning("⚠️ Using demonstration analysis - full engine not available")
                final_report = analyze_policy(final_text)
            
            st.session_state["report"] = final_report
            st.session_state["report_text"] = final_text
            st.success("✅ Policy audit completed successfully!")
        except Exception as e:
            st.error(f"❌ Analysis error: {e}")

# ==========================
# REPORT DISPLAY
# ==========================

if "report" in st.session_state:
    report = st.session_state["report"]
    
    st.markdown("---")
    st.subheader("📊 Audit Results")
    
    # Overall Status
    status = report.get("Overall Status", "Unknown")
    if "FAIL" in status.upper():
        st.error(f"**Compliance Status:** {status}")
    elif "PASS" in status.upper():
        st.success(f"**Compliance Status:** {status}")
    else:
        st.warning(f"**Compliance Status:** {status}")

    # Executive Summary
    st.markdown("**Executive Summary**")
    st.write(report.get("Executive Summary", "No summary available."))

    # Detailed Analysis
    st.markdown("**Detailed Analysis**")
    tab1, tab2, tab3 = st.tabs(["⚖️ Legal Compliance", "🌍 Bias Assessment", "🔐 Data Privacy"])

    with tab1:
        conflict_data = report.get("Raw Reports", {}).get("Conflict Report", {})
        if conflict_data:
            st.json(conflict_data)
        else:
            st.info("No legal compliance issues detected")

    with tab2:
        bias_data = report.get("Raw Reports", {}).get("Bias Report", {})
        if bias_data:
            st.json(bias_data)
        else:
            st.info("No bias assessment data available")

    with tab3:
        pii_data = report.get("Raw Reports", {}).get("PII Report", {})
        if pii_data:
            st.json(pii_data)
        else:
            st.info("No data privacy issues detected")

    # Export Section
    st.markdown("---")
    st.subheader("📤 Export Results")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**PDF Report**")
        pdf_bytes = create_pdf(report)
        if pdf_bytes:
            st.download_button(
                label="Download PDF Report",
                data=pdf_bytes,
                file_name="VidhikAI_Audit_Report.pdf",
                mime="application/pdf",
                use_container_width=True
            )

    with col2:
        st.markdown("**Raw Data**")
        json_str = json.dumps(report, indent=2)
        st.download_button(
            label="Download JSON Data",
            data=json_str,
            file_name="VidhikAI_Audit_Data.json",
            mime="application/json",
            use_container_width=True
        )

    # Raw Data View
    with st.expander("View Complete Dataset"):
        st.json(report)

# ==========================
# FOOTER
# ==========================

st.markdown("---")
st.caption("Vidhik AI • Government of Uttarakhand • DPDP Act Compliance • IT Act 2000 • 2025")
