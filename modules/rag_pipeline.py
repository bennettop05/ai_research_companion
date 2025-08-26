from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader
import os

# Lightweight embeddings
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def load_and_embed_pdf(pdf_path, persist_dir="db/", chunk_size=800, chunk_overlap=100):
    """
    Load a PDF, split it into chunks, embed them, and store in a persistent vector DB.
    """
    # Load PDF pages
    loader = PyPDFLoader(pdf_path)
    pages = loader.load()

    # Split into chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = splitter.split_documents(pages)

    # Ensure the vector DB directory exists
    os.makedirs(persist_dir, exist_ok=True)

    # Create Chroma vector DB and persist
    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=persist_dir
    )
    vectordb.persist()
    return vectordb

def query_rag(question, persist_dir="db/", top_k=15):
    """
    Query the persistent RAG vector store and return top_k relevant chunks.
    """
    vectordb = Chroma(persist_directory=persist_dir, embedding_function=embeddings)
    retriever = vectordb.as_retriever()
    docs = retriever.get_relevant_documents(question)

    # Return top_k results as combined context
    return "\n\n".join([doc.page_content for doc in docs[:top_k]])
