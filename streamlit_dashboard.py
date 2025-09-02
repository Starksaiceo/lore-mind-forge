import streamlit as st
import requests
from datetime import datetime

API_BASE_URL = "https://your-xano-api-url/api/your-group-id"  # Replace this with your actual Xano API base URL

def fetch_data(endpoint):
    try:
        res = requests.get(f"{API_BASE_URL}/{endpoint}")
        return res.json()
    except Exception as e:
        return {"error": str(e)}

def post_goal(title, priority=1):
    try:
        payload = {
            "title": title,
            "priority": priority,
            "status": "pending"
        }
        res = requests.post(f"{API_BASE_URL}/goal_queue", json=payload)
        return res.status_code == 200
    except Exception as e:
        return False

# UI config
st.set_page_config(page_title="🧠 AI CEO Dashboard", layout="wide")

st.sidebar.title("👨‍💼 AI CEO Console")
st.sidebar.markdown("Control your automated business agent")

section = st.sidebar.radio("📊 Choose view", ["📋 Dashboard", "🎯 Add Goal", "🧠 Memory", "💰 Profits", "🛠️ Tools Used"])

if section == "📋 Dashboard":
    st.title("🧠 AI CEO Dashboard")
    st.subheader("Live Goal Overview")

    data = fetch_data("goal_queue")
    if "goal_queue" in data:
        for goal in data["goal_queue"]:
            with st.expander(f"🎯 {goal['title']}"):
                st.write(f"**Status**: {goal.get('status', 'pending')}")
                st.write(f"**Priority**: {goal.get('priority', 1)}")
                st.write(f"**Created**: {goal.get('created_at', 'unknown')}")
    else:
        st.warning("No goals found or API error.")

elif section == "🎯 Add Goal":
    st.title("➕ Add New Goal")
    goal_title = st.text_input("Goal title")
    priority = st.slider("Priority", 1, 10, 5)
    if st.button("Submit Goal"):
        if post_goal(goal_title, priority):
            st.success("✅ Goal submitted successfully!")
        else:
            st.error("❌ Failed to submit goal.")

elif section == "🧠 Memory":
    st.title("🧠 Agent Memory")
    st.info("Memory viewer coming soon...")

elif section == "💰 Profits":
    st.title("💰 Profit Tracker")
    st.info("Profit tracking UI coming soon...")

elif section == "🛠️ Tools Used":
    st.title("🛠️ Tools & Services")
    st.markdown("- OpenRouter\n- LangChain\n- Xano\n- Streamlit\n- Replit\n- ChromaDB\n- Stripe (planned)")