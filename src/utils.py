#! /usr/bin/env python3

import argparse
from datetime import datetime
from urllib.parse import quote, urlencode

import arxiv
import feedparser
import requests
from beartype import beartype
from beartype.typing import List


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
def _quote_term(term: str) -> str:
    """Wrap multi-word terms in quotes so arXiv treats them as a phrase."""
    term = term.strip().strip('"')
    return f'"{term}"' if " " in term else term


@beartype
def gen_search_query(
    keywords: List[str], author: str, from_year: int, to_year: int
) -> str:
    """Generate the raw arXiv search_query string (not URL-encoded).

    Both backends use this, so they send the same query.
    """
    keywords = [k for k in keywords if k.strip()]
    if not keywords and not author:
        raise ValueError("Provide at least one keyword or an author.")
    if len(keywords) > 5:
        raise ValueError("Maximum of 5 keywords allowed.")
    if from_year > to_year:
        raise ValueError("from_year cannot be later than to_year.")

    parts = []
    if keywords:
        terms = " OR ".join(f"ti:{_quote_term(k)}" for k in keywords)
        parts.append(f"({terms})")
    if author:
        parts.append(f"au:{_quote_term(author)}")
    parts.append(f"submittedDate:[{from_year}01010000 TO {to_year}12312359]")
    return " AND ".join(parts)


@beartype
def gen_arxiv_query(search_query: str, max_results: int) -> str:
    """Generate the full, URL-encoded arXiv API URL."""
    params = {
        "search_query": search_query,
        "sortBy": "lastUpdatedDate",
        "sortOrder": "descending",
        "max_results": max_results,
    }
    return f"https://export.arxiv.org/api/query?{urlencode(params, quote_via=quote)}"


@beartype
def do_requests(args: argparse.Namespace) -> None:
    """Query arXiv via our own URL, fetched with requests, parsed with feedparser."""
    search_query = gen_search_query(
        args.keywords, args.author, args.from_year, args.to_year
    )
    print(f"Query: {search_query}\n")
    response = requests.get(gen_arxiv_query(search_query, args.max_results), timeout=30)
    response.raise_for_status()
    feed = feedparser.parse(response.text)
    for entry in feed.entries:
        published = datetime.strptime(entry.published, "%Y-%m-%dT%H:%M:%SZ")
        print(f"{entry.title} ({published.date()})")
        print(entry.link)
        print(entry.summary)
        print()


@beartype
def do_arxiv_package(args: argparse.Namespace) -> None:
    """Query arXiv with the `arxiv` package (handles paging, rate limits, retries)."""
    search_query = gen_search_query(
        args.keywords, args.author, args.from_year, args.to_year
    )
    print(f"Query: {search_query}\n")
    client = arxiv.Client()
    search = arxiv.Search(
        query=search_query,
        max_results=args.max_results,
        sort_by=arxiv.SortCriterion.LastUpdatedDate,
        sort_order=arxiv.SortOrder.Descending,
    )
    for result in client.results(search):
        print(f"{result.title} ({result.published.date()})")
        print(result.entry_id)
        print(result.summary)
        print()
