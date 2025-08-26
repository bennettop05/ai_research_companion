from transformers import pipeline

def summarize_text(text: str, max_length=150) -> str:
    """
    Summarize long text into concise version using HuggingFace pipeline.
    """
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    result = summarizer(text, max_length=max_length, min_length=50, do_sample=False)
    return result[0]["summary_text"]
