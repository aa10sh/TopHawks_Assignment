from openai import OpenAI
from config import OPENAI_API_KEY, OPENAI_MODEL

from prompts import (
    SCORE_EXPLANATION_SYSTEM, SCORE_EXPLANATION_USER,
    RECOMMENDED_ACTION_SYSTEM, RECOMMENDED_ACTION_USER,
)

_client = None

def _get_client() -> OpenAI:
    global _client
    if _client is None:
        if not OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is not set in your .env file.")
        _client = OpenAI(api_key=OPENAI_API_KEY)
    return _client

def get_score_explanation(
    company_name: str,
    industry: str,
    company_size: str,
    monthly_traffic: int,
    pricing_visits: int,
    email_opens: int,
    days_since_engagement: int,
    demo_requested: bool,
    score: int,
    badge: str,
) -> str:
    """2-sentence human-readable explanation of the score."""
    user_msg = SCORE_EXPLANATION_USER.format(
        company_name=company_name,
        industry=industry,
        company_size=company_size,
        monthly_traffic=monthly_traffic,
        pricing_visits=pricing_visits,
        email_opens=email_opens,
        days_since_engagement=days_since_engagement,
        demo_requested="Yes" if demo_requested else "No",
        score=score,
        badge=badge,
    )
    resp = _get_client().chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": SCORE_EXPLANATION_SYSTEM},
            {"role": "user",   "content": user_msg},
        ],
        max_tokens=120,
        temperature=0.4,
    )
    return resp.choices[0].message.content.strip()

def get_recommended_action(
    score: int,
    badge: str,
    days_since_engagement: int,
    demo_requested: bool,
    pricing_visits: int,
) -> str:
    """Short (≤5 word) recommended next action string."""
    user_msg = RECOMMENDED_ACTION_USER.format(
        score=score,
        badge=badge,
        days_since_engagement=days_since_engagement,
        demo_requested="Yes" if demo_requested else "No",
        pricing_visits=pricing_visits,
    )
    resp = _get_client().chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": RECOMMENDED_ACTION_SYSTEM},
            {"role": "user",   "content": user_msg},
        ],
        max_tokens=20,
        temperature=0.2,
    )
    return resp.choices[0].message.content.strip()