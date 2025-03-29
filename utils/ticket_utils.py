import pandas as pd
import os

def generate_ticket_id():
    file_path = "data/ticket_logs.csv"
    if not os.path.exists(file_path):
        return "TCK1001"
    
    df = pd.read_csv(file_path)
    if df.empty or 'ticket_id' not in df.columns:
        return "TCK1001"

    last_id = df['ticket_id'].iloc[-1]
    number = int(last_id.replace("TCK", ""))
    return f"TCK{number + 1}"
