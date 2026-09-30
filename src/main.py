#! /usr/bin/env python3


from parser import parse_args
from utils import do_arxiv_package, do_requests

if __name__ == "__main__":
    args = parse_args()
    print(args)
    if args.backend == "arxiv":
        do_arxiv_package(args)
    else:
        do_requests(args)
