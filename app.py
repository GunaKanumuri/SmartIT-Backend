import streamlit as st
import joblib
import os
import pandas as pd
from datetime import datetime
import subprocess
from dotenv import load_dotenv
from auto_git_push import auto_git_push
import sys
sys.path.append(r'C:\Users\gunak\AppData\Roaming\Python\Python313\site-packages')

import joblib


load_dotenv()  # Load token from .env

def auto_git_push():
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        return "GitHub token not found."

    # Remote URL with token auth
    remote = f"https://{token}@github.com/GunaKanumuri/smart-it-helpdesk.git"

    try:
        subprocess.run(["git", "add", "ticket_logs.csv"], check=True)
        subprocess.run(["git", "commit", "-m", "📝 Auto-logged ticket from app"], check=True)
        subprocess.run(["git", "push", remote, "main"], check=True)
        return "✅ Auto-pushed to GitHub!"
    except subprocess.CalledProcessError as e:
        return f"❌ Git push failed: {str(e)}"

# Constants
MODEL_PATH = "ticket_classifier.pkl"

# Title and instructions
st.set_page_config(page_title="Smart IT Helpdesk", layout="centered")
st.title("🚀 Smart IT Helpdesk Automation")
st.markdown("Enter your IT issue below, and our AI will classify it into one of the categories: **Hardware**, **Software**, or **Network**.")

# Load model
@st.cache_resource
def load_model(path):
    if os.path.exists(path):
        return joblib.load(path)
    else:
        return None

model = load_model(MODEL_PATH)

if model is None:
    st.error("❌ Model file not found. Please ensure 'ticket_classifier.pkl' is in the same folder.")
    st.stop()

# Text input
ticket_text = st.text_area("📝 Describe your IT issue:", placeholder="E.g., My laptop won't connect to Wi-Fi")

# Predict button
if st.button("🔍 Classify Ticket"):
    if ticket_text.strip() == "":
        st.warning("Please enter a valid issue description.")
    else:
        prediction = model.predict([ticket_text])[0]
        st.success(f"✅ **Predicted Category:** `{prediction}`")

        # Save log
        log_data = {
            "timestamp": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
            "ticket_text": [ticket_text],
            "predicted_category": [prediction]
        }

        log_df = pd.DataFrame(log_data)

        # Append to CSV
        log_file = "ticket_logs.csv"
        if os.path.exists(log_file):
            log_df.to_csv(log_file, mode='a', header=False, index=False)
        else:
            log_df.to_csv(log_file, index=False)

        st.info("📝 Ticket logged to `ticket_logs.csv`")
        # ✅ Auto-push to GitHub
        push_status = auto_git_push()
        st.info(push_status)
