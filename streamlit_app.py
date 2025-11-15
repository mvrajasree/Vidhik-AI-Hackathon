import streamlit as st

st.set_page_config(
    page_title="Vidhik AI: Governance Gateway",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Dynamic Landing Section (Government Homepage Style) ---
HERO_SVG = '''
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="100" height="100"><g><path d="M32 2c7 0 13 4 16 9 3 5 3 11 3 19 0 9-6 18-19 27-1 .6-2 .6-3 0C17 48 11 39 11 30c0-8 0-14 3-19 3-5 9-9 18-9z" fill="#2a5298"/><circle cx="32" cy="22" r="6" fill="#fff"/><path d="M22 46c4 2 8 3 10 3s6-1 10-3" fill="none" stroke="#fff" stroke-width="1.4" stroke-linecap="round"/></g></svg>
'''

LANDING_STYLE = """
<style>
.landing-bg {
  background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
  border-radius: 26px;
  box-shadow: 0 8px 30px rgba(15,23,42,0.11);
  color: #fff;
  padding: 2.2rem 2.4rem 2rem 2.4rem;
  margin-bottom: 2.2rem;
  display: flex;
  align-items: center;
  gap: 2.5rem;
}
.landing-text {
  flex: 2;
}
.landing-headline {
  font-size: 2.7rem;
  font-weight: 800;
  margin-bottom: 0.6rem;
  letter-spacing: 0.2px;
}
.landing-sub {
  font-size: 1.15rem;
  font-weight: 400;
  margin-bottom: 1.3rem;
  opacity: 0.96;
}
.cta-row {
  display: flex;
  gap: 1rem;
  margin-top: 2rem;
}
.cta-btn {
  background: #fff;
  color: #1e3c72;
  border: none;
  font-weight: 700;
  padding: 0.65rem 1.7rem;
  font-size: 1.09rem;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(42,82,152,0.10);
  cursor: pointer;
  transition: background 0.23s, color 0.23s;
}
.cta-btn:hover {
  background: #e6eef8;
}
@media (max-width:900px) {
  .landing-bg { flex-direction: column; padding: 1.4rem 1rem; gap: 1.3rem; }
}
</style>
"""
st.markdown(LANDING_STYLE, unsafe_allow_html=True)

st.markdown(f"""
<div class='landing-bg'>
  <div style='flex:1;display:flex;align-items:center;justify-content:center;min-width:120px;'>
      {HERO_SVG}
  </div>
  <div class='landing-text'>
    <div class='landing-headline'>⚖️ Vidhik AI</div>
    <div class='landing-sub'>A Unified Governance Gateway for the Government of Uttarakhand.<br>
      Empowering secure, fair, and fully compliant e-Governance through advanced policy audits, legal analysis, and privacy assurance for digital public services.
    </div>
    <div>
      <ul style="margin-top:0.2rem; font-size:1.08rem; line-height:1.74;">
        <li>PII Redaction & DPDP Act Compliance (Privacy by Design)</li>
        <li>Automated Legal Conflict Detection & Fairness Analysis</li>
        <li>Bias and Inclusivity Reporting on all policy drafts</li>
        <li>Fully exportable, session-preserved, and audit-trailed</li>
      </ul>
    </div>
    <div class='cta-row'>
      <a href='#policy-draft-to-audit'><button class='cta-btn'>Start Audit</button></a>
      <a href='#' onclick='window.scrollTo(0,document.body.scrollHeight)'><button class='cta-btn'>Export & Reports</button></a>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# --- Quick Stats Overview ---
with st.expander("ℹ️ What does Vidhik AI do?", expanded=False):
    st.markdown("""
    **Vidhik AI** is Uttarakhand's next-generation governance intelligence assistant:
    - Instantly audits digital policies and citizen service drafts for compliance, bias, and privacy risks.
    - Pinpoints issues under India’s DPDP Act and IT Act with detailed, plain-language explanations.
    - Tailored for government officers, policy architects, and public service designers.
    """)

# (Rest of your Streamlit application below)
