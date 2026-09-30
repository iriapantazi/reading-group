#! /usr/bin/env python3

import argparse
from datetime import datetime
from beartype import beartype

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
        "--backend",
        type=str,
        default="requests",
        choices=["requests", "arxiv"],
        help="How to query arXiv: build the URL ourselves ('requests') "
        "or use the `arxiv` package.",
    )
    parser.add_argument(
        "--keywords",
        type=str,
        nargs="*",
        default=["ASR"],
        help="Keywords to search for in paper titles (OR-ed together). "
        "Pass `--keywords` with no values to search by author only.",
    )
    parser.add_argument(
        "--author",
        type=str,
        default="",
        help="The author of the paper to search for, e.g. 'Geoffrey Hinton'.",
    )
    parser.add_argument(
        "--from-year",
        type=int,
        default=2024,
        help="Earliest submission year to include.",
    )
    parser.add_argument(
        "--to-year",
        type=int,
        default=datetime.now().year,
        help="Latest submission year to include (defaults to the current year).",
    )
    parser.add_argument(
        "--max-results",
        type=int,
        default=5,
        help="The maximum number of results to return.",
    )
    parser.add_argument(
        "--storage-dir",
        type=str,
        default="storage",
        help="The storage location for the downloaded PDFs.",
    )
    parser.add_argument(
        "--model",
        type=str,
        default="meta-llama/Llama-3.2-3B-Instruct",
        choices=["meta-llama/Llama-3.2-3B-Instruct", "chatgpt4o"],
        help="The LLM model that will be used. "
        "For this PoC only Llama-3.2-3B-Instruct is supported.",
    )

    return parser.parse_args()
