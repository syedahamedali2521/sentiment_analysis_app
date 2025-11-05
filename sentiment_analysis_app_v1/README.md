# Futuristic Sentiment Analysis App (BERT - Online)

This is a Streamlit web app that performs **sentiment analysis** using a Hugging Face DistilBERT model (downloaded at runtime). The UI uses a dark neon theme with glowing horizontal bars to visualize Positive / Neutral / Negative scores.

## Run locally

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the Streamlit app:
```bash
streamlit run app/app.py
```

Notes:
- The first time the app runs it will download the DistilBERT model (internet required).
- For bulk analysis, upload a CSV with a column named `text`.
- The app shows a glowing neon bar visualization for each analyzed text.
