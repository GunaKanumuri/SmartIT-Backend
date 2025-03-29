import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="🛠 Backend Ticket Tracker", layout="wide")
st.title("🛠 Admin Dashboard - Smart IT Helpdesk")

# Load ticket logs
log_path = "data/ticket_logs.csv"

if not os.path.exists(log_path):
    st.warning("No ticket logs found.")
    st.stop()

df = pd.read_csv(log_path)

# Filters
st.sidebar.header("📊 Filter Tickets")
status_filter = st.sidebar.multiselect("Filter by Status", df["status"].unique(), default=df["status"].unique())
category_filter = st.sidebar.multiselect("Filter by Category", df["category"].unique(), default=df["category"].unique())

filtered_df = df[df["status"].isin(status_filter) & df["category"].isin(category_filter)]

#st.subheader("🎟 All Tickets")
#st.dataframe(filtered_df, use_container_width=True)
st.subheader("✏️ Update a Ticket")

ticket_ids = filtered_df["ticket_id"].tolist()
selected_ticket = st.selectbox("Select Ticket ID to Update", ticket_ids)

ticket_row = df[df["ticket_id"] == selected_ticket].iloc[0]

# Show current info
st.markdown(f"**Issue:** {ticket_row['issue_description']}")
st.markdown(f"**Category:** {ticket_row['category']}")
st.markdown(f"**Current Status:** {ticket_row['status']}")
st.markdown(f"**Backend Note:** {ticket_row['backend_note']}")

# Editable fields
status = st.selectbox("Update Status", ["Open", "Pending", "Closed", "Reassigned"])
action_taken = st.text_input("Action Taken", ticket_row['action_taken'])
updated_by = st.text_input("Updated By", ticket_row['updated_by'])
reassigned_to = st.selectbox("Reassigned To (if any)", ["", "Hardware", "Software", "Network"], index=0)

# Save button
if st.button("💾 Save Update"):
    index = df[df["ticket_id"] == selected_ticket].index[0]

    df.at[index, 'status'] = status
    df.at[index, 'action_taken'] = action_taken
    df.at[index, 'updated_by'] = updated_by
    df.at[index, 'reassigned_to'] = reassigned_to

    df.to_csv(log_path, index=False)
    st.success("✅ Ticket updated successfully!")
