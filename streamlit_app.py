"""
Vidhik AI – Government Blue Dashboard
Complete Streamlit UI + PDF Export
"""

import streamlit as st
import json
import io
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# Try import of actual engine
try:
    from vidhik_engine import analyze_policy
except Exception:
    def analyze_policy(text):
        now = datetime.utcnow().isoformat() + "Z"
        return {
            "Overall Status": "Medium Risk",
            "Executive Summary": "Demo version: medium risk found (PII + accessibility).",
            "Actionable Recommendations": (
                "### ⚖️ Legal Conflicts\n- Remove compulsory Aadhar.\n- Add retention limits.\n\n"
                "### 🌍 Inclusive Language\n- Avoid hardware-exclusive requirements.\n\n"
                "### 🔒 PII Risk\n- Redact names & address before publication."
            ),
            "Raw Reports": {
                "Conflict Report": {
                    "Conflicting Laws": [
                        {"Rank": 1, "Similarity Score": 0.92, "Risk Level": "High",
                         "Legal Provision": "Right to privacy & Data Minimization (DPDP)"}
                    ]
                },
                "Bias Report": {
                    "flagged_phrases": [
                        {"phrase": "bank account numbers", "lexicon": "exclusionary"},
                        {"phrase": "high-speed fiber only", "lexicon": "accessibility"},
                    ]
                },
                "PII Report": {
                    "status": "PII Found",
                    "detected_items": [
                        {"type": "Name", "value": "Mr. Rajesh Kumar"},
                        {"type": "Address", "value": "Mandi Road, Dehradun 248001"},
                    ]
                }
            },
            "generated_at": now
        }


# ---------------------------
# PDF GENERATOR
# ---------------------------
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm

def create_pdf_from_report(report: dict):
    buffer = io.BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        topMargin=2*cm,
        bottomMargin=2*cm,
        leftMargin=2*cm,
        rightMargin=2*cm
    )

    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("<b>Vidhik AI – Policy Audit Report</b>", styles["Title"]))
    story.append(Spacer(1, 16))

    # Overall Status
    status = report.get("Overall Status", "Unknown")
    story.append(Paragraph(f"<b>Overall Status:</b> {status}", styles["Heading2"]))
    story.append(Spacer(1, 10))

    # Executive Summary
    story.append(Paragraph("<b>Executive Summary</b>", styles["Heading2"]))
    story.append(Paragraph(report.get("Executive Summary", "No summary"), styles["Normal"]))
    story.append(Spacer(1, 12))

    # Recommendations
    story.append(Paragraph("<b>Actionable Recommendations</b>", styles["Heading2"]))
    rec_html = report.get("Actionable Recommendations", "None").replace("\n", "<br/>")
    story.append(Paragraph(rec_html, styles["Normal"]))
    story.append(Spacer(1, 12))

    # Raw Reports
    story.append(Paragraph("<b>Raw Reports</b>", styles["Heading2"]))

    for k, v in report.get("Raw Reports", {}).items():
        story.append(Paragraph(f"<b>{k}</b>", styles["Heading3"]))
        v_json = json.dumps(v, indent=2).replace("\n", "<br/>")
        story.append(Paragraph(v_json, styles["Code"]))
        story.append(Spacer(1, 12))

    doc.build(story)
    pdf_data = buffer.getvalue()
    buffer.close()
    return pdf_data


