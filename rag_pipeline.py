# rag_pipeline.py

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.document_loaders import PyPDFLoader
import os

def load_and_embed_pdf(pdf_path, persist_dir="db/"):
    loader = PyPDFLoader(pdf_path)
    pages = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    chunks = splitter.split_documents(pages)

    os.makedirs(persist_dir, exist_ok=True)

    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=OpenAIEmbeddings(),
        persist_directory=persist_dir
    )

    vectordb.persist()
    return vectordb

def query_rag(question, persist_dir="db/"):
    vectordb = Chroma(persist_directory=persist_dir, embedding_function=OpenAIEmbeddings())
    retriever = vectordb.as_retriever()
    docs = retriever.get_relevant_documents(question)
    context = "\n\n".join([doc.page_content for doc in docs[:3]])
    return context
