#! /usr/bin/env python3

import argparse
from datetime import datetime

import feedparser
import requests
from beartype import beartype
from beartype.typing import List

from utils import do_requests, get_arxiv_pdf


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
        default=["llama-3"],
        help="The keywords to search for in the arXiv API.",
    )
    parser.add_argument(
        "--author",
        type=str,
        default="",
        help="The author of the paper to search for. Not currently supported.",
    )
    parser.add_argument(
        "--published-after",
        type=int,
        default=2024,
        help="The year after which the papers should be published.",
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
        default="/storage/",
        help="The storage location for the downloaded PDFs. "
        "This has to be a volume mounted to the container.",
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


if __name__ == "__main__":
    args = parse_args()
    print(args)
    do_requests(args)
