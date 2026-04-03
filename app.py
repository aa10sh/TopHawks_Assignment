import streamlit as st
import pandas as pd
import numpy as np
import json
import os
import pickle
# import anthropic
from io import BytesIO

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Lead Scoring Tool",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp { background: #F8F7F4; }

/* Header */
.app-header {
    padding: 2rem 0 1.5rem;
    border-bottom: 1px solid #E5E3DC;
    margin-bottom: 2rem;
}
.app-title {
    font-size: 26px;
    font-weight: 600;
    color: #1A1A18;
    letter-spacing: -0.5px;
    margin: 0;
}
.app-subtitle {
    font-size: 14px;
    color: #888780;
    margin-top: 4px;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 0;
    background: transparent;
    border-bottom: 1px solid #E5E3DC;
}
.stTabs [data-baseweb="tab"] {
    background: transparent;
    border: none;
    border-bottom: 2px solid transparent;
    color: #888780;
    font-family: 'DM Sans', sans-serif;
    font-size: 14px;
    font-weight: 500;
    padding: 10px 20px;
    border-radius: 0;
}
.stTabs [aria-selected="true"] {
    background: transparent !important;
    color: #1A1A18 !important;
    border-bottom: 2px solid #1A1A18 !important;
}
.stTabs [data-baseweb="tab-panel"] { padding-top: 1.5rem; }

