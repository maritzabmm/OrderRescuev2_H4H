# Order Rescue AI Streamlit Demo

Public Streamlit demo for Order Rescue AI.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy

Use this folder as the repository root in Streamlit Community Cloud.

```text
Main file path: app.py
```

The app uses `data_demo.csv`, a lightweight sample created for public deployment. Full datasets are intentionally excluded from GitHub.

## Optional Secrets

```toml
GEMINI_API_KEY = "..."
ELEVENLABS_API_KEY = "..."
TWILIO_ACCOUNT_SID = "..."
TWILIO_AUTH_TOKEN = "..."
TWILIO_PHONE_NUMBER = "..."
```

Without secrets, the app still runs with static fallback messages.
