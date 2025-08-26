import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

# local modules
from modules.arxiv_loader import fetch_arxiv_pdf
from modules.rag_pipeline import load_and_embed_pdf, query_rag
from modules.memory_manager import ConversationMemory
from logs.feedback_logger import log_feedback
from logs.trace_logger import log_trace

# ---- Env & Client ----
load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "meta-llama/llama-3.1-8b-instruct")

if not OPENROUTER_API_KEY:
    st.error("❌ Missing OPENROUTER_API_KEY in .env")
    st.stop()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

# ---- Streamlit UI ----
st.set_page_config(page_title="AI Research Companion", layout="wide")
st.title("📚 AI Research Companion")

memory = ConversationMemory()

# ---- Sidebar: Fetch arXiv paper ----
st.sidebar.subheader("📥 Fetch Paper from arXiv")
query = st.sidebar.text_input("Search keyword (e.g. transformers, LLM)")

if st.sidebar.button("Fetch Paper"):
    with st.spinner("Fetching and processing..."):
        try:
            pdf_path = fetch_arxiv_pdf(query)
            st.sidebar.success(f"Downloaded: {os.path.basename(pdf_path)}")
            load_and_embed_pdf(pdf_path)
            st.sidebar.success("Document embedded for RAG ✅")
        except Exception as e:
            st.sidebar.error(f"Error: {e}")

# ---- Main QnA ----
st.markdown("### 🔍 Ask a Question About the Paper")
user_question = st.text_input("Your question")

if user_question:
    with st.spinner("Thinking..."):
        # fetch more context (larger window for richer answers)
        context = query_rag(user_question, top_k=15)

        system_prompt = (
            "You are an AI research assistant. "
            "Use the provided context from the paper as the primary source. "
            "If context is insufficient, add your own knowledge to fill gaps. "
            "Always clearly prefer paper information first, then supplement with general knowledge. "
            "Write answers in a clear, detailed, well-structured format with explanations."
        )

        user_prompt = f"""Context from the paper:
{context}

Question: {user_question}

Answer format:
1. 📄 Context-based Answer (from the paper)
2. 🌍 Additional Explanation (if paper context is missing)

Final Answer:
"""

        try:
            response = client.chat.completions.create(
                model=OPENROUTER_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.4,
                max_tokens=1200,   # ⬆ longer answers
            )

            # ✅ Safe extraction
            if response and response.choices and response.choices[0].message:
                answer = response.choices[0].message.content.strip()
            else:
                answer = "⚠️ No valid response from model."

            st.success("Answer:")
            st.write(answer)

            memory.add(user_question, answer)
            log_trace(user_question, "RAG Context Retrieval", context, answer)

            # ---- Feedback ----
            st.markdown("---")
            st.subheader("How was the answer?")
            col1, col2 = st.columns(2)
            if col1.button("👍 Thumbs Up"):
                log_feedback(user_question, answer, "thumbs_up")
                st.success("Thanks for your feedback!")
            if col2.button("👎 Thumbs Down"):
                log_feedback(user_question, answer, "thumbs_down")
                st.warning("We'll try to improve.")

        except Exception:
            # ❌ silently ignore model errors (no red scary box)
            pass

# ---- Show Memory ----
if st.checkbox("🧠 Show last 3 memory turns"):
    st.code(memory.get(), language="text")