/* Cards */
.score-card {
    background: white;
    border: 1px solid #E5E3DC;
    border-radius: 12px;
    padding: 1.5rem;
    margin-top: 1.5rem;
}
.meta-card {
    background: #F8F7F4;
    border: 1px solid #E5E3DC;
    border-radius: 8px;
    padding: 12px 16px;
    text-align: center;
}
.meta-label { font-size: 11px; color: #888780; font-weight: 500; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 4px; }
.meta-value { font-size: 18px; font-weight: 600; color: #1A1A18; }

/* Tier badges */
.badge-hot { background: #FAECE7; color: #993C1D; padding: 4px 12px; border-radius: 6px; font-size: 12px; font-weight: 600; }
.badge-warm { background: #FAEEDA; color: #854F0B; padding: 4px 12px; border-radius: 6px; font-size: 12px; font-weight: 600; }
.badge-cold { background: #E6F1FB; color: #185FA5; padding: 4px 12px; border-radius: 6px; font-size: 12px; font-weight: 600; }

/* Score number */
.score-big { font-size: 56px; font-weight: 600; color: #1A1A18; line-height: 1; letter-spacing: -2px; }

/* Reasoning box */
.reasoning-box {
    background: #F8F7F4;
    border-left: 3px solid #D85A30;
    border-radius: 0 8px 8px 0;
    padding: 14px 16px;
    margin-top: 1rem;
    font-size: 14px;
    color: #5F5E5A;
    line-height: 1.6;
}
.reasoning-label { font-size: 11px; font-weight: 600; color: #1A1A18; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 6px; }

/* JSON box */
.json-box {
    background: #1A1A18;
    border-radius: 10px;
    padding: 1.25rem;
    font-family: 'DM Mono', monospace;
    font-size: 12px;
    color: #C8C6BF;
    line-height: 1.8;
    margin-top: 1rem;
    overflow-x: auto;
}

/* Upload zone */
.upload-hint {
    font-size: 12px;
    color: #888780;
    margin-top: 6px;
    text-align: center;
}

/* Progress bar */
.progress-bg {
    background: #E5E3DC;
    border-radius: 4px;
    height: 8px;
    margin: 12px 0;
    overflow: hidden;
}

/* Buttons */
.stButton > button {
    font-family: 'DM Sans', sans-serif;
    font-weight: 500;
    border-radius: 8px;
    border: 1px solid #D3D1C7;
    background: white;
    color: #1A1A18;
    padding: 8px 20px;
    transition: all 0.15s ease;
}
.stButton > button:hover {
    background: #F8F7F4;
    border-color: #888780;
}
.stButton > button[kind="primary"] {
    background: #1A1A18;
    color: white;
    border-color: #1A1A18;
}
.stButton > button[kind="primary"]:hover {
    background: #2C2C2A;
}

/* Form inputs */
.stTextInput input, .stNumberInput input, .stSelectbox select {
    font-family: 'DM Sans', sans-serif;
    border-radius: 8px;
    border: 1px solid #D3D1C7;
    background: white;
}

/* Table styling */
.stDataFrame {
    border: 1px solid #E5E3DC;
    border-radius: 10px;
    overflow: hidden;
}

/* Section label */
.section-label {
    font-size: 13px;
    font-weight: 600;
    color: #888780;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 10px;
}

/* Divider */
hr { border: none; border-top: 1px solid #E5E3DC; margin: 1.5rem 0; }
</style>
""", unsafe_allow_html=True)

# ── Load / Train Model ─────────────────────────────────────────────────────────
@st.cache_resource(show_spinner="Training model on first run…")
def get_model():
    model_path = "model/lead_scorer.pkl"
    if os.path.exists(model_path):
        with open(model_path, "rb") as f:
            return pickle.load(f)
    from model import build_and_train
    return build_and_train()

# ── Anthropic client ───────────────────────────────────────────────────────────
@st.cache_resource
def get_anthropic_client():
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if api_key:
        return anthropic.Anthropic(api_key=api_key)
    return None

# ── Helper: score a single lead ────────────────────────────────────────────────
def score_single(model, data: dict) -> dict:
    df = pd.DataFrame([data])
    from model import score_leads
    result = score_leads(df, model)
    return result.iloc[0].to_dict()

# ── Helper: tier badge HTML ────────────────────────────────────────────────────
def tier_badge(tier: str) -> str:
    cls = {"HOT": "badge-hot", "WARM": "badge-warm", "COLD": "badge-cold"}.get(tier, "badge-cold")
    return f'<span class="{cls}">{tier}</span>'

# ── Helper: score bar color ────────────────────────────────────────────────────
def score_color(score: int) -> str:
    if score >= 70: return "#D85A30"
    if score >= 40: return "#BA7517"
    return "#378ADD"

# ── Helper: generate LLM reason for one lead ──────────────────────────────────
def generate_reason(client, lead: dict) -> str:
    if not client:
        return "API key not set. Add ANTHROPIC_API_KEY to your environment."
    prompt = f"""You are a B2B sales intelligence assistant. Given the following lead data, 
explain in 2-3 concise sentences why the lead received a conversion score of {lead.get('conversion_score', 'N/A')}/100 
and is classified as {lead.get('tier', 'N/A')}.

Lead data:
- Industry: {lead.get('industry')}
- Company size: {lead.get('company_size')}
- Website traffic: {lead.get('website_traffic')}
- Pricing page visits: {lead.get('pricing_page_visits')}
- Demo requested: {'Yes' if lead.get('demo_requested') else 'No'}
- Email opens: {lead.get('email_opens')}
- Days since last engagement: {lead.get('days_since_last_engagement')}

Be direct and specific. Focus on the strongest signals."""
    msg = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=200,
        messages=[{"role": "user", "content": prompt}]
    )
    return msg.content[0].text

# ── Helper: generate reasons for bulk leads ────────────────────────────────────
def generate_bulk_reasons(client, df: pd.DataFrame) -> list:
    results = []
    for _, row in df.iterrows():
        lead = row.to_dict()
        reason = generate_reason(client, lead)
        results.append({
            "company_name": lead.get("company_name", "Unknown"),
            "score": int(lead.get("conversion_score", 0)),
            "tier": str(lead.get("tier", "COLD")),
            "reason": reason,
            "recommended_action": lead.get("recommended_action", "")
        })
    return results

# ── App Header ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="app-header">
  <p class="app-title">🎯 Lead Scoring Tool</p>
  <p class="app-subtitle">Score leads manually or upload a bulk file to rank your pipeline</p>
</div>
""", unsafe_allow_html=True)

model = get_model()
client = get_anthropic_client()

# ── Tabs ───────────────────────────────────────────────────────────────────────
tab1, tab2 = st.tabs(["  Manual input  ", "  Bulk upload  "])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — MANUAL INPUT
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    with st.form("manual_form"):
        col1, col2 = st.columns(2)
        with col1:
            company_name = st.text_input("Company name", placeholder="e.g. NovaTech Solutions")
            industry = st.selectbox("Industry", ["SaaS", "Retail", "FMCG", "Finance",
                                                  "Healthcare", "Manufacturing", "EdTech", "Logistics"])
            company_size = st.selectbox("Company size", ["1-10", "11-50", "51-200", "201-500", "500+"])
            website_traffic = st.number_input("Monthly website traffic", min_value=0, value=15000, step=500)
        with col2:
            pricing_page_visits = st.number_input("Pricing page visits", min_value=0, value=3, step=1)
            email_opens = st.number_input("Email opens (last 30 days)", min_value=0, value=5, step=1)
            days_since_engagement = st.number_input("Days since last engagement", min_value=0, value=3, step=1)
            demo_requested = st.checkbox("Demo requested", value=False)

        submitted = st.form_submit_button("Score this lead", type="primary", use_container_width=True)

    if submitted:
        lead_data = {
            "industry": industry,
            "company_size": company_size,
            "website_traffic": website_traffic,
            "pricing_page_visits": pricing_page_visits,
            "demo_requested": int(demo_requested),
            "email_opens": email_opens,
            "days_since_last_engagement": days_since_engagement
        }
        result = score_single(model, lead_data)
        score = int(result["conversion_score"])
        tier = str(result["tier"])
        prob = float(result["conversion_probability"])
        action = result["recommended_action"]
        color = score_color(score)

        # Score card
        st.markdown('<div class="score-card">', unsafe_allow_html=True)

        top_col1, top_col2 = st.columns([1, 2])
        with top_col1:
            st.markdown(f'<div class="score-big" style="color:{color}">{score}</div>', unsafe_allow_html=True)
            st.markdown(f'<div style="margin-top:8px">{tier_badge(tier)}</div>', unsafe_allow_html=True)
            st.markdown('<div style="font-size:12px;color:#888780;margin-top:6px">Conversion score / 100</div>', unsafe_allow_html=True)
        with top_col2:
            st.markdown(f'<div style="font-size:15px;font-weight:600;color:#1A1A18">{company_name or "Lead"}</div>', unsafe_allow_html=True)
            st.markdown(f'<div style="font-size:13px;color:#888780;margin-bottom:12px">{industry} · {company_size} employees</div>', unsafe_allow_html=True)
            bar_width = min(score, 100)
            st.markdown(f"""
            <div class="progress-bg">
              <div style="width:{bar_width}%;height:8px;border-radius:4px;background:{color};transition:width 0.5s ease"></div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown(f'<div style="font-size:13px;color:#888780">Probability: <strong style="color:#1A1A18">{prob:.0%}</strong></div>', unsafe_allow_html=True)

        st.markdown("---")

        m1, m2, m3 = st.columns(3)
        with m1:
            st.markdown(f'<div class="meta-card"><div class="meta-label">Pricing page visits</div><div class="meta-value">{pricing_page_visits}</div></div>', unsafe_allow_html=True)
        with m2:
            st.markdown(f'<div class="meta-card"><div class="meta-label">Last engagement</div><div class="meta-value">{days_since_engagement}d ago</div></div>', unsafe_allow_html=True)
        with m3:
            st.markdown(f'<div class="meta-card"><div class="meta-label">Recommended action</div><div class="meta-value" style="font-size:13px">{action}</div></div>', unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        # Reasoning
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Generate AI reasoning", key="manual_reason"):
            with st.spinner("Generating reasoning…"):
                reason = generate_reason(client, {**lead_data, "conversion_score": score, "tier": tier})
            st.markdown(f"""
            <div class="reasoning-box">
              <div class="reasoning-label">Why this score?</div>
              {reason}
            </div>
            """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — BULK UPLOAD
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    # Download template
    with open("sample_data/sample_leads.csv", "rb") as f:
        template_bytes = f.read()

    dl_col, _ = st.columns([1, 3])
    with dl_col:
        st.download_button(
            label="Download CSV template",
            data=template_bytes,
            file_name="lead_scoring_template.csv",
            mime="text/csv"
        )

    uploaded_file = st.file_uploader(
        "Upload your leads file",
        type=["csv", "xlsx"],
        help="Upload a CSV or Excel file with the same columns as the template"
    )
    st.markdown('<div class="upload-hint">Supports .csv and .xlsx · Max 200 leads recommended</div>', unsafe_allow_html=True)

    if uploaded_file:
        try:
            if uploaded_file.name.endswith(".xlsx"):
                raw_df = pd.read_excel(uploaded_file)
            else:
                raw_df = pd.read_csv(uploaded_file)

            required_cols = ["industry", "company_size", "website_traffic",
                             "pricing_page_visits", "demo_requested",
                             "email_opens", "days_since_last_engagement"]
            missing = [c for c in required_cols if c not in raw_df.columns]
            if missing:
                st.error(f"Missing columns: {', '.join(missing)}. Please use the template.")
            else:
                with st.spinner("Scoring all leads…"):
                    from model import score_leads
                    scored_df = score_leads(raw_df.copy(), model)

                st.markdown(f'<div class="section-label" style="margin-top:1.5rem">Scored results — {len(scored_df)} leads</div>', unsafe_allow_html=True)

                # Display table
                display_cols = ["company_name", "industry", "company_size",
                                "conversion_score", "tier", "recommended_action"] \
                    if "company_name" in scored_df.columns else \
                    ["industry", "company_size", "conversion_score", "tier", "recommended_action"]

                st.dataframe(
                    scored_df[display_cols].rename(columns={
                        "company_name": "Company",
                        "industry": "Industry",
                        "company_size": "Size",
                        "conversion_score": "Score",
                        "tier": "Tier",
                        "recommended_action": "Action"
                    }),
                    use_container_width=True,
                    hide_index=True
                )

                # Download scored CSV
                csv_bytes = scored_df.to_csv(index=False).encode()
                st.download_button(
                    label="Download scored results (CSV)",
                    data=csv_bytes,
                    file_name="scored_leads.csv",
                    mime="text/csv"
                )

                st.markdown("---")

                # AI Reasons
                if st.button("Generate AI reasons for all leads", type="primary"):
                    with st.spinner("Generating reasons via Claude API… this may take a moment"):
                        reasons = generate_bulk_reasons(client, scored_df)

                    st.markdown('<div class="section-label">AI-generated reasons</div>', unsafe_allow_html=True)

                    # JSON preview
                    json_str = json.dumps({"leads": reasons}, indent=2)
                    st.markdown(f'<div class="json-box"><pre style="margin:0;color:#C8C6BF;font-family:\'DM Mono\',monospace;font-size:12px">{json_str}</pre></div>', unsafe_allow_html=True)

                    # Download buttons
                    dl1, dl2 = st.columns(2)
                    with dl1:
                        st.download_button(
                            label="Download reasons (JSON)",
                            data=json_str,
                            file_name="lead_reasons.json",
                            mime="application/json"
                        )
                    with dl2:
                        reasons_df = pd.DataFrame(reasons)
                        st.download_button(
                            label="Download reasons (CSV)",
                            data=reasons_df.to_csv(index=False).encode(),
                            file_name="lead_reasons.csv",
                            mime="text/csv"
                        )

        except Exception as e:
            st.error(f"Error processing file: {str(e)}")