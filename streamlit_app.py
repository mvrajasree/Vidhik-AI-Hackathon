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
# THEME / MODE TOGGLE
# ==========================
if "theme" not in st.session_state:
    st.session_state["theme"] = "light"

def toggle_theme():
    st.session_state["theme"] = "dark" if st.session_state["theme"] == "light" else "light"

# ==========================
# PREMIUM UI (LIGHT & DARK)
# ==========================
LIGHT_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');

body, textarea, input, button {
    font-family: "Inter", sans-serif !important;
}
.block-container {
    padding-top: 1.5rem !important;
    padding-bottom: 2.5rem !important;
    max-width: 1300px;
}

/* HEADER */
.main-header {
    text-align: center;
    padding: 2.6rem 0 3.1rem 0;
    background: linear-gradient(135deg, #1e3c72 0%, #233b82 40%, #2a5298 100%);
    border-radius: 18px;
    color: white;
    box-shadow: 0 8px 22px rgba(0,0,0,0.18);
    border: 1px solid rgba(255,255,255,0.10);
    position: relative;
}
.main-header h1 {
    margin-bottom: 0.2rem;
    font-size: 2.85rem;
    font-weight: 800;
}
.main-header h3 {
    margin: 0;
    font-size: 1.15rem;
    font-weight: 400;
    opacity: 0.95;
}
.main-header .emblem {
    position: absolute;
    right: 28px;
    top: 18px;
    width: 64px;
    height: 64px;
}

/* SECTION HEADER */
.section-header {
    border-bottom: 2px solid #1e3c72;
    padding-bottom: 0.45rem;
    margin-bottom: 1rem;
    margin-top: 1.5rem;
    color: #1e3c72 !important;
    font-weight: 700;
    font-size: 1.35rem;
}

/* CARDS */
.action-card {
    background-color: #f9fafb;
    padding: 1.4rem;
    border-radius: 12px;
    border-left: 4px solid #274d9b;
    margin-bottom: 1rem;
    box-shadow: 0 4px 14px rgba(0,0,0,0.06);
    transition: all 0.25s ease;
}
.action-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 22px rgba(0,0,0,0.10);
}

.gov-card {
    background: #ffffff;
    padding: 1.6rem;
    border-radius: 14px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.06);
    border: 1px solid #e5e7eb;
}

/* Buttons */
.stButton button {
    border-radius: 10px !important;
    padding: 0.6rem 1rem;
    font-size: 0.95rem;
    font-weight: 600;
    border: none;
    background: #1e3c72;
    color: white;
    transition: all 0.25s ease;
}
.stButton button:hover {
    background: #294892;
    transform: translateY(-2px);
    box-shadow: 0 8px 18px rgba(0,0,0,0.14);
}

.stButton > button[kind="secondary"] {
    background: #eef2f7 !important;
    color: #1e3c72 !important;
}
.stButton > button[kind="secondary"]:hover {
    background: #e1e8f3 !important;
}

/* Text area */
.stTextArea textarea {
    border: 2px solid #d1d5db !important;
    border-radius: 10px !important;
    font-size: 0.98rem;
    line-height: 1.5;
    padding: 0.85rem !important;
    transition: all 0.25s ease;
}
.stTextArea textarea:focus {
    border-color: #1e3c72 !important;
    box-shadow: 0 0 0 3px rgba(30,60,114,0.18);
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #f8fafc;
    border-right: 1px solid #e6eef8;
    padding-top: 1.6rem;
}

/* Footer */
.footer {
    text-align: center;
    color: #1e3c72;
    font-size: 0.95rem;
    padding: 1.2rem;
    font-weight: 600;
}

