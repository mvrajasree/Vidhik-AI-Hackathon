import streamlit as st
import json
import tempfile
import os
# Import the core logic from your engine file
from vidhik_engine import analyze_policy

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Vidhik AI: Governance Gateway",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- COLORS AND STYLES ---
# Use Streamlit's built-in success/warning/error colors for impact
FAIL_COLOR = "#FF4B4B" # Red
PASS_COLOR = "#00BFA5" # Teal Green

# --- HEADER AND INTRODUCTION ---
st.title("⚖️ Vidhik AI: The Compliance-First Policy Audit")
st.markdown("### The Governance Gateway for the Government of Uttarakhand")
st.info("Upload your policy draft (or use the sample text) and click 'Run Audit' to instantly check for legal conflicts, PII risks, and policy bias.")

# --- SIDEBAR (THE ENGINE ARCHITECTURE) ---
st.sidebar.title("Vidhik AI Architecture")
st.sidebar.markdown("**Phase 1: The Security Gatekeeper**")
st.sidebar.markdown("✅ PII Redaction & Data Privacy Check (DPDP Act)")
st.sidebar.markdown("**Phase 2: The Legal Analyzer**")
st.sidebar.markdown("✅ Semantic Conflict Detection (FAISS DB)")
st.sidebar.markdown("**Phase 3: The Fairness Auditor**")
st.sidebar.markdown("✅ Linguistic Bias & Inclusivity Check")

# --- FILE UPLOAD SECTION ---
st.sidebar.markdown("---")
st.sidebar.subheader("📁 Upload Policy Document")
uploaded_file = st.sidebar.file_uploader(
    "Choose a file",
    type=['txt', 'pdf', 'docx', 'doc'],
    help="Upload your policy document (TXT, PDF, DOCX, DOC)"
)

# --- INPUT AREA ---
# Placeholder text (the intentionally flawed policy draft)
placeholder_policy = """
[Draft Policy: GO for Digital Service Delivery Platform (DSDP)]

[Clause 3.0: Citizen Enrollment]
All citizens of the state must register their personal details and bank account numbers on the DSDP. Citizens shall, in all instances, only use their Aadhar ID and provide scanned copies of their current utility bill. Mr. Rajesh Kumar, residing at Mandi Road, Dehradun 248001, will be the initial contact for technical queries.

[Clause 4.1: Data Handling Protocol]
Data collected via the DSDP will be stored on a private server maintained by the department. Personal data, including the Aadhar ID, may be retained indefinitely and shared with any other state department upon simple request.

[Clause 5.0: Access and Availability]
Access to DSDP services is restricted solely to citizens who can reliably interface using dedicated, high-speed fiber-optic internet connections and advanced desktop computing hardware.
"""

# Process uploaded file
input_text = ""
if uploaded_file is not None:
    try:
        # Display file details
        st.sidebar.success(f"✅ File uploaded: {uploaded_file.name}")
        st.sidebar.write(f"File type: {uploaded_file.type}")
        st.sidebar.write(f"File size: {uploaded_file.size} bytes")
        
        # Read file content based on file type
        if uploaded_file.type == "text/plain":
            # TXT file
            input_text = str(uploaded_file.read(), "utf-8")
        elif uploaded_file.type == "application/pdf":
            # PDF file - would need PyPDF2 or pdfplumber
            try:
                import PyPDF2
                pdf_reader = PyPDF2.PdfReader(uploaded_file)
                input_text = ""
                for page in pdf_reader.pages:
                    input_text += page.extract_text() + "\n"
            except ImportError:
                st.sidebar.warning("PDF processing requires PyPDF2. Install with: pip install PyPDF2")
                input_text = "[PDF content - install PyPDF2 to process]"
        elif uploaded_file.type in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document", 
                                   "application/msword"]:
            # DOCX or DOC file - would need python-docx
            try:
                import docx
                doc = docx.Document(uploaded_file)
                input_text = ""
                for paragraph in doc.paragraphs:
                    input_text += paragraph.text + "\n"
            except ImportError:
                st.sidebar.warning("DOCX processing requires python-docx. Install with: pip install python-docx")
                input_text = "[DOCX content - install python-docx to process]"
        else:
            st.sidebar.error("Unsupported file type")
            
    except Exception as e:
        st.sidebar.error(f"Error reading file: {str(e)}")
        input_text = placeholder_policy
else:
    input_text = placeholder_policy

# Text area for policy input (shows uploaded content or placeholder)
policy_input = st.text_area(
    "Policy Draft to Audit:",
    value=input_text,
    height=400,
    help="Review and edit the policy text before running the audit"
)

# --- EXECUTION BUTTON ---
if st.button("🚀 Run Vidhik AI Audit", type="primary"):
    if not policy_input.strip():
        st.error("Please enter some policy text to analyze.")
        st.stop()
    
    try:
        # Show loading spinner
        with st.spinner("🔍 Analyzing policy for legal conflicts, bias, and PII risks..."):
            # Call the analyze_policy function
            final_report = analyze_policy(policy_input)
        
        # Store results for display
        st.session_state['report'] = final_report
        st.success("✅ Audit completed successfully!")

    except Exception as e:
        st.error(f"An error occurred during audit: {str(e)}")
        st.stop()

