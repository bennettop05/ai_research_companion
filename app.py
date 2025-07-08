import streamlit as st
import os
from dotenv import load_dotenv
from arxiv_loader import fetch_arxiv_pdf
from rag_pipeline import load_and_embed_pdf, query_rag
from memory_manager import ConversationMemory
from logs.feedback_logger import log_feedback
from trace_logger import log_trace
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(page_title="AI Research Companion", layout="wide")
st.title("📚 AI Research Companion")

memory = ConversationMemory()

# --- Sidebar: Arxiv Paper Fetch ---
st.sidebar.subheader("📥 Fetch Paper from arXiv")
query = st.sidebar.text_input("Search keyword (e.g. transformers, LLM)")
if st.sidebar.button("Fetch Paper"):
    with st.spinner("Fetching and processing..."):
        pdf_path = fetch_arxiv_pdf(query)
        st.sidebar.success(f"Downloaded: {os.path.basename(pdf_path)}")
        load_and_embed_pdf(pdf_path)
        st.sidebar.success("Document embedded for RAG ✅")

# --- Main UI: Ask Question ---
st.markdown("### 🔍 Ask a Question About the Paper")
user_question = st.text_input("Your question")

if user_question:
    with st.spinner("Thinking..."):
        context = query_rag(user_question)
        prompt = f"""Answer the user's question using this context:\n\n{context}\n\nQ: {user_question}\nA:"""

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        answer = response.choices[0].message.content

        st.success("Answer:")
        st.write(answer)

        # Log to memory and trace
        memory.add(user_question, answer)
        log_trace(user_question, "RAG Context Retrieval", context, answer)

        # Feedback Section
        st.markdown("---")
        st.subheader("How was the answer?")
        col1, col2 = st.columns(2)

        if col1.button("👍 Thumbs Up"):
            log_feedback(user_question, answer, "thumbs_up")
            st.success("Thanks for your feedback!")

        if col2.button("👎 Thumbs Down"):
            log_feedback(user_question, answer, "thumbs_down")
            st.warning("We'll try to improve.")

# Optional: Show last 3 interactions
if st.checkbox("🧠 Show last 3 memory turns"):
    st.code(memory.get(), language="text")
