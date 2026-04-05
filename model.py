import os
import pickle
import numpy as np
import pandas as pd

from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

from config import MODEL_PATH, FEATURE_COLS, COMPANY_SIZE_MAP, INDUSTRY_MAP
from data_gen import generate_leads

def feature_engineering(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["company_size_enc"]    = out["company_size"].map(COMPANY_SIZE_MAP).fillna(0).astype(int)
    out["industry_enc"]        = out["industry"].map(INDUSTRY_MAP).fillna(8).astype(int)
    out["monthly_traffic_log"] = np.log1p(out["monthly_traffic"])
    out["demo_requested"]      = out["demo_requested"].astype(int)
    return out

def train(n_samples: int =5000) -> GradientBoostingRegressor:
    print("Genearting Training data...")
    df= generate_leads(n=n_samples)
    df= feature_engineering(df)


    X = df[FEATURE_COLS]
    y = df["score"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = GradientBoostingRegressor(
        n_estimators=300,
        learning_rate=0.05,
        max_depth=4,
        random_state=42,
    )
    model.fit(X_train, y_train)

    mae = mean_absolute_error(y_test, model.predict(X_test))
    print(f"Test MAE: {mae:.2f} points")

    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model, f)
    print(f"Model saved → {MODEL_PATH}")
    return model

def load_model() -> GradientBoostingRegressor:
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            f"No model found at '{MODEL_PATH}'. Run `python model.py` first."
        )
    with open(MODEL_PATH, "rb") as f:
        return pickle.load(f)
    

# AFTER (fixed) — use a separate variable name
def predict_score(
    company_size: str,
    industry: str,
    monthly_traffic: int,
    pricing_visits: int,
    email_opens: int,
    days_since_engagement: int,
    demo_requested: bool,
    model=None,
) -> int:
    if model is None:
        model = load_model()

    input_df = pd.DataFrame([{
        "company_size":           company_size,
        "industry":               industry,
        "monthly_traffic":        monthly_traffic,
        "pricing_visits":         pricing_visits,
        "email_opens":            email_opens,
        "days_since_engagement":  days_since_engagement,
        "demo_requested":         int(demo_requested),
    }])
    engineered = feature_engineering(input_df)
    raw = model.predict(engineered[FEATURE_COLS])[0]
    return int(np.clip(round(raw), 0, 100))

def score_dataframe(df: pd.DataFrame, model=None) -> pd.DataFrame:
    """Batch-score a DataFrame. Returns df with added 'score' column."""
    if model is None:
        model = load_model()
    fe = feature_engineering(df)
    raw = model.predict(fe[FEATURE_COLS])
    out = df.copy()
    out["score"] = np.clip(np.round(raw), 0, 100).astype(int)
    return out


if __name__ == "__main__":
    train()




