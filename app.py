import streamlit as st

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(page_title="Lead Scoring Tool", layout="wide")

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Global */
    body { background-color: #0d0d0d; color: #e0e0e0; }
    .stApp { background-color: #0d0d0d; }

    /* Title */
    h1 { color: #c0c0c0 !important; font-weight: 300 !important; }
    .subtitle { color: #888; font-size: 0.95rem; margin-top: -12px; margin-bottom: 24px; }

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #1a1a1a;
        border-radius: 8px;
        padding: 4px;
        gap: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        color: #888;
        border-radius: 6px;
        padding: 6px 20px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #2a2a2a !important;
        color: #fff !important;
    }

    /* Labels */
    label { color: #aaa !important; font-size: 0.75rem !important;
            letter-spacing: 0.08em !important; text-transform: uppercase; }

    /* Inputs */
    .stTextInput input, .stNumberInput input, .stSelectbox select {
        background-color: #fff !important;
        color: #111 !important;
        border-radius: 8px !important;
        border: 1px solid #ddd !important;
    }

    /* Score card */
    .score-card {
        background-color: #fff;
        border-radius: 16px;
        padding: 28px 32px;
        color: #111;
        margin-top: 24px;
    }
    .score-label { font-size: 0.8rem; color: #888; margin-bottom: 4px; }
    .score-value { font-size: 4rem; font-weight: 700; line-height: 1; }
    .badge-hot {
        display: inline-block;
        background: #ffe5d9;
        color: #c84b11;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.06em;
        padding: 4px 10px;
        border-radius: 20px;
        margin-left: 10px;
        vertical-align: middle;
    }
    .badge-warm {
        display: inline-block;
        background: #fff3cd;
        color: #856404;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.06em;
        padding: 4px 10px;
        border-radius: 20px;
        margin-left: 10px;
        vertical-align: middle;
    }
    .badge-cold {
        display: inline-block;
        background: #e2e8f0;
        color: #475569;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.06em;
        padding: 4px 10px;
        border-radius: 20px;
        margin-left: 10px;
        vertical-align: middle;
    }
    .company-meta { text-align: right; font-size: 0.85rem; color: #555; }
    .stat-box {
        background: #f7f7f5;
        border-radius: 10px;
        padding: 14px 18px;
        margin-top: 12px;
    }
    .stat-box-label { font-size: 0.78rem; color: #888; }
    .stat-box-value { font-size: 1.1rem; font-weight: 600; color: #111; margin-top: 2px; }
    .reason-box {
        border-left: 3px solid #c84b11;
        background: #fff8f5;
        padding: 14px 18px;
        border-radius: 0 10px 10px 0;
        margin-top: 16px;
        color: #333;
        font-size: 0.88rem;
    }
    .reason-box strong { color: #111; }
</style>
""", unsafe_allow_html=True)

# ── Import your functions here ─────────────────────────────────────────────
# from functions import score_lead, get_badge, get_recommended_action, get_score_reason
# Placeholder stubs — replace with your real imports:
def score_lead(company_size, industry, traffic, pricing_visits,
               email_opens, days_since_engagement, demo_requested):
    """Stub — replace with your scoring logic."""
    score = 50
    if demo_requested:
        score += 20
    if pricing_visits >= 5:
        score += 10
    if days_since_engagement <= 2:
        score += 10
    if industry == "SaaS":
        score += 5
    if company_size in ("51–200", "201–500", "501–1000", "1000+"):
        score += 5
    return min(score, 100)

def get_badge(score):
    """Stub — replace with your badge logic."""
    if score >= 70:
        return "HOT", "hot"
    elif score >= 40:
        return "WARM", "warm"
    else:
        return "COLD", "cold"

def get_recommended_action(score, days_since_engagement):
    """Stub — replace with your action logic."""
    if score >= 70 and days_since_engagement <= 3:
        return "Call within 24h"
    elif score >= 40:
        return "Send follow-up email"
    else:
        return "Add to nurture sequence"

def get_score_reason(score, pricing_visits, demo_requested,
                     days_since_engagement, industry, company_size):
    """Stub — replace with your explanation logic."""
    return (
        "High pricing page visits combined with a recent demo request and "
        "engagement within 48 hours are strong purchase-intent signals. "
        f"Company size and {industry} industry align well with typical conversion profiles."
    )
# ──────────────────────────────────────────────────────────────────────────────

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("# Lead scoring tool")
st.markdown('<p class="subtitle">Score leads manually or upload a bulk file to rank your pipeline</p>',
            unsafe_allow_html=True)

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab_manual, tab_bulk = st.tabs(["Manual input", "Bulk upload"])

# ════════════════════════════════════════════════════════════════════════════
# TAB 1 — Manual Input
# ════════════════════════════════════════════════════════════════════════════
with tab_manual:

    col1, col2 = st.columns(2)

    with col1:
        company_name = st.text_input("Company Name", value="NovaTech Solutions")

    with col2:
        industry = st.selectbox(
            "Industry",
            ["SaaS", "E-commerce", "Healthcare", "Finance", "Manufacturing",
             "Education", "Retail", "Real Estate", "Other"],
            index=0,
        )

    col3, col4 = st.columns(2)

    with col3:
        company_size = st.selectbox(
            "Company Size",
            ["1–10", "11–50", "51–200", "201–500", "501–1000", "1000+"],
            index=2,
        )

    with col4:
        monthly_traffic = st.number_input(
            "Monthly Website Traffic", min_value=0, value=15000, step=500
        )

    col5, col6 = st.columns(2)

    with col5:
        pricing_visits = st.number_input(
            "Pricing Page Visits", min_value=0, value=5, step=1
        )

    with col6:
        email_opens = st.number_input(
            "Email Opens (Last 30 Days)", min_value=0, value=8, step=1
        )

    col7, col8 = st.columns(2)

    with col7:
        days_since_engagement = st.number_input(
            "Days Since Last Engagement", min_value=0, value=2, step=1
        )

    with col8:
        st.markdown("<br>", unsafe_allow_html=True)   # vertical align
        demo_requested = st.checkbox("Demo requested", value=True)

    st.markdown("<br>", unsafe_allow_html=True)
    run_score = st.button("Score this lead", type="primary")

    # ── Results card ──────────────────────────────────────────────────────────
    if run_score or "last_score" in st.session_state:

        if run_score:
            score = score_lead(
                company_size, industry, monthly_traffic,
                pricing_visits, email_opens, days_since_engagement,
                demo_requested,
            )
            badge_text, badge_style = get_badge(score)
            action = get_recommended_action(score, days_since_engagement)
            reason = get_score_reason(
                score, pricing_visits, demo_requested,
                days_since_engagement, industry, company_size,
            )
            # Cache so card persists without re-click
            st.session_state["last_score"] = dict(
                score=score, badge_text=badge_text, badge_style=badge_style,
                action=action, reason=reason,
                company_name=company_name, industry=industry,
                company_size=company_size, pricing_visits=pricing_visits,
                days_since_engagement=days_since_engagement,
            )

        d = st.session_state["last_score"]
        score        = d["score"]
        badge_text   = d["badge_text"]
        badge_style  = d["badge_style"]
        action       = d["action"]
        reason       = d["reason"]

        badge_html = f'<span class="badge-{badge_style}">{badge_text}</span>'

        # Progress bar colour via inline style
        bar_pct = score
        bar_color = "#c84b11" if badge_style == "hot" else ("#e6a817" if badge_style == "warm" else "#94a3b8")

        st.markdown(f"""
        <div class="score-card">
            <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                <div>
                    <div class="score-label">Conversion score</div>
                    <div>
                        <span class="score-value">{score}</span>
                        {badge_html}
                    </div>
                </div>
                <div class="company-meta">
                    <strong>{d['company_name']}</strong><br>
                    {d['industry']} · {d['company_size']} employees
                </div>
            </div>

            <!-- Progress bar -->
            <div style="margin:18px 0 8px; background:#eee; border-radius:99px; height:10px; overflow:hidden;">
                <div style="width:{bar_pct}%; height:100%; background:{bar_color}; border-radius:99px;"></div>
            </div>

            <!-- Stat boxes -->
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
                    <div class="stat-box-value">{action}</div>
                </div>
            </div>

            <!-- Reason -->
            <div class="reason-box">
                <strong>Why this score?</strong><br>
                {reason}
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
        import pandas as pd

        df = pd.read_csv(uploaded_file)
        st.markdown(f"**{len(df)} leads loaded.** Preview:")
        st.dataframe(df.head(10), use_container_width=True)

        if st.button("Score all leads", type="primary"):
            # ── Replace the lambda below with your real score_lead call ──
            df["score"] = df.apply(
                lambda r: score_lead(
                    r.get("company_size", "1–10"),
                    r.get("industry", "Other"),
                    r.get("monthly_traffic", 0),
                    r.get("pricing_visits", 0),
                    r.get("email_opens", 0),
                    r.get("days_since_engagement", 30),
                    bool(r.get("demo_requested", False)),
                ),
                axis=1,
            )
            df["badge"] = df["score"].apply(lambda s: get_badge(s)[0])
            df["recommended_action"] = df.apply(
                lambda r: get_recommended_action(r["score"], r.get("days_since_engagement", 30)),
                axis=1,
            )
            df_sorted = df.sort_values("score", ascending=False).reset_index(drop=True)

            st.success("Scoring complete!")
            st.dataframe(df_sorted, use_container_width=True)

            csv_out = df_sorted.to_csv(index=False).encode("utf-8")
            st.download_button(
                "Download scored leads as CSV",
                data=csv_out,
                file_name="scored_leads.csv",
                mime="text/csv",
            )