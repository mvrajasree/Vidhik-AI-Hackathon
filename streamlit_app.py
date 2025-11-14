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
# CLEAN STYLING
# ==========================

st.markdown("""
    <style>
    .main-header {
        text-align: center;
        margin-top: -2rem;
        margin-bottom: 1rem;
        padding: 1.5rem 0;
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        border-radius: 10px;
        color: white;
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
    .section-header {
        border-bottom: 2px solid #1e3c72;
        padding-bottom: 0.5rem;
        margin-bottom: 1rem;
        color: #1e3c72 !important;
        font-weight: 600;
        font-size: 1.4rem;
    }
    .action-card {
        background-color: #f8fafc;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #1e3c72;
        margin-bottom: 1rem;
    }
    .stButton button {
        border-radius: 8px;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    .success-msg {
        background-color: #f0fff4;
        border: 1px solid #9ae6b4;
        border-radius: 8px;
        padding: 0.75rem;
        margin: 0.5rem 0;
        color: #22543d;
    }
    .report-section {
        background-color: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border: 1px solid #e2e8f0;
    }
    .compact-section {
        margin: 0.5rem 0;
        padding: 0;
    }
    /* Remove extra padding from Streamlit elements */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    .stTextArea textarea {
        border: 2px solid #e2e8f0;
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================
# PROFESSIONAL HEADER
# ==========================

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
# SIMPLIFIED PDF GENERATOR
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
# CLEAN SIDEBAR
# ==========================

st.sidebar.markdown(
    """
    <div style='text-align: center; margin-bottom: 1rem;'>
        <h3 style='color: #1e3c72;'>🔍 Navigation</h3>
    </div>
    """,
    unsafe_allow_html=True
)

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
# COMPACT MAIN CONTENT AREA
# ==========================

st.markdown("### Policy Document Analysis")

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
        help="Supported formats: TXT, PDF, DOCX, DOC"
    )
    if uploaded_file:
        st.success(f"✅ {uploaded_file.name}")

# ==========================
# ALIGNED ACTION CONTROLS
# ==========================

st.markdown("---")

# Create a container for aligned buttons
button_col1, button_col2, button_col3 = st.columns([1, 2, 1])

with button_col1:
    use_sample = st.checkbox("Use sample policy", value=True)
    reset_clicked = st.button("🔄 Reset Text", use_container_width=True)

with button_col2:
    # Center the main audit button
    run_audit = st.button(
        "🚀 Run Comprehensive Audit", 
        type="primary", 
        use_container_width=True,
        help="Initiate full policy analysis"
    )

with button_col3:
    # Right-align the clear button
    if st.session_state.get("report"):
        clear_clicked = st.button("🗑️ Clear Results", use_container_width=True, type="secondary")
    else:
        # Placeholder to maintain alignment
        st.empty()

# Handle button actions
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

if run_audit:
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
            final_text = input_text if input_text else policy_input
        except Exception as e:
            st.error(f"❌ File processing error: {e}")
            final_text = policy_input
    else:
        final_text = policy_input

    if not final_text.strip():
        st.error("Please provide policy text for analysis.")
        st.stop()

    with st.spinner("🔍 Conducting comprehensive policy analysis..."):
        try:
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
# CLEAN REPORT DISPLAY
# ==========================

if "report" in st.session_state:
    report = st.session_state["report"]
    
    st.markdown("---")
    st.markdown("### 📊 Audit Results")
    
    # Overall Status - Compact
    status_col1, status_col2 = st.columns([1, 4])
    with status_col1:
        st.markdown("**Compliance Status**")
    with status_col2:
        status = report.get("Overall Status", "Unknown")
        if "FAIL" in status.upper():
            st.error(f"**{status}**")
        elif "PASS" in status.upper():
            st.success(f"**{status}**")
        else:
            st.warning(f"**{status}**")

    # Executive Summary - Compact
    st.markdown("**Executive Summary**")
    st.write(report.get("Executive Summary", "No summary available."))

    # Detailed Analysis - Compact
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

    # Export Section - Compact
    st.markdown("---")
    st.markdown("### 📤 Export Results")
    
    export_col1, export_col2 = st.columns(2)
    
    with export_col1:
        st.markdown("**PDF Report**")
        pdf_bytes = create_pdf(report)
        if pdf_bytes:
            st.download_button(
                label="Download PDF",
                data=pdf_bytes,
                file_name="VidhikAI_Audit_Report.pdf",
                mime="application/pdf",
                use_container_width=True
            )

    with export_col2:
        st.markdown("**Raw Data**")
        json_str = json.dumps(report, indent=2)
        st.download_button(
            label="Download JSON",
            data=json_str,
            file_name="VidhikAI_Audit_Data.json",
            mime="application/json",
            use_container_width=True
        )

    # Raw Data View
    with st.expander("View Complete Dataset"):
        st.json(report)

# ==========================
# CLEAN FOOTER
# ==========================

st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #1e3c72; font-size: 0.9rem; padding: 1rem; font-weight: 500;'>
        <strong>Vidhik AI</strong> • Government of Uttarakhand • DPDP Act Compliance • IT Act 2000 • 2025
    </div>
    """,
    unsafe_allow_html=True
)