/* Small responsive tweaks */
@media (max-width: 900px) {
    .main-header h1 { font-size: 2rem; }
    .main-header .emblem { display: none; }
}
</style>
"""

DARK_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');
body, textarea, input, button {
    font-family: "Inter", sans-serif !important;
    background-color: #0b1020 !important;
    color: #e6eef8 !important;
}
.block-container {
    padding-top: 1.5rem !important;
    padding-bottom: 2.5rem !important;
    max-width: 1300px;
}

/* HEADER */
.main-header {
    text-align: center;
    padding: 2.6rem 0 3.1rem 0;
    background: linear-gradient(135deg, #0f1724 0%, #142032 40%, #16283a 100%);
    border-radius: 18px;
    color: #e6eef8;
    box-shadow: 0 8px 22px rgba(0,0,0,0.6);
    border: 1px solid rgba(255,255,255,0.04);
    position: relative;
}
.main-header h1 {
    margin-bottom: 0.2rem;
    font-size: 2.85rem;
    font-weight: 800;
}
.main-header h3 {
    margin: 0;
    font-size: 1.15rem;
    font-weight: 400;
    opacity: 0.9;
}
.main-header .emblem {
    position: absolute;
    right: 28px;
    top: 18px;
    width: 64px;
    height: 64px;
    filter: brightness(1.15) contrast(0.9);
}

/* SECTION HEADER */
.section-header {
    border-bottom: 2px solid #28445f;
    padding-bottom: 0.45rem;
    margin-bottom: 1rem;
    margin-top: 1.5rem;
    color: #9fb8d8 !important;
    font-weight: 700;
    font-size: 1.35rem;
}

/* CARDS */
.action-card {
    background-color: #071226;
    padding: 1.4rem;
    border-radius: 12px;
    border-left: 4px solid #274d9b;
    margin-bottom: 1rem;
    box-shadow: 0 4px 20px rgba(0,0,0,0.6);
    transition: all 0.25s ease;
}
.action-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 26px rgba(0,0,0,0.7);
}

.gov-card {
    background: #071226;
    padding: 1.6rem;
    border-radius: 14px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.6);
    border: 1px solid #102235;
}

/* Buttons */
.stButton button {
    border-radius: 10px !important;
    padding: 0.6rem 1rem;
    font-size: 0.95rem;
    font-weight: 600;
    border: none;
    background: #29588a;
    color: white;
    transition: all 0.25s ease;
}
.stButton button:hover {
    background: #3a6fa6;
    transform: translateY(-2px);
    box-shadow: 0 8px 18px rgba(0,0,0,0.4);
}

.stButton > button[kind="secondary"] {
    background: #0f2240 !important;
    color: #a9c7e6 !important;
}
.stButton > button[kind="secondary"]:hover {
    background: #12263a !important;
}

/* Text area */
.stTextArea textarea {
    border: 2px solid #16324a !important;
    border-radius: 10px !important;
    font-size: 0.98rem;
    line-height: 1.5;
    padding: 0.85rem !important;
    background: #021124 !important;
    color: #dbeeff !important;
}
.stTextArea textarea:focus {
    border-color: #3b6aa6 !important;
    box-shadow: 0 0 0 3px rgba(59,106,166,0.12);
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #031026;
    border-right: 1px solid #071a2e;
    padding-top: 1.6rem;
}

/* Footer */
.footer {
    text-align: center;
    color: #9fc0e6;
    font-size: 0.95rem;
    padding: 1.2rem;
    font-weight: 600;
}

@media (max-width: 900px) {
    .main-header h1 { font-size: 2rem; }
    .main-header .emblem { display: none; }
}
</style>
"""

# Inject CSS based on theme
if st.session_state["theme"] == "light":
    st.markdown(LIGHT_CSS, unsafe_allow_html=True)
else:
    st.markdown(DARK_CSS, unsafe_allow_html=True)

# ==========================
# HEADER WITH UTTARAKHAND EMBLEM (SVG)
# ==========================
# Inline SVG emblem (simple, respectful shield-style emblem placeholder)
UTTARAKHAND_SVG = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64" aria-hidden="true">
  <defs>
    <linearGradient id="g1" x1="0" x2="1" y1="0" y2="1">
      <stop offset="0" stop-color="#f59e0b"/>
      <stop offset="1" stop-color="#f97316"/>
    </linearGradient>
  </defs>
  <g>
    <path d="M32 2c7 0 13 4 16 9 3 5 3 11 3 19 0 9-6 18-19 27-1 .6-2 .6-3 0C17 48 11 39 11 30c0-8 0-14 3-19 3-5 9-9 18-9z" fill="url(#g1)"/>
    <circle cx="32" cy="22" r="6" fill="#fff"/>
    <path d="M22 46c4 2 8 3 10 3s6-1 10-3" fill="none" stroke="#fff" stroke-width="1.6" stroke-linecap="round"/>
  </g>
</svg>
"""

st.markdown(
    f"""
    <div class='main-header'>
        <div style="display:flex;align-items:center;justify-content:center;gap:16px;">
            <div style="text-align:left;">
                <h1>⚖️ Vidhik AI</h1>
                <h3>Governance Gateway for the Government of Uttarakhand</h3>
            </div>
            <div style="width:72px; height:72px;" class="emblem">{UTTARAKHAND_SVG}</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# Theme toggle small control
with st.sidebar:
    st.markdown("### Theme")
    col_a, col_b = st.columns([3,1])
    with col_a:
        st.write("")  # spacer
    with col_b:
        if st.button("🌓", help="Toggle light / dark theme"):
            toggle_theme()
            st.experimental_rerun()

st.info("📋 Upload your policy draft or use the sample text below to conduct a comprehensive compliance audit.")

