import streamlit as st
import requests

# ---- FastAPI backend URL ----
API_URL = "https://your-vercel-url.vercel.app"  # replace with your deployed FastAPI URL

st.set_page_config(page_title="AI Research Companion", layout="wide")
st.title("📚 AI Research Companion")

# ---- Memory placeholder ----
memory = []

# ---- Sidebar: Fetch Paper ----
st.sidebar.subheader("📥 Fetch Paper from arXiv")
query = st.sidebar.text_input("Search keyword (e.g. transformers, LLM)")

if st.sidebar.button("Fetch Paper"):
    if not query:
        st.sidebar.error("Please enter a search keyword!")
    else:
        with st.spinner("Fetching and embedding paper..."):
            try:
                response = requests.get(f"{API_URL}/fetch_paper", params={"query": query})
                if response.status_code == 200:
                    st.sidebar.success(f"Downloaded & embedded: {response.json()['pdf']}")
                else:
                    st.sidebar.error(f"Error: {response.text}")
            except Exception as e:
                st.sidebar.error(f"Exception: {e}")

# ---- Main QnA ----
st.markdown("### 🔍 Ask a Question About the Paper")
user_question = st.text_input("Your question")

if st.button("Ask Question"):
    if not user_question:
        st.error("Please enter a question!")
    else:
        with st.spinner("Thinking..."):
            try:
                response = requests.post(f"{API_URL}/ask", json={"question": user_question})
                if response.status_code == 200:
                    answer = response.json()["answer"]
                    st.success("Answer:")
                    st.write(answer)
                    memory.append({"question": user_question, "answer": answer})
                else:
                    st.error(f"Error: {response.text}")
            except Exception as e:
                st.error(f"Exception: {e}")

# ---- Feedback ----
if memory:
    last_turn = memory[-1]
    st.markdown("---")
    st.subheader("Was this answer helpful?")
    col1, col2 = st.columns(2)
    if col1.button("👍 Thumbs Up"):
        requests.post(f"{API_URL}/feedback", json={
            "question": last_turn["question"],
            "answer": last_turn["answer"],
            "feedback": "thumbs_up"
        })
        st.success("Thanks for your feedback!")
    if col2.button("👎 Thumbs Down"):
        requests.post(f"{API_URL}/feedback", json={
            "question": last_turn["question"],
            "answer": last_turn["answer"],
            "feedback": "thumbs_down"
        })
        st.warning("We'll try to improve.")

# ---- Show Memory ----
if st.checkbox("🧠 Show last 3 memory turns"):
    for turn in memory[-3:]:
        st.markdown(f"**Q:** {turn['question']}")
        st.markdown(f"**A:** {turn['answer']}")