# --- REPORT DISPLAY ---
if 'report' in st.session_state:
    report = st.session_state['report']
    st.markdown("---")
    
    # 1. Overall Status Header (High-Impact)
    overall_status = report.get('Overall Status', 'Unknown')
    status_text = f"**{overall_status}**"
    
    if overall_status in ["Clean", "Low Risk"]:
        st.success(f"## ✅ Policy Status: {status_text}", icon="✅")
    elif overall_status in ["High Risk", "Database Error", "Processing Error"]:
        st.error(f"## ❌ POLICY ALERT: {status_text}", icon="⚠️")
    elif overall_status == "Medium Risk":
        st.warning(f"## ⚠️ Policy Status: {status_text}", icon="⚠️")
    else:
        st.info(f"## Policy Status: {status_text}")

    # 2. Executive Summary (if available)
    if 'Executive Summary' in report:
        st.header("Executive Summary")
        st.markdown(report['Executive Summary'])
    else:
        # Create a simple executive summary from the overall status
        st.header("Executive Summary")
        if overall_status == "Clean":
            st.markdown("The policy draft appears compliant with minimal risks detected across legal, bias, and PII dimensions.")
        elif overall_status == "Medium Risk":
            st.markdown("The policy draft requires attention with moderate risks identified. Review the detailed findings below.")
        elif overall_status == "High Risk":
            st.markdown("**CRITICAL ISSUES DETECTED:** This policy draft contains high-risk elements requiring immediate attention before deployment.")
        else:
            st.markdown("Analysis completed. Review the detailed findings in the sections below.")
    
    st.markdown("---")

    # 3. Actionable Recommendations (Tab View)
    tab1, tab2, tab3 = st.tabs(["⚖️ Legal Conflicts", "🌍 Policy Bias", "🔐 PII & Data Risk"])
    
    with tab1:
        st.subheader("Legal Conflicts and Compliance Violations")
        if 'Actionable Recommendations' in report:
            # Extract legal conflicts section
            rec_text = report['Actionable Recommendations']
            if "### ⚖️ Recommendations for Legal Conflicts" in rec_text:
                legal_section = rec_text.split("### ⚖️ Recommendations for Legal Conflicts")[1]
                if "### 🌍 Recommendations for Inclusive Language" in legal_section:
                    legal_section = legal_section.split("### 🌍 Recommendations for Inclusive Language")[0]
                st.markdown(legal_section)
            else:
                st.markdown(rec_text)
        else:
            st.info("No legal recommendations available.")
        
        # Display the Conflicting Laws from the raw report
        if (report.get('Raw Reports', {}).get('Conflict Report', {}).get('Conflicting Laws')):
            st.markdown("---")
            st.markdown("**Detailed Conflict Analysis:**")
            for conflict in report['Raw Reports']['Conflict Report']['Conflicting Laws']:
                with st.expander(f"Conflict #{conflict.get('Rank', 'N/A')} - Similarity: {conflict.get('Similarity Score', 'N/A')} - Risk: {conflict.get('Risk Level', 'N/A')}"):
                    st.write(f"**Legal Provision:** {conflict.get('Legal Provision', 'N/A')}")
        
    with tab2:
        st.subheader("Ethical Audit: Exclusionary Language")
        if 'Actionable Recommendations' in report:
            # Extract bias section
            rec_text = report['Actionable Recommendations']
            if "### 🌍 Recommendations for Inclusive Language" in rec_text:
                bias_section = rec_text.split("### 🌍 Recommendations for Inclusive Language")[1]
                if "### 🔒 Recommendations for PII Risk" in bias_section:
                    bias_section = bias_section.split("### 🔒 Recommendations for PII Risk")[0]
                st.markdown(bias_section)
            else:
                st.info("No bias recommendations in this format.")
        else:
            st.info("No bias recommendations available.")
            
        # Display the flagged phrases from the raw report
        if (report.get('Raw Reports', {}).get('Bias Report', {}).get('flagged_phrases')):
            st.markdown("---")
            st.markdown("**Flagged Phrases:**")
            for flag in report['Raw Reports']['Bias Report']['flagged_phrases']:
                st.warning(f"**'{flag.get('phrase', 'N/A')}'** - Category: {flag.get('lexicon', 'N/A')}")

    with tab3:
        st.subheader("Data Privacy and PII Risk")
        pii_report = report.get('Raw Reports', {}).get('PII Report', {})
        pii_status = pii_report.get('status', 'Unknown')
        
        if pii_status == "PII Found":
            st.error(f"**Status:** {pii_status}. High-risk PII was detected. Ensure the PII redaction layer is permanently applied before public release.")
            
            # Show detected PII items
            if pii_report.get('detected_items'):
                st.markdown("**Detected PII Items:**")
                for pii_item in pii_report['detected_items']:
                    st.write(f"- **{pii_item.get('type', 'Unknown')}:** `{pii_item.get('value', 'N/A')}`")
        else:
            st.success(f"**Status:** {pii_status}. Document appears clean of PII.")
        
        # Show PII recommendations
        if 'Actionable Recommendations' in report and "### 🔒 Recommendations for PII Risk" in report['Actionable Recommendations']:
            st.markdown("---")
            pii_section = report['Actionable Recommendations'].split("### 🔒 Recommendations for PII Risk")[1]
            st.markdown(pii_section)

    # 4. Raw Report (Collapsible)
    with st.expander("📊 View Raw Analysis Report"):
        st.json(report)

# --- FOOTER ---
st.markdown("---")
st.markdown(
    "**Vidhik AI** | Built for the Government of Uttarakhand | "
    "Compliance Framework: DPDP Act 2023, IT Act 2000, Constitutional Principles"
)
