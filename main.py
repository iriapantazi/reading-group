#! /usr/bin/env python3

import argparse
from datetime import datetime

import feedparser
from beartype import beartype
from beartype.typing import List


@beartype
def parse_args() -> argparse.Namespace:

    parser = argparse.ArgumentParser(description="Parse arguments.")
    parser.add_argument(
        "--source",
        type=str,
        default="arxiv",
        choices=["arxiv", "semantic-scholar"],
        help="The name of the website to form the URL.",
    )
    parser.add_argument(
        "--keywords",
        type=str,
        nargs="+",
        help="The keywords to search for in the arXiv API.",
    )
    parser.add_argument(
        "--max-results",
        type=int,
        default=5,
        help="The maximum number of results to return.",
    )
    parser.add_argument(
        "--model",
        type=str,
        default="meta-llama/Llama-3.2-3B-Instruct",
        choices=["meta-llama/Llama-3.2-3B-Instruct", "chatgpt4o"],
        help="The LLM model that will be used. If it's llama-3 it will be .",
    )

    return parser.parse_args()


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
def do_requests(args: argparse.Namespace) -> None:
    """ """
    search_term = "llama-3"
    feed = feedparser.parse(
        f"http://export.arxiv.org/api/query?search_query=ti:{search_term}&sortBy=lastUpdatedDate&sortOrder=descending&max_results=2"
    )
    for entry in feed.entries:
        published = datetime.strptime(entry.published, "%Y-%m-%dT%H:%M:%SZ")
        if published.year >= 2024:
            print(f"{entry.title} ({published.date()})")
            print(entry.link)
            get_arxiv_pdf(entry.link)
            print()


if __name__ == "__main__":
    args = parse_args()
    print(args)
    do_requests(args)
