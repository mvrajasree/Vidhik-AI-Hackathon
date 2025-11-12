import streamlit as st
import json
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

input_text = st.text_area(
    "Policy Draft to Audit:",
    value=placeholder_policy,
    height=400
)

# --- EXECUTION BUTTON ---
if st.button("🚀 Run Vidhik AI Audit", type="primary"):
    # Mocking the reports since we don't have the live FAISS connection here
    # In a real setup, this function would return the actual report.
    try:
        # Assuming analyze_policy takes the text and returns the final report dictionary
        final_report = analyze_policy(input_text)
        
        # Store results for display
        st.session_state['report'] = final_report

    except Exception as e:
        st.error(f"An error occurred during audit: {e}")
        st.stop()


# --- REPORT DISPLAY ---
if 'report' in st.session_state:
    report = st.session_state['report']
    st.markdown("---")
    
    # 1. Overall Status Header (High-Impact)
    status_text = f"**{report['Overall Status']}**"
    if report['Overall Status'] == "PASS":
        st.success(f"## ✅ Policy Status: {status_text}", icon="✅")
    else:
        st.error(f"## ❌ POLICY ALERT: {status_text}", icon="⚠️")

    # 2. Executive Summary
    st.header("Executive Summary")
    st.markdown(report['Executive Summary'])
    st.markdown("---")

    # 3. Actionable Recommendations (Tab View)
    tab1, tab2, tab3 = st.tabs(["⚖️ Legal Conflicts", "🚫 Policy Bias", "🔐 PII & Data Risk"])
    
    with tab1:
        st.subheader("Legal Conflicts and Compliance Violations")
        st.markdown(report['Actionable Recommendations'].split("### Recommendations for Bias Flags")[0])
        # Display the Conflicting Laws from the raw report
        if report['Raw Reports']['Conflict Report']['Conflicting Laws']:
            st.markdown("---")
            st.markdown("**Raw Conflict Citations:**")
            for conflict in report['Raw Reports']['Conflict Report']['Conflicting Laws']:
                st.code(f"Found: {conflict['Law Citation']} conflict with clause: \"{conflict['New Policy Clause'][:60]}...\"", language="")
        
    with tab2:
        st.subheader("Ethical Audit: Exclusionary Language")
        st.markdown(report['Actionable Recommendations'].split("### Recommendations for Bias Flags")[1].split("### Recommendations for Legal Conflicts")[0])
        # Display the flagged phrases from the raw report
        if report['Raw Reports']['Bias Report']['flagged_phrases']:
            st.markdown("---")
            st.markdown("**Flagged Phrases:**")
            for flag in report['Raw Reports']['Bias Report']['flagged_phrases']:
                st.warning(f"Phrase: '{flag['phrase']}' (Lexicon: {flag['lexicon']})")

    with tab3:
        st.subheader("Data Privacy and PII Risk")
        pii_status = report['Raw Reports']['PII Redaction Status']
        if pii_status == "PII Found":
             st.warning(f"**Status:** {pii_status}. High-risk PII was detected. Ensure the PII redaction layer is permanently applied before public release.")
        else:
             st.success(f"**Status:** {pii_status}. Document appears clean of PII.")
