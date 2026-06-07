# Streamlit Cloud Deploy Guide

This project is ready to deploy from `coded_minds_test`.

## Files Streamlit needs

```text
order_rescue_deploy/app.py
order_rescue_deploy/data_demo.csv
order_rescue_deploy/requirements.txt
order_rescue_deploy/models/gradient_boosting_order_rescue.pkl
```

The full datasets are ignored on purpose.

## Create the primary public app

1. Go to https://share.streamlit.io
2. Click **Create app**.
3. Select the GitHub repository.
4. Configure:

```text
Branch: main
Main file path: order_rescue_deploy/app.py
```

5. Choose a public URL, for example:

```text
order-rescue-h4h.streamlit.app
```

## Create a backup public app

Repeat the same steps, using the same repository and same file path, but choose a second URL:

```text
order-rescue-backup-h4h.streamlit.app
```

Both apps can point to the same GitHub repo. Streamlit Cloud will treat them as two separate deployments, so you can keep one as backup for presentation day.

## Optional secrets

Add these only if you want Gemini, ElevenLabs, or Twilio live integrations:

```toml
GEMINI_API_KEY = "..."
ELEVENLABS_API_KEY = "..."
TWILIO_ACCOUNT_SID = "..."
TWILIO_AUTH_TOKEN = "..."
TWILIO_PHONE_NUMBER = "..."
```

The app still works without secrets because it has fallback messages.

## If deployment fails

Check these first:

- GitHub repo includes `order_rescue_deploy/data_demo.csv`.
- GitHub repo does not include `merged.csv` or `bases/`.
- Streamlit main file path is exactly `order_rescue_deploy/app.py`.
- `requirements.txt` exists inside `order_rescue_deploy/`.


## Which folder should I use?

Use only:

```text
order_rescue_deploy/
```

Do not deploy the old local folder `order rescue/`. It is ignored and kept only as a local working copy.