# ==========================
# SIMPLIFIED PDF GENERATOR (original logic preserved)
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
# MOCK ANALYSIS FUNCTION (exact original preserved)
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
# SIDEBAR (upgraded, sticky, informative)
# ==========================
with st.sidebar:
    st.markdown(
        """
        <div style='text-align: center; margin-bottom: 1rem;'>
            <h3 style='color: #1e3c72;'>🔍 Navigation</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

    with st.expander("🏛️ System Architecture", expanded=False):
        st.markdown("""
        **Phase 1: Security Gatekeeper**  
        ✅ PII Redaction & Data Privacy Check (DPDP Act)
        
        **Phase 2: Legal Analyzer**  
        ✅ Semantic Conflict Detection (FAISS DB)
        
        **Phase 3: Fairness Auditor**  
        ✅ Linguistic Bias & Inclusivity Check
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

# ==========================
# POLICY CONTENT (exact original text area content preserved)
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
# MAIN CONTENT
# ==========================
st.markdown("<div class='section-header'>Policy Document Analysis</div>", unsafe_allow_html=True)

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
# ACTION BUTTONS (aligned)
# ==========================
st.markdown("---")

# Initialize variables in session_state if not present
if "report" not in st.session_state:
    st.session_state["report"] = None
if "report_text" not in st.session_state:
    st.session_state["report_text"] = None

reset_clicked = False
clear_clicked = False
run_audit = False

button_col1, button_col2, button_col3 = st.columns([1, 2, 1])

with button_col1:
    use_sample = st.checkbox("Use sample policy", value=True)
    reset_clicked = st.button("🔄 Reset Text", use_container_width=True)

with button_col2:
    run_audit = st.button(
        "🚀 Run Comprehensive Audit", 
        type="primary", 
        use_container_width=True,
        help="Initiate full policy analysis"
    )

with button_col3:
    if st.session_state.get("report"):
        clear_clicked = st.button("🗑️ Clear Results", use_container_width=True, type="secondary")
    else:
        st.empty()

# Button actions
if reset_clicked:
    st.session_state.clear()
    st.experimental_rerun()

if clear_clicked:
    st.session_state.pop("report", None)
    st.session_state.pop("report_text", None)
    st.experimental_rerun()

# ==========================
# AUDIT PROCESSING (original logic preserved)
# ==========================
if run_audit:
    input_text = ""
    if uploaded_file:
        try:
            # Try to detect text types by uploaded_file.type
            if uploaded_file.type == "text/plain":
                input_text = str(uploaded_file.read(), "utf-8")
            elif uploaded_file.type == "application/pdf" or uploaded_file.name.lower().endswith(".pdf"):
                try:
                    import PyPDF2
                    reader = PyPDF2.PdfReader(uploaded_file)
                    extracted = []
                    for page in reader.pages:
                        try:
                            txt = page.extract_text() or ""
                        except Exception:
                            txt = ""
                        extracted.append(txt)
                    input_text = "\n".join(extracted)
                except Exception as e:
                    # fallback: attempt read as bytes -> decode
                    try:
                        input_text = str(uploaded_file.read(), "utf-8", errors="ignore")
                    except Exception:
                        input_text = ""
            elif uploaded_file.type in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                                        "application/msword"] or uploaded_file.name.lower().endswith((".docx", ".doc")):
                try:
                    import docx
                    doc = docx.Document(uploaded_file)
                    input_text = "\n".join([p.text for p in doc.paragraphs])
                except Exception as e:
                    # fallback read binary decode
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

    # progress/emulation badges
    badge_col1, badge_col2, badge_col3 = st.columns(3)
    badge_col1.markdown("<div class='action-card gov-card'><strong>Phase 1</strong><div>PII Check</div></div>", unsafe_allow_html=True)
    badge_col2.markdown("<div class='action-card gov-card'><strong>Phase 2</strong><div>Semantic Analysis</div></div>", unsafe_allow_html=True)
    badge_col3.markdown("<div class='action-card gov-card'><strong>Phase 3</strong><div>Bias Audit</div></div>", unsafe_allow_html=True)
    
    with st.spinner("🔍 Conducting comprehensive policy analysis..."):
        try:
            try:
                # preserve original attempt to import vidhik_engine
                from vidhik_engine import analyze_policy as real_analyze_policy  # noqa: F401
                # If available, call it (kept exact like original)
                final_report = real_analyze_policy(final_text)
            except Exception:
                st.warning("⚠️ Using demonstration analysis - full engine not available")
                final_report = analyze_policy(final_text)
            
            st.session_state["report"] = final_report
            st.session_state["report_text"] = final_text
            st.success("✅ Policy audit completed successfully!")
        except Exception as e:
            st.error(f"❌ Analysis error: {e}")

# ==========================
# CLEAN REPORT DISPLAY (original structure preserved)
# ==========================
if st.session_state.get("report"):
    report = st.session_state["report"]
    
    st.markdown("---")
    st.markdown("### 📊 Audit Results")
    
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

    # EXPORT SECTION
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
        else:
            st.info("PDF generation not available in this environment.")

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

    with st.expander("View Complete Dataset"):
        st.json(report)

# ==========================
# FOOTER
# ==========================
st.markdown("---")
st.markdown(
    """
    <div class='footer'>
        <strong>Vidhik AI</strong> • Government of Uttarakhand • DPDP Act Compliance • IT Act 2000 • 2025
    </div>
    """,
    unsafe_allow_html=True
)
