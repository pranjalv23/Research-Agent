import os

import arxiv
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from llama_parse import LlamaParse

from connections import llama_parse_api_key


def process_pdf(path):
    parser = LlamaParse(
        api_key=llama_parse_api_key,
        result_type="markdown",
        num_workers=8,
        verbose=True,
        language="en",
    )

    docs = parser.load_data(path)
    with open(os.getcwd() + 'text.md', 'a') as f:  # Open the file in append mode ('a')
        for doc in docs:
            f.write(doc.text + '\n')

    markdown_path = os.path.join(os.getcwd(), 'text.md')
    loader = UnstructuredMarkdownLoader(markdown_path)
    documents = loader.load()
    os.remove(markdown_path)
    return documents


def process_arxiv(doc_id):
    paper = next(arxiv.Client().results(arxiv.Search(id_list=[doc_id])))
    paper.download_pdf(dirpath=os.getcwd(), filename="downloaded-paper.pdf")
    pdf_path = os.path.join(os.getcwd(), 'downloaded-paper.pdf')
    documents = process_pdf(pdf_path)
    return documents