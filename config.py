import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY=os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL   = "gpt-4o-mini" 
print("KEY LOADED:", os.getenv("OPENAI_API_KEY", "NOT FOUND")[:12] + "...")
MODEL_PATH = "model/lead_scorer.pkl"

HOT_THRESHOLD=70
WARM_THRESHOLD=40

FEATURE_COLS = [
    "company_size_enc",
    "industry_enc",
    "monthly_traffic_log",
    "pricing_visits",
    "email_opens",
    "days_since_engagement",
    "demo_requested",
]

COMPANY_SIZE_MAP = {
    "1–10":     0,
    "11–50":    1,
    "51–200":   2,
    "201–500":  3,
    "501–1000": 4,
    "1000+":    5,
}

INDUSTRY_MAP = {
    "SaaS":          0,
    "E-commerce":    1,
    "Healthcare":    2,
    "Finance":       3,
    "Manufacturing": 4,
    "Education":     5,
    "Retail":        6,
    "Real Estate":   7,
    "Other":         8,
}