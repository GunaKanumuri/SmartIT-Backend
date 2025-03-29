# auto_git_push.py
import subprocess
import os
from dotenv import load_dotenv

load_dotenv()  # Load token from .env

def auto_git_push():
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        return "❌ GitHub token not found."

    # Replace with your GitHub repo
    remote = f"https://{token}@github.com/GunaKanumuri/smart-it-helpdesk.git"

    try:
        subprocess.run(["git", "add", "data/ticket_logs.csv"], check=True)
        subprocess.run(["git", "commit", "-m", "📝 Auto-logged ticket from app"], check=True)
        subprocess.run(["git", "push", remote, "main"], check=True)
        return "✅ Auto-pushed to GitHub!"
    except subprocess.CalledProcessError as e:
        return f"❌ Git push failed: {str(e)}"
