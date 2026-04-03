# app.py
import streamlit as st
import pandas as pd

from config import HOT_THRESHOLD, WARM_THRESHOLD, COMPANY_SIZE_MAP, INDUSTRY_MAP
from model  import predict_score, score_dataframe, load_model
from llm    import get_score_explanation, get_recommended_action

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(page_title="Lead Scoring Tool", layout="wide")

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    body { background-color: #0d0d0d; color: #e0e0e0; }
    .stApp { background-color: #0d0d0d; }
    h1 { color: #c0c0c0 !important; font-weight: 300 !important; }
    .subtitle { color: #888; font-size: 0.95rem; margin-top: -12px; margin-bottom: 24px; }
    .stTabs [data-baseweb="tab-list"] {
        background-color: #1a1a1a; border-radius: 8px; padding: 4px; gap: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: transparent; color: #888; border-radius: 6px; padding: 6px 20px;
    }
    .stTabs [aria-selected="true"] { background-color: #2a2a2a !important; color: #fff !important; }
    label { color: #aaa !important; font-size: 0.75rem !important;
            letter-spacing: 0.08em !important; text-transform: uppercase; }
    .stTextInput input, .stNumberInput input {
        background-color: #fff !important; color: #111 !important;
        border-radius: 8px !important; border: 1px solid #ddd !important;
    }
    .score-card {
        background-color: #fff; border-radius: 16px;
        padding: 28px 32px; color: #111; margin-top: 24px;
    }
    .score-label  { font-size: 0.8rem; color: #888; margin-bottom: 4px; }
    .score-value  { font-size: 4rem; font-weight: 700; line-height: 1; }
    .badge-hot    { display:inline-block; background:#ffe5d9; color:#c84b11;
                    font-size:0.72rem; font-weight:700; letter-spacing:0.06em;
                    padding:4px 10px; border-radius:20px; margin-left:10px; vertical-align:middle; }
    .badge-warm   { display:inline-block; background:#fff3cd; color:#856404;
                    font-size:0.72rem; font-weight:700; letter-spacing:0.06em;
                    padding:4px 10px; border-radius:20px; margin-left:10px; vertical-align:middle; }
    .badge-cold   { display:inline-block; background:#e2e8f0; color:#475569;
                    font-size:0.72rem; font-weight:700; letter-spacing:0.06em;
                    padding:4px 10px; border-radius:20px; margin-left:10px; vertical-align:middle; }
    .company-meta { text-align:right; font-size:0.85rem; color:#555; }
    .stat-box     { background:#f7f7f5; border-radius:10px; padding:14px 18px; margin-top:12px; }
    .stat-box-label { font-size:0.78rem; color:#888; }
    .stat-box-value { font-size:1.1rem; font-weight:600; color:#111; margin-top:2px; }
    .reason-box   { border-left:3px solid #c84b11; background:#fff8f5;
                    padding:14px 18px; border-radius:0 10px 10px 0;
                    margin-top:16px; color:#333; font-size:0.88rem; }
    .reason-box strong { color:#111; }
</style>
""", unsafe_allow_html=True)


# ── Helpers ───────────────────────────────────────────────────────────────────

def badge_for(score: int) -> tuple[str, str]:
    if score >= HOT_THRESHOLD:
        return "HOT", "hot"
    elif score >= WARM_THRESHOLD:
        return "WARM", "warm"
    return "COLD", "cold"


@st.cache_resource
def get_model():
    try:
        return load_model()
    except FileNotFoundError:
        st.error("⚠️ No trained model found. Run `python model.py` first.", icon="🚨")
        st.stop()


# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("# Lead scoring tool")
st.markdown('<p class="subtitle">Score leads manually or upload a bulk file to rank your pipeline</p>',
            unsafe_allow_html=True)

tab_manual, tab_bulk = st.tabs(["Manual input", "Bulk upload"])

# ════════════════════════════════════════════════════════════════════════════
# TAB 1 — Manual Input
# ════════════════════════════════════════════════════════════════════════════
with tab_manual:
    col1, col2 = st.columns(2)
    with col1:
        company_name = st.text_input("Company Name", value="NovaTech Solutions")
    with col2:
        industry = st.selectbox("Industry", list(INDUSTRY_MAP.keys()))

    col3, col4 = st.columns(2)
    with col3:
        company_size = st.selectbox("Company Size", list(COMPANY_SIZE_MAP.keys()), index=2)
    with col4:
        monthly_traffic = st.number_input("Monthly Website Traffic", min_value=0, value=15000, step=500)

    col5, col6 = st.columns(2)
    with col5:
        pricing_visits = st.number_input("Pricing Page Visits", min_value=0, value=5, step=1)
    with col6:
        email_opens = st.number_input("Email Opens (Last 30 Days)", min_value=0, value=8, step=1)

    col7, col8 = st.columns(2)
    with col7:
        days_since_engagement = st.number_input("Days Since Last Engagement", min_value=0, value=2, step=1)
    with col8:
        st.markdown("<br>", unsafe_allow_html=True)
        demo_requested = st.checkbox("Demo requested", value=True)

    st.markdown("<br>", unsafe_allow_html=True)
    run_score = st.button("Score this lead", type="primary")

    if run_score:
        with st.spinner("Scoring lead …"):
            mdl   = get_model()
            score = predict_score(
                company_size, industry, monthly_traffic,
                pricing_visits, email_opens, days_since_engagement,
                demo_requested, model=mdl,
            )
            badge_text, badge_style = badge_for(score)

        with st.spinner("Getting AI explanation …"):
            reason = get_score_explanation(
                company_name, industry, company_size, monthly_traffic,
                pricing_visits, email_opens, days_since_engagement,
                demo_requested, score, badge_text,
            )
            action = get_recommended_action(
                score, badge_text, days_since_engagement,
                demo_requested, pricing_visits,
            )

        st.session_state["last_score"] = dict(
            score=score, badge_text=badge_text, badge_style=badge_style,
            action=action, reason=reason, company_name=company_name,
            industry=industry, company_size=company_size,
            pricing_visits=pricing_visits, days_since_engagement=days_since_engagement,
        )

    if "last_score" in st.session_state:
        d           = st.session_state["last_score"]
        score       = d["score"]
        badge_style = d["badge_style"]
        bar_color   = "#c84b11" if badge_style == "hot" else ("#e6a817" if badge_style == "warm" else "#94a3b8")

        st.markdown(f"""
        <div class="score-card">
            <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                <div>
                    <div class="score-label">Conversion score</div>
                    <div>
                        <span class="score-value">{score}</span>
                        <span class="badge-{badge_style}">{d['badge_text']}</span>
                    </div>
                </div>
                <div class="company-meta">
                    <strong>{d['company_name']}</strong><br>
                    {d['industry']} · {d['company_size']} employees
                </div>
            </div>
            <div style="margin:18px 0 8px; background:#eee; border-radius:99px; height:10px; overflow:hidden;">
                <div style="width:{score}%; height:100%; background:{bar_color}; border-radius:99px;"></div>
            </div>
            <div style="display:flex; gap:12px; margin-top:4px;">
                <div class="stat-box" style="flex:1;">
                    <div class="stat-box-label">Pricing page visits</div>
                    <div class="stat-box-value">{d['pricing_visits']}</div>
                </div>
                <div class="stat-box" style="flex:1;">
                    <div class="stat-box-label">Last engagement</div>
                    <div class="stat-box-value">{d['days_since_engagement']} days ago</div>
                </div>
                <div class="stat-box" style="flex:1;">
                    <div class="stat-box-label">Recommended action</div>
                    <div class="stat-box-value">{d['action']}</div>
                </div>
            </div>
            <div class="reason-box">
                <strong>Why this score?</strong><br>{d['reason']}
            </div>
        </div>
        """, unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
# TAB 2 — Bulk Upload
# ════════════════════════════════════════════════════════════════════════════
with tab_bulk:
    st.markdown("#### Upload a CSV file")
    st.markdown(
        "Expected columns: `company_name`, `industry`, `company_size`, "
        "`monthly_traffic`, `pricing_visits`, `email_opens`, "
        "`days_since_engagement`, `demo_requested`"
    )

    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.markdown(f"**{len(df)} leads loaded.** Preview:")
        st.dataframe(df.head(10), use_container_width=True)

        if st.button("Score all leads", type="primary"):
            with st.spinner(f"Scoring {len(df)} leads …"):
                mdl    = get_model()
                df_out = score_dataframe(df, model=mdl)
                df_out["badge"] = df_out["score"].apply(lambda s: badge_for(s)[0])
                df_out = df_out.sort_values("score", ascending=False).reset_index(drop=True)

            st.success("Scoring complete!")
            st.dataframe(df_out, use_container_width=True)

            st.download_button(
                "Download scored leads as CSV",
                data=df_out.to_csv(index=False).encode("utf-8"),
                file_name="scored_leads.csv",
                mime="text/csv",
            )