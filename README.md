🧠 Neon Sentiment Analysis App
🌌 Overview

A futuristic AI-powered Sentiment Analysis web app built with Streamlit and Hugging Face Transformers (DistilBERT).
It analyzes any text, tweet, or product review and classifies the sentiment as Positive, Negative, or Neutral — with glowing neon visual feedback ✨.

🚀 Features

⚡ Real-time Sentiment Detection using BERT-based Transformer.

📊 Interactive Results Visualization with glowing bars and dynamic colors.

🧾 CSV Upload Support – Analyze multiple reviews or tweets at once.

🌈 Dark Neon UI for a futuristic and immersive look.

☁️ Deployed on Streamlit Cloud – accessible online instantly.

🧩 Tech Stack

Frontend/UI: Streamlit

Model: DistilBERT (via transformers pipeline)

Backend: Python

Data: CSV (optional input)

Styling: Custom CSS (neon glowing effects)

⚙️ Installation (Run Locally)
# Clone the repo
git clone https://github.com/syedahamedali2521/sentiment_analysis_app.git
cd sentiment_analysis_app/sentiment_analysis_app_v1

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app/app.py

📂 Project Structure
sentiment_analysis_app_v1/
│
├── app/
│   ├── app.py                # Streamlit frontend
│   ├── static/style.css      # Neon glowing styles
│   └── assets/               # Optional icons/images
│
├── src/
│   └── analyze_sentiment.py  # Hugging Face sentiment logic
│
├── data/                     # Example datasets (optional)
├── requirements.txt
└── README.md

💡 Example Use

Enter text such as:

“The movie was absolutely incredible, I loved it!”

🟢 Output → Positive (0.987)
with a glowing green bar animation ✨

🧑‍💻 Author

Syed Ahamed Ali
Made with ❤️ using Python, Transformers, and Streamlit.

🌐 Live Demo

👉 Launch on Streamlit Cloud
