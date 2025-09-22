#! /usr/bin/env python3

import argparse
from datetime import datetime

import feedparser
import requests
from beartype import beartype
from beartype.typing import List
from langchain.schema import Document


@beartype
def get_arxiv_pdf(url: str) -> None:
    """Get the PDF link from the arXiv entry."""
    pdf_url = url.replace("abs", "pdf")
    response = requests.get(pdf_url)
    if response.status_code == 200:
        with open("arxiv.pdf", "wb") as f:
            f.write(response.content)
        print(f"Downloaded {pdf_url}")
    else:
        print(f"Failed to download {pdf_url}")


@beartype
def gen_arxiv_query(keywords: List[str], max_results: int) -> str:
    """Generate the arXiv query string."""
    if not keywords:
        raise ValueError("Keywords list cannot be empty.")
    if len(keywords) > 5:
        raise ValueError("Maximum of 5 keywords allowed.")
    if max_results == 1:
        return f"http://export.arxiv.org/api/query?search_query=ti:{keywords[0]}&sortBy=lastUpdatedDate&sortOrder=descending&max_results={max_results}"  # noqa: E501
    else:
        query = " OR ".join(keywords)
        return f"http://export.arxiv.org/api/query?search_query=ti:{query}&sortBy=lastUpdatedDate&sortOrder=descending&max_results={max_results}"  # noqa: E501


@beartype
def do_requests(args: argparse.Namespace) -> None:
    """ """

    # search_term = "llama-3"
    query = gen_arxiv_query(args.keywords, args.max_results)
    feed = feedparser.parse(query)
    docs = []
    for entry in feed.entries:
        published = datetime.strptime(entry.published, "%Y-%m-%dT%H:%M:%SZ")
        if published.year >= args.published_after:
            print(f"{entry.title} ({published.date()})")
            print(entry.link)
            print(entry.title)
            print(entry.summary)
            meta = f"Title: {entry.title}\nSummary: {entry.link}"
