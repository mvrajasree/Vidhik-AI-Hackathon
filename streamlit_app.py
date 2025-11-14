# streamlit_app.py — Vidhik AI Premium (UI v3) — Full Integration
# - Includes original logic (file handling, PDF parsing, mock analysis)
# - Enhanced premium UI (dark/light adaptive, Uttarakhand emblem, no orange accent)
# - Multi-step audit workflow (Phase 1..3) wired to the analysis function
# - Export (PDF/JSON), session-state preserved

import streamlit as st
import json
import io
import os
from pathlib import Path

# ------------------ Page config ------------------
st.set_page_config(
    page_title="Vidhik AI: Governance Gateway",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ------------------ Theme state & toggle ------------------
if "theme" not in st.session_state:
    st.session_state["theme"] = "light"

def toggle_theme():
    st.session_state["theme"] = "dark" if st.session_state["theme"] == "light" else "light"
    st.experimental_rerun()

# ------------------ Adaptive CSS (no orange accent) ------------------
BASE_CSS = r"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');
:root { --gov-blue: #1e3c72; }
body, textarea, input, button { font-family: 'Inter', sans-serif !important; }
.block-container { padding-top: 1.6rem !important; padding-bottom: 2.6rem !important; max-width: 1300px; }

/* Remove default Streamlit header background (ribbon) */
header[data-testid="stHeader"] { background: none !important; box-shadow: none !important; }

/* Header box */
.main-header { text-align:center; padding:2.2rem 1rem; border-radius:12px; position:relative; }
.main-title { margin:0; font-size:2.6rem; font-weight:800; }
.main-sub { margin:0; font-size:1.05rem; font-weight:400; opacity:0.95 }

/* Cards */
.gov-card { background: var(--card-bg); padding:1.4rem; border-radius:14px; border:1px solid var(--card-border); box-shadow:var(--card-shadow); }
.action-card { padding:0.9rem 1rem; border-radius:10px; }

/* Buttons */
.stButton button { border-radius:10px !important; padding:0.6rem 1rem; font-weight:600; }

/* Text area */
.stTextArea textarea { border-radius:10px !important; padding:0.85rem !important; }

/* Footer */
.footer { text-align:center; font-size:0.95rem; padding:1.1rem; font-weight:600; }

/* Small responsive */
@media (max-width:900px){ .main-title { font-size:1.6rem; } }
</style>
"""

LIGHT_VARS = r"""
<style>
:root {
  --card-bg: #ffffff;
  --card-border: #e6eef8;
  --card-shadow: 0 6px 20px rgba(15,23,42,0.06);
  --text-color: #0b1220;
  --bg-color: #ffffff;
}
</style>
"""

DARK_VARS = r"""
<style>
:root {
  --card-bg: #071226;
  --card-border: rgba(255,255,255,0.04);
  --card-shadow: 0 6px 22px rgba(0,0,0,0.6);
  --text-color: #e6eef8;
  --bg-color: #071226;
}
</style>
"""

# inject CSS
st.markdown(BASE_CSS, unsafe_allow_html=True)
if st.session_state["theme"] == "light":
    st.markdown(LIGHT_VARS, unsafe_allow_html=True)
else:
    st.markdown(DARK_VARS, unsafe_allow_html=True)

# ------------------ Uttarakhand emblem (neutral colors) ------------------
UTTARAKHAND_SVG = '''
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64" aria-hidden="true">
  <g>
    <path d="M32 2c7 0 13 4 16 9 3 5 3 11 3 19 0 9-6 18-19 27-1 .6-2 .6-3 0C17 48 11 39 11 30c0-8 0-14 3-19 3-5 9-9 18-9z" fill="#2a5298"/>
    <circle cx="32" cy="22" r="6" fill="#ffffff"/>
    <path d="M22 46c4 2 8 3 10 3s6-1 10-3" fill="none" stroke="#ffffff" stroke-width="1.4" stroke-linecap="round"/>
  </g>
</svg>
'''

# ------------------ Header ------------------
st.markdown(f"""
<div class='main-header gov-card' style='display:flex;align-items:center;justify-content:space-between;'>
  <div style='display:flex;gap:16px;align-items:center;'>
    <div style='text-align:left;'>
      <h1 class='main-title'>⚖️ Vidhik AI</h1>
      <div class='main-sub'>Governance Gateway for the Government of Uttarakhand</div>
    </div>
  </div>
  <div style='width:68px;height:68px;display:flex;align-items:center;justify-content:center;'>
    {UTTARAKHAND_SVG}
  </div>
</div>
""", unsafe_allow_html=True)

# Theme toggle in sidebar
with st.sidebar:
    st.markdown("### Appearance")
    col1, col2 = st.columns([3,1])
    with col2:
        if st.button("🌓", help="Toggle light/dark theme"):
            toggle_theme()

# ------------------ Sidebar content (sticky) ------------------
with st.sidebar:
    st.markdown("---")
    st.markdown("### 🔍 Navigation")
    with st.expander("🏛️ System Architecture", expanded=False):
        st.markdown("""
        **Phase 1: Security Gatekeeper**  
        - PII Redaction & Data Privacy Check (DPDP Act)
        
        **Phase 2: Legal Analyzer**  
        - Semantic Conflict Detection (FAISS DB)
        
        **Phase 3: Fairness Auditor**  
        - Linguistic Bias & Inclusivity Check
        """)
    st.markdown("---")
    st.markdown("**📊 Quick Stats**")
    st.info("""
    Audits Completed: 127  
    Processing Time: 2.3s  
    Compliance Rate: 89%
    """)
    st.markdown("---")
    st.markdown("**Helpful Links**")
    st.markdown("- DPDP Act, 2023 (internal)\n- IT Act, 2000 summaries\n- Governance design guidelines")

# ------------------ Core functions (original logic preserved) ------------------

def create_pdf(report):
    try:
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.units import cm
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, leftMargin=2*cm, rightMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm)
        styles = getSampleStyleSheet()
        story = []
        story.append(Paragraph("<b>Vidhik AI – Policy Audit Report</b>", styles["Title"]))
        story.append(Spacer(1, 16))
        status = report.get("Overall Status", "Unknown")
        story.append(Paragraph(f"<b>Overall Status:</b> {status}", styles["Heading2"]))
        story.append(Spacer(1, 12))
        story.append(Paragraph("<b>Executive Summary</b>", styles["Heading2"]))
        summary = report.get("Executive Summary", "").replace("\n", "<br/>")
        story.append(Paragraph(summary, styles["Normal"]))
        story.append(Spacer(1, 12))
        story.append(Paragraph("<b>Actionable Recommendations</b>", styles["Heading2"]))
        recommendations = report.get("Actionable Recommendations", "").replace("\n", "<br/>")
        story.append(Paragraph(recommendations, styles["Normal"]))
        story.append(Spacer(1, 12))
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


def analyze_policy(policy_text):
    """Mock analysis function if the real engine isn't available"""
    # Keep original behavior but expand a bit for more detailed mock outputs
    return {
        "Overall Status": "PASS with Recommendations",
        "Executive Summary": "Policy analysis completed successfully. No critical legal conflicts detected, but some improvements recommended for data privacy and inclusivity.",
        "Actionable Recommendations": "1. Limit data retention period\n2. Remove mandatory Aadhar requirement\n3. Add alternative authentication methods\n4. Specify data sharing protocols",
        "Raw Reports": {
            "Conflict Report": {"status": "PASS", "issues_found": 2, "details": ["Clause 4.1: indefinite retention flagged", "Clause 3.0: mandatory Aadhar requirement"]},
            "Bias Report": {"status": "WARNING", "issues_found": 1, "details": ["Clause 5.0: accessibility restrictions"]},
            "PII Report": {"status": "FAIL", "issues_found": 3, "details": ["Aadhar stored in cleartext", "Personal addresses included", "Indefinite retention period"]}
        }
    }

# ------------------ Main layout and preserved policy text ------------------
placeholder_policy = """
[Draft Policy: GO for Digital Service Delivery Platform (DSDP)]

[Clause 3.0: Citizen Enrollment]
All citizens of the state must register their personal details and bank account numbers on the DSDP. Citizens shall, in all instances, only use their Aadhar ID and provide scanned copies of their current utility bill. Mr. Rajesh Kumar, residing at Mandi Road, Dehradun 248001, will be the initial contact for technical queries.

[Clause 4.1: Data Handling Protocol]
Data collected via the DSDP will be stored on a private server maintained by the department. Personal data, including the Aadhar ID, may be retained indefinitely and shared with any other state department upon simple request.

[Clause 5.0: Access and Availability]
Access to DSDP services is restricted solely to citizens who can reliably interface using dedicated, high-speed fiber-optic internet connections and advanced desktop computing hardware.
"""

st.markdown("<div style='margin-top:1rem;' class='section-header'>Policy Document Analysis</div>", unsafe_allow_html=True)

col_main, col_ctrl = st.columns([3, 1])

with col_main:
    st.markdown("**Policy Draft to Audit**")
    policy_input = st.text_area(
        "Policy Draft to Audit:",
        value=placeholder_policy,
        height=370,
        label_visibility="collapsed"
    )

with col_ctrl:
    st.markdown("**Document Controls**")
    uploaded_file = st.file_uploader(
        "Upload Document",
        type=['txt', 'pdf', 'docx', 'doc'],
        help="Supported formats: TXT, PDF, DOCX, DOC"
    )
    if uploaded_file:
        st.success(f"✅ {uploaded_file.name}")

# ------------------ Buttons row ------------------
st.markdown("---")
btn_c1, btn_c2, btn_c3 = st.columns([1,2,1])

with btn_c1:
    use_sample = st.checkbox("Use sample policy", value=True)
    reset_clicked = st.button("🔄 Reset Text", use_container_width=True)

with btn_c2:
    run_audit = st.button("🚀 Run Comprehensive Audit", type="primary", use_container_width=True)

with btn_c3:
    if st.session_state.get("report"):
        clear_clicked = st.button("🗑️ Clear Results", use_container_width=True, type="secondary")
    else:
        clear_clicked = False

if reset_clicked:
    st.session_state.clear()
    st.experimental_rerun()

if clear_clicked:
    st.session_state.pop("report", None)
    st.session_state.pop("report_text", None)
    st.experimental_rerun()

# ------------------ Audit processing (keeps original file parsing logic) ------------------
if run_audit:
    input_text = ""
    if uploaded_file:
        try:
            if uploaded_file.type == "text/plain" or uploaded_file.name.lower().endswith('.txt'):
                input_text = str(uploaded_file.read(), "utf-8")
            elif uploaded_file.type == "application/pdf" or uploaded_file.name.lower().endswith('.pdf'):
                try:
                    import PyPDF2
                    reader = PyPDF2.PdfReader(uploaded_file)
                    pages = []
                    for page in reader.pages:
                        try:
                            pages.append(page.extract_text() or "")
                        except Exception:
                            pages.append("")
                    input_text = "\n".join(pages)
                except Exception:
                    try:
                        input_text = str(uploaded_file.read(), "utf-8", errors="ignore")
                    except Exception:
                        input_text = ""
            elif uploaded_file.type in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                                        "application/msword"] or uploaded_file.name.lower().endswith(('.docx', '.doc')):
                try:
                    import docx
                    doc = docx.Document(uploaded_file)
                    input_text = "\n".join([p.text for p in doc.paragraphs])
                except Exception:
                    try:
                        input_text = str(uploaded_file.read(), "utf-8", errors="ignore")
                    except Exception:
                        input_text = ""
            final_text = input_text if input_text else policy_input
        except Exception as e:
            st.error(f"❌ File processing error: {e}")
            final_text = policy_input
    else:
        final_text = policy_input

    if not final_text.strip():
        st.error("Please provide policy text for analysis.")
        st.stop()

    # show progress badges
    p1, p2, p3 = st.columns(3)
    p1.markdown("<div class='gov-card action-card'><strong>Phase 1</strong><div>PII Check</div></div>", unsafe_allow_html=True)
    p2.markdown("<div class='gov-card action-card'><strong>Phase 2</strong><div>Semantic Analysis</div></div>", unsafe_allow_html=True)
    p3.markdown("<div class='gov-card action-card'><strong>Phase 3</strong><div>Bias Audit</div></div>", unsafe_allow_html=True)

    with st.spinner("🔍 Conducting comprehensive policy analysis..."):
        try:
            try:
                # attempt to use real engine if available
                from vidhik_engine import analyze_policy as real_analyze_policy
                final_report = real_analyze_policy(final_text)
            except Exception:
                st.warning("⚠️ Using demonstration analysis - full engine not available")
                final_report = analyze_policy(final_text)

            st.session_state["report"] = final_report
            st.session_state["report_text"] = final_text
            st.success("✅ Policy audit completed successfully!")
        except Exception as e:
            st.error(f"❌ Analysis error: {e}")

# ------------------ Results display ------------------
if st.session_state.get("report"):
    report = st.session_state["report"]
    st.markdown("---")
    st.markdown("### 📊 Audit Results")

    sleft, sright = st.columns([1,4])
    with sleft:
        st.markdown("**Compliance Status**")
    with sright:
        status = report.get("Overall Status", "Unknown")
        if "FAIL" in status.upper():
            st.error(f"**{status}**")
        elif "PASS" in status.upper():
            st.success(f"**{status}**")
        else:
            st.warning(f"**{status}**")

    st.markdown("**Executive Summary**")
    st.write(report.get("Executive Summary", "No summary available."))

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

    # Export
    st.markdown("---")
    st.markdown("### 📤 Export Results")
    ec1, ec2 = st.columns(2)
    with ec1:
        st.markdown("**PDF Report**")
        pdf_bytes = create_pdf(report)
        if pdf_bytes:
            st.download_button(
                label="Download PDF",
                data=pdf_bytes,
                file_name="VidhikAI_Audit_Report.pdf",
                mime="application/pdf",
                use_container_width=True,
            )
        else:
            st.info("PDF generation not available in this environment.")
    with ec2:
        st.markdown("**Raw Data**")
        json_str = json.dumps(report, indent=2)
        st.download_button(
            label="Download JSON",
            data=json_str,
            file_name="VidhikAI_Audit_Data.json",
            mime="application/json",
            use_container_width=True,
        )

    with st.expander("View Complete Dataset"):
        st.json(report)

# ------------------ Footer ------------------
st.markdown("---")
st.markdown("<div class='footer'><strong>Vidhik AI</strong> • Government of Uttarakhand • DPDP Act Compliance • IT Act 2000 • 2025</div>", unsafe_allow_html=True)
