import numpy as np 
import pandas as pd
import os

from config import COMPANY_SIZE_MAP, INDUSTRY_MAP

RANDOM_SEED=42
N_SAMPLES=5000

def generate_leads(n: int = N_SAMPLES, seed: int = RANDOM_SEED) -> pd.DataFrame:
    rng = np.random.default_rng(seed)

    company_sizes = list(COMPANY_SIZE_MAP.keys())
    industries    = list(INDUSTRY_MAP.keys())

    df = pd.DataFrame({
        "company_name":          [f"Company_{i}" for i in range(n)],
        "company_size":          rng.choice(company_sizes, n),
        "industry":              rng.choice(industries, n),
        "monthly_traffic":       rng.integers(500, 500_000, n),
        "pricing_visits":        rng.integers(0, 30, n),
        "email_opens":           rng.integers(0, 50, n),
        "days_since_engagement": rng.integers(0, 90, n),
        "demo_requested":        rng.integers(0, 2, n),   # 0 or 1
    })

    # ── Deterministic score used as training label (0–100) ───────────────────
    size_score    = df["company_size"].map(COMPANY_SIZE_MAP) / 5 * 20        # 0–20
    traffic_score = np.log1p(df["monthly_traffic"]) / np.log1p(500_000) * 15 # 0–15
    visit_score   = np.clip(df["pricing_visits"] / 10, 0, 1) * 25            # 0–25
    email_score   = np.clip(df["email_opens"] / 20, 0, 1) * 15               # 0–15
    recency_score = (1 - df["days_since_engagement"] / 90) * 15              # 0–15
    demo_score    = df["demo_requested"] * 10                                 # 0–10

    df["score"] = np.clip(
        size_score + traffic_score + visit_score +
        email_score + recency_score + demo_score + noise,
        0, 100
    ).round().astype(int)

    return df

def save_sample_csv(path: str = "sample_data/sample_leads.csv", n: int = 20):
    """Save a small human-readable sample (no score column) for bulk upload."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df = generate_leads(n=n)
    df.drop(columns=["score"]).to_csv(path, index=False)
    print(f"Sample CSV saved → {path}")


if __name__ == "__main__":
    df = generate_leads()
    print(df.head())
    print(f"\nGenerated {len(df)} rows. Score range: {df['score'].min()}–{df['score'].max()}")
    save_sample_csv()

    