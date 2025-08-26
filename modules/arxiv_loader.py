import os
import arxiv
import requests

def fetch_arxiv_pdf(query, save_dir="data"):
    os.makedirs(save_dir, exist_ok=True)
    search = arxiv.Search(query=query, max_results=1, sort_by=arxiv.SortCriterion.Relevance)
    result = next(search.results())
    pdf_url = result.pdf_url
    pdf_path = os.path.join(save_dir, f"{result.entry_id.split('/')[-1]}.pdf")

    if not os.path.exists(pdf_path):
        r = requests.get(pdf_url)
        with open(pdf_path, "wb") as f:
            f.write(r.content)
    return pdf_path
