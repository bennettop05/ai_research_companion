import arxiv
import os

def fetch_arxiv_pdf(keyword: str, save_dir: str = "docs/") -> str:
    search = arxiv.Search(
        query=keyword,
        max_results=1,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )

    os.makedirs(save_dir, exist_ok=True)

    for result in search.results():
        filename = f"{result.title[:50].replace(' ', '_')}.pdf"
        filepath = os.path.join(save_dir, filename)
        result.download_pdf(filename=filepath)
        return filepath
    
    return "No paper found."
