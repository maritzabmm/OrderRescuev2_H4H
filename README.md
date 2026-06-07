# Order Rescue AI

Order Rescue AI is a prototype for anticipating SKU substitutions before dispatch. The goal is to reduce customer surprise, warehouse friction, and revenue at risk by assigning a substitution-risk score to each order line.

## Business Problem

When a requested product is unavailable close to dispatch time, the customer may receive a substitute without proactive notice. This creates complaints, loss of trust, and operational friction.

Order Rescue shifts the process from reactive to preventive:

- Predict substitution risk at the order-line level.
- Prioritize high-risk SKUs for warehouse review.
- Notify customers proactively when an adjustment may happen.
- Estimate revenue at risk and potential revenue rescue.

## Repository Structure

```text
.
├── database_clean.ipynb        # Data cleaning and final modeling table construction
├── eda.ipynb                   # Exploratory data analysis
├── modelo.ipynb                # Modeling notebook with leakage-aware split/evaluation
├── modelo_xgbooost.py          # Experimental XGBoost script
├── order_rescue_deploy/        # Streamlit Cloud-ready app
│   ├── app.py
│   ├── data_demo.csv           # Lightweight demo sample for public deployment
│   ├── requirements.txt
│   ├── README.md
│   └── models/
└── requirements.txt
```

## Data Notes

The full datasets are intentionally not tracked in Git because they are large and may exceed GitHub limits. They remain local under `bases/`.

The modeling grain is `id_linea`:

- `Orders` + `details_clean` merge by `id_pedido`.
- `Resultados` merges by `id_linea`.
- `fue_sustituida = 1` when an `id_linea` appears in `Resultados`.

This avoids inflating positives by joining substitutions at the full-order level.

## Streamlit Demo

The only app folder used for deployment is `order_rescue_deploy/`. It uses `data_demo.csv`, a lightweight sample intended for Streamlit Cloud.

Run locally:

```bash
cd order_rescue_deploy
pip install -r requirements.txt
streamlit run app.py
```

Deploy on Streamlit Community Cloud with:

```text
Main file path: app.py
```

Optional integrations can be configured through Streamlit secrets:

```toml
GEMINI_API_KEY = "..."
ELEVENLABS_API_KEY = "..."
TWILIO_ACCOUNT_SID = "..."
TWILIO_AUTH_TOKEN = "..."
TWILIO_PHONE_NUMBER = "..."
```

The app still works without these secrets using fallback messages.

## Recommended Presentation Framing

The technical pipeline and notebooks support the real modeling story. The Streamlit app in `order_rescue_deploy/` is the product demo showing how risk scores become operational actions for warehouse teams and customer communication.

## Public Deployment Links

For the final presentation, create two Streamlit Cloud apps from the same repository so you have a backup link.

### Primary App

```text
Repository: maritzabmm/OrderRescue_H4H
Branch: main
Main file path: order_rescue_deploy/app.py
Suggested URL: order-rescue-h4h.streamlit.app
```

### Backup App

Create a second Streamlit app pointing to the same repository and same file path, but choose a different app URL.

```text
Repository: maritzabmm/OrderRescue_H4H
Branch: main
Main file path: order_rescue_deploy/app.py
Suggested URL: order-rescue-backup-h4h.streamlit.app
```

This gives you two independent public Streamlit URLs. If one app sleeps, fails, or gets redeployed slowly, use the backup link.

> Note: `data_demo.csv` is a lightweight public demo sample. Full datasets are intentionally ignored because they are too large for GitHub/Streamlit Cloud.


## Important Folder Note

Use only this folder for the public app:

```text
order_rescue_deploy/
```

The older local folder `order rescue/` is ignored by Git and should not be used for Streamlit Cloud.
