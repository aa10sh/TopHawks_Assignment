# TopHawks_Assignment

# 🎯 Lead Scoring Tool

> **An intelligent B2B lead prioritization engine** — combining a trained ML model with GPT-powered explanations to help sales teams focus on the leads most likely to convert.

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35+-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-412991?style=flat-square&logo=openai&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-GradientBoosting-F7931E?style=flat-square&logo=scikit-learn&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-22c55e?style=flat-square)

---

## 📸 Demo

| Manual Scoring | Bulk Upload |
|---|---|
| Enter a lead's details and get an instant score, badge, recommended action, and GPT explanation | Upload a CSV of hundreds of leads and download a ranked, scored file in seconds |

---

## Live Streamlit Link:
 [[Click here for demo](https://tophawksassignment-myjtwwt6tauvbjunkvckxd.streamlit.app/)]

## 🧠 What It Does

Most CRMs score leads with rigid rule-based systems. This tool does it smarter:

1. **ML Model** — A `GradientBoostingRegressor` trained on 5,000 synthetic leads produces a continuous score (0–100) based on behavioral and firmographic signals
2. **LLM Layer** — GPT-4o-mini reads the lead's data and the score, then generates a natural-language explanation of *why* the lead scored that way and *what action* to take
3. **Clean UI** — A Streamlit interface that works for both one-off manual scoring and bulk CSV processing

---

## ✨ Features

- 🔢 **ML-powered scoring** — GradientBoosting model trained on firmographic + behavioral features
- 🤖 **GPT explanations** — Every score comes with a 2-sentence human-readable reason
- ⚡ **Recommended actions** — "Call within 24h", "Send case study", "Add to nurture" — context-aware, not hardcoded
- 📁 **Bulk upload** — Score an entire pipeline from a CSV; download results ranked by score
- 🏷️ **HOT / WARM / COLD badges** — Instant visual triage for sales reps
- 📊 **Progress bar + stat cards** — Engagement recency, pricing visits, and recommended action at a glance
- 🎨 **Dark-themed UI** — Polished, minimal interface built entirely in Streamlit with custom CSS

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                        app.py                           │
│              Streamlit UI  (2 tabs)                     │
│         Manual Input  │  Bulk CSV Upload                │
└────────────┬──────────┴──────────┬──────────────────────┘
             │                     │
     ┌───────▼──────┐      ┌───────▼──────┐
     │   model.py   │      │    llm.py    │
     │  Gradient    │      │  OpenAI API  │
     │  Boosting    │      │  GPT-4o-mini │
     │  Regressor   │      │              │
     └───────┬──────┘      └───────┬──────┘
             │                     │
     ┌───────▼──────┐      ┌───────▼──────┐
     │  data_gen.py │      │  prompts.py  │
     │  Synthetic   │      │  Prompt      │
     │  Training    │      │  Templates   │
     │  Data        │      │              │
     └──────────────┘      └──────────────┘
             │
     ┌───────▼──────┐
     │  config.py   │
     │  Thresholds  │
     │  Encodings   │
     │  API Keys    │
     └──────────────┘
```

---

## 🔬 ML Model Details

### Features Used

| Feature | Type | Signal |
|---|---|---|
| `company_size_enc` | Ordinal | Larger companies → higher deal value |
| `industry_enc` | Categorical | SaaS/Finance → higher conversion baseline |
| `monthly_traffic_log` | Log-transformed continuous | Log scale reduces skew from outliers |
| `pricing_visits` | Integer | High intent signal — pricing research = purchase consideration |
| `email_opens` | Integer | Engagement depth over 30-day window |
| `days_since_engagement` | Integer | Recency — lower = more likely still in buying mode |
| `demo_requested` | Binary | Strongest single conversion signal |

### Training
- **Algorithm:** `GradientBoostingRegressor` (scikit-learn)
- **Data:** 5,000 synthetically generated leads with deterministic scoring + Gaussian noise (σ=3)
- **Split:** 80/20 train/test
- **Metric:** Mean Absolute Error (MAE) on held-out test set
- **Output:** Continuous score clipped to [0, 100]

### Score → Badge Mapping
```
70–100  →  🔴 HOT   — High purchase intent, act immediately
40–69   →  🟡 WARM  — Engaged, needs nurturing
0–39    →  ⚪ COLD  — Low intent, add to long-term nurture
```

---

## 📁 Project Structure

```
lead-scoring-tool/
│
├── app.py              ← Streamlit UI (manual + bulk tabs, score card, CSS)
├── model.py            ← Feature engineering, model training, inference
├── data_gen.py         ← Synthetic lead data generator (5,000 rows)
├── llm.py              ← OpenAI API calls (explanation + recommended action)
├── prompts.py          ← All GPT prompt templates (separated for easy iteration)
├── config.py           ← API keys, score thresholds, feature encodings
│
├── model/
│   └── lead_scorer.pkl ← Saved model (generated by python model.py)
│
├── sample_data/
│   └── sample_leads.csv ← 20-row sample for testing bulk upload
│
├── .env.example        ← Environment variable template
├── requirements.txt    ← Python dependencies
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- An OpenAI API key → [platform.openai.com/api-keys](https://platform.openai.com/api-keys)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/lead-scoring-tool.git
cd lead-scoring-tool

# 2. Create and activate a virtual environment
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
cp .env.example .env
# Open .env and add your OpenAI API key:
# OPENAI_API_KEY=sk-proj-...

# 5. Train the ML model
python model.py
# → Generates 5,000 synthetic leads, trains model, saves to model/lead_scorer.pkl
# → Prints test MAE on completion

# 6. Launch the app
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 📋 Bulk Upload Format

The CSV must contain these columns (column order doesn't matter):

| Column | Type | Example |
|---|---|---|
| `company_name` | string | `NovaTech Solutions` |
| `industry` | string | `SaaS`, `Finance`, `Healthcare`, ... |
| `company_size` | string | `1–10`, `11–50`, `51–200`, `201–500`, `501–1000`, `1000+` |
| `monthly_traffic` | integer | `15000` |
| `pricing_visits` | integer | `5` |
| `email_opens` | integer | `8` |
| `days_since_engagement` | integer | `2` |
| `demo_requested` | 0 or 1 | `1` |

A ready-to-use sample file is included at `sample_data/sample_leads.csv`.

---

## 🔧 Configuration

All tunable parameters live in `config.py`:

```python
OPENAI_MODEL   = "gpt-4o-mini"   # swap to "gpt-4o" for higher quality explanations
HOT_THRESHOLD  = 70              # score >= 70 → HOT
WARM_THRESHOLD = 40              # score >= 40 → WARM
```

To retrain the model on more data:
```bash
python data_gen.py   # regenerates sample CSV
python model.py      # retrains and overwrites model/lead_scorer.pkl
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| UI | Streamlit + custom CSS |
| ML Model | scikit-learn GradientBoostingRegressor |
| LLM | OpenAI GPT-4o-mini via `openai` Python SDK |
| Data | NumPy + Pandas (synthetic generation) |
| Config | python-dotenv |

---

## 🔮 Potential Enhancements

- [ ] Connect to real CRM data (HubSpot / Salesforce API)
- [ ] Replace synthetic training data with historical closed/lost deal data
- [ ] Add SHAP values for per-feature score contribution visualization
- [ ] Authentication layer for multi-user sales team access
- [ ] Webhook integration to auto-score new inbound leads
- [ ] A/B test different GPT prompt strategies and track explanation quality

---

## 👤 Author

Built by **Adarsh Singh**
