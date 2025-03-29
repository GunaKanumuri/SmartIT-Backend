import streamlit as st
import joblib
import os
import pandas as pd
from datetime import datetime
import subprocess
from dotenv import load_dotenv
from utils.auto_git_push import auto_git_push
import sys
sys.path.append(r'C:\Users\gunak\AppData\Roaming\Python\Python313\site-packages')

import joblib
from utils.ticket_utils import generate_ticket_id

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
MODEL_PATH = "model/ticket_classifier.pkl"
model = joblib.load(MODEL_PATH)

# Ticket log path
LOG_PATH = "data/ticket_logs.csv"

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
    st.error("❌ Model file not found. Please ensure 'model/ticket_classifier.pkl' is in the same folder.")
    st.stop()

# Text input
user_id = st.text_input("👤 User ID (optional)", "guest")
ticket_text = st.chat_input("📝 Describe your IT issue (e.g. 'My laptop won't charge')")

if ticket_text:
    # Show user message
    with st.chat_message("user"):
        st.markdown(ticket_text)

    # Get prediction + probabilities
    probabilities = model.predict_proba([ticket_text])[0]
    labels = model.classes_
    prediction = labels[probabilities.argmax()]
    top_prob = max(probabilities)

    # Show bot response
    # Chat response to customer
    with st.chat_message("assistant"):
        if top_prob < 0.7:
            st.markdown(f"🤖 I’ve logged this issue under **{prediction}**. If it’s not the right match, our IT team will redirect it. ✅")
        else:
            st.markdown(f"🤖 Your issue has been logged under **{prediction}**. Our team will handle it shortly. ✅")

    # Build backend note
    top_indices = probabilities.argsort()[::-1]
    top_2 = [(labels[i], round(probabilities[i]*100, 2)) for i in top_indices[:2]]
    backend_note = f"Primary: {top_2[0][0]} ({top_2[0][1]}%), Secondary: {top_2[1][0]} ({top_2[1][1]}%)"

    # ✅ Show backend note only for admins
    if user_id.lower() == "admin":
        st.caption(f"📌 Internal Note: {backend_note}")

    # Generate ticket ID
    ticket_id = generate_ticket_id()

    # Log the ticket
    log_data = {
            "ticket_id": [ticket_id],
            "timestamp": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
            "user_id": [user_id],
            "issue_description": [ticket_text],
            "category": [prediction],
            "backend_note": [backend_note],
            "status": ["Open"],
            "action_taken": [""],
            "updated_by": [""],
            "reassigned_to": [""]
    }

    log_df = pd.DataFrame(log_data)
    log_path = "data/ticket_logs.csv"


    if os.path.exists(log_path):
        log_df.to_csv(log_path, mode='a', header=False, index=False)
    else:
        log_df.to_csv(log_path, index=False)

    st.toast("📝 Ticket logged to `ticket_logs.csv`")

    # GitHub push
    push_status = auto_git_push()
    st.toast(push_status)
