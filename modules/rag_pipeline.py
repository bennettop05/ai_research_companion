from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
import os
import pickle

# Lightweight embeddings
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def load_and_embed_pdf(pdf_path, faiss_index_path="db/faiss_index", chunk_size=800, chunk_overlap=100):
    """
    Load a PDF, split it into chunks, embed them, and store in FAISS vector DB.
    """
    # Load PDF pages
    loader = PyPDFLoader(pdf_path)
    pages = loader.load()

    # Split into chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = splitter.split_documents(pages)

    # Create FAISS vector DB
    vectordb = FAISS.from_documents(chunks, embeddings)

    # Save FAISS index (binary + metadata)
    os.makedirs(os.path.dirname(faiss_index_path), exist_ok=True)
    faiss_index_file = faiss_index_path + ".pkl"
    with open(faiss_index_file, "wb") as f:
        pickle.dump(vectordb, f)

    return vectordb


def query_rag(question, faiss_index_path="db/faiss_index", top_k=15):
    """
    Query the FAISS vector store and return top_k relevant chunks.
    """
    faiss_index_file = faiss_index_path + ".pkl"
    if not os.path.exists(faiss_index_file):
        raise FileNotFoundError("FAISS index not found. Run load_and_embed_pdf first.")

    # Load FAISS index
    with open(faiss_index_file, "rb") as f:
        vectordb = pickle.load(f)

    retriever = vectordb.as_retriever(search_kwargs={"k": top_k})
    docs = retriever.get_relevant_documents(question)

    # Return combined context
    return "\n\n".join([doc.page_content for doc in docs])