# ---------------------------
# PAGE CONFIG
# ---------------------------
st.set_page_config(
    page_title="Vidhik AI — Governance Gateway",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ---------------------------
# CSS
# ---------------------------
st.markdown(
    """
    <style>
    .top-nav {
        background: linear-gradient(90deg,#0D47A1,#1565C0,#1976D2);
        padding: 14px 20px;
        color: white;
        border-radius: 8px;
        font-size: 20px;
        font-weight: 700;
        box-shadow: 0 6px 16px rgba(13,71,161,0.25);
    }
    .subtitle {
        font-size: 13px;
        opacity: 0.9;
        margin-top: -6px;
    }
    .card {
        background: white;
        padding: 18px;
        border-radius: 10px;
        box-shadow: 0 4px 14px rgba(0,0,0,0.08);
        margin-bottom: 20px;
    }
    .muted {
        color: #546E7A;
        font-size: 13px;
    }
    .metric-value {
        font-size: 22px;
        font-weight: 700;
        color: #0D47A1;
    }
    .metric-title {
        font-size: 13px;
        color: #607D8B;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------------------
# TOP NAV
# ---------------------------
st.markdown("<div class='top-nav'>⚖️ Vidhik AI — Governance Gateway</div>", unsafe_allow_html=True)


# ---------------------------
# SIDEBAR
# ---------------------------
with st.sidebar:
    st.header("🧭 Navigation")
    nav = st.radio("", ["Dashboard", "New Audit", "Settings", "About"])
    st.markdown("---")
    st.caption("Compliance Framework: DPDP • IT Act • Constitutional Principles")


# ---------------------------
# ROUTES
# ---------------------------

# ------------------ DASHBOARD ------------------
if nav == "Dashboard":
    st.subheader("Overview")
    st.markdown("<div class='muted'>Your recent policy audits and analytics summary.</div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div class='metric-title'>Total Audits</div>", unsafe_allow_html=True)
        st.markdown("<div class='metric-value'>42</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div class='metric-title'>High Risk</div>", unsafe_allow_html=True)
        st.markdown("<div class='metric-value'>7</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with col3:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div class='metric-title'>Medium Risk</div>", unsafe_allow_html=True)
        st.markdown("<div class='metric-value'>18</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Chart
    months = pd.date_range(end=pd.Timestamp.today(), periods=6, freq="M").strftime("%b")
    vals = np.random.randint(3, 12, size=6)
    fig, ax = plt.subplots(figsize=(6, 3))
    ax.plot(months, vals, marker="o")
    ax.grid(alpha=0.3)
    st.pyplot(fig)


# ------------------ NEW AUDIT ------------------
elif nav == "New Audit":
    st.subheader("New Policy Audit")
    st.markdown("<div class='muted'>Paste or upload a draft policy to begin the analysis.</div>", unsafe_allow_html=True)

    text = st.text_area("Policy Text", height=300)

    uploaded = st.file_uploader("Upload File", type=["txt", "pdf", "docx", "doc"])
    if uploaded:
        try:
            if uploaded.type == "text/plain":
                text = str(uploaded.read(), "utf-8")
            elif uploaded.type == "application/pdf":
                import PyPDF2
                reader = PyPDF2.PdfReader(uploaded)
                text = "\n".join([p.extract_text() for p in reader.pages])
            else:
                import docx
                doc = docx.Document(uploaded)
                text = "\n".join([p.text for p in doc.paragraphs])
        except:
            st.error("Failed to read uploaded file.")

    if st.button("🚀 Run Vidhik AI Audit"):
        if not text.strip():
            st.error("Enter or upload policy text first.")
        else:
            with st.spinner("Analyzing..."):
                report = analyze_policy(text)
                st.session_state["report"] = report
            st.success("Audit Completed!")

    # If report exists, show buttons
    if "report" in st.session_state:
        rep = st.session_state["report"]

        st.subheader("Audit Result")
        st.write(f"**Status:** {rep.get('Overall Status')}")

        pdf_file = create_pdf_from_report(rep)

        st.download_button(
            "📄 Download PDF Report",
            data=pdf_file,
            file_name="VidhikAI_Audit_Report.pdf",
            mime="application/pdf"
        )

        st.download_button(
            "📥 Download JSON Report",
            data=json.dumps(rep, indent=2),
            file_name="VidhikAI_Audit_Report.json",
            mime="application/json"
        )

        with st.expander("View Full Report JSON"):
            st.json(rep)


# ------------------ SETTINGS ------------------
elif nav == "Settings":
    st.subheader("Settings")
    st.write("No advanced settings yet.")


# ------------------ ABOUT ------------------
elif nav == "About":
    st.subheader("About Vidhik AI")
    st.write("Government-grade policy compliance auditor for Uttarakhand.")
    st.write("Built with DPDP Act, IT Act and constitutional principles.")


st.markdown("---")
st.caption("Vidhik AI • Government of Uttarakhand • 2025")
