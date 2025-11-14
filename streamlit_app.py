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
# MAIN APP
# ==========================

def main():
    st.title("⚖️ Vidhik AI: The Compliance-First Policy Audit")
    st.markdown("### The Governance Gateway for the Government of Uttarakhand")
    st.info("Upload your policy draft (or use the sample text) and click 'Run Audit' to instantly check for legal conflicts, PII risks, and policy bias.")

    # ==========================
    # SIDEBAR
    # ==========================

    st.sidebar.title("Navigation")

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

    placeholder_policy = """[Draft Policy: GO for Digital Service Delivery Platform (DSDP)]

[Clause 3.0: Citizen Enrollment]
All citizens must register their personal details on the DSDP platform.

[Clause 4.1: Data Handling Protocol]
Data collected via the DSDP will be stored securely.

[Clause 5.0: Access and Availability]
Access to DSDP services is available to all citizens."""

    # ==========================
    # MAIN TEXT AREA
    # ==========================

    st.subheader("Policy Draft to Audit:")
    
    # Initialize session state for text
    if 'policy_text' not in st.session_state:
        st.session_state.policy_text = placeholder_policy
    
    policy_input = st.text_area(
        "Policy Text",
        value=st.session_state.policy_text,
        height=300,
        label_visibility="collapsed",
        key="policy_text_area"
    )

    # ==========================
    # FILE UPLOAD SECTION
    # ==========================

    st.markdown("---")
    st.subheader("📁 Upload Policy Document")
    
    uploaded_file = st.file_uploader(
        "Choose a file to replace the current policy text",
        type=['txt', 'pdf', 'docx', 'doc'],
        help="Upload your policy document to replace the text above"
    )

    # Process uploaded file
    if uploaded_file is not None:
        try:
            st.success(f"✅ Uploaded: {uploaded_file.name}")
            
            file_type = uploaded_file.type
            text_content = None
            
            if file_type == "text/plain":
                text_content = process_text_file(uploaded_file)
            elif file_type == "application/pdf":
                text_content = process_pdf_file(uploaded_file)
            elif file_type in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/msword"]:
                text_content = process_docx_file(uploaded_file)
            
            if text_content:
                st.session_state.policy_text = text_content
                st.rerun()
            else:
                st.error("Could not extract text from the uploaded file.")
                
        except Exception as e:
            st.error(f"Error processing file: {e}")

    # ==========================
    # RUN BUTTON SECTION
    # ==========================

    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Run Vidhik AI Audit", type="primary", use_container_width=True):
            if not st.session_state.policy_text.strip():
                st.error("Please enter policy text or upload a file first.")
            else:
                with st.spinner("🔍 Analyzing policy document..."):
                    try:
                        # Try to import the real analyzer, fall back to mock
                        try:
                            from vidhik_engine import analyze_policy as real_analyze_policy
                            final_report = real_analyze_policy(st.session_state.policy_text)
                        except ImportError:
                            st.warning("Using mock analysis - vidhik_engine not available")
                            final_report = analyze_policy(st.session_state.policy_text)
                        
                        st.session_state.report = final_report
                        st.session_state.report_generated = True
                        st.success("✅ Audit Complete!")
                        
                    except Exception as e:
                        st.error(f"Analysis failed: {e}")

    # ==========================
    # REPORT DISPLAY
    # ==========================

    if "report" in st.session_state and st.session_state.get("report_generated", False):
        report = st.session_state.report
        
        st.markdown("---")
        st.header("📊 Audit Report")
        
        # Overall Status
        status = report.get("Overall Status", "Unknown")
        if "FAIL" in status.upper():
            st.error(f"### 📌 Overall Status: {status}")
        elif "PASS" in status.upper():
            st.success(f"### 📌 Overall Status: {status}")
        else:
            st.warning(f"### 📌 Overall Status: {status}")

        # Executive Summary
        st.subheader("Executive Summary")
        st.write(report.get("Executive Summary", "No summary available."))

        # Recommendations
        st.subheader("Actionable Recommendations")
        st.write(report.get("Actionable Recommendations", "No specific recommendations."))

        # Detailed Reports in Tabs
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

        # ==========================
        # PDF DOWNLOAD SECTION
        # ==========================

        st.markdown("---")
        st.header("📄 Export Report")
        
        col1, col2 = st.columns(2)
        
        with col1:
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
                
        with col2:
            st.subheader("Download JSON Data")
            json_str = json.dumps(report, indent=2)
            st.download_button(
                label="📥 Download JSON",
                data=json_str,
                file_name="VidhikAI_Audit_Data.json",
                mime="application/json",
                use_container_width=True
            )

        # Clear button
        if st.button("🗑️ Clear Current Report", use_container_width=True):
            for key in ['report', 'report_generated']:
                st.session_state.pop(key, None)
            st.rerun()

    # ==========================
    # FOOTER
    # ==========================
    st.markdown("---")
    st.caption("Vidhik AI • Government of Uttarakhand • DPDP Act • IT Act • 2025")

# Run the app
if __name__ == "__main__":
    main()
