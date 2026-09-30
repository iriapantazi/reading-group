# Reading Group

## Introduction

This utility queries ArXiV for keywords and retrieves recently published articles
along with their summary.
Still a WIP as summarization has not been implemented yet.

## Instructions

```bash
pip install -r requirements.txt

huggingface-cli login --token $HF_TOKEN

# see help for supported arguments
python src/main.py --help
```

## Forming a request

A request is a set of command-line flags. The script turns them into a single
arXiv search query, prints that query, then prints the title, date, link and
abstract of each match.

### Flags

| Flag                         | Default      | What it does                                                 |
| ---------------------------- | ------------ | ------------------------------------------------------------ |
| `--keywords KW [KW ...]`     | `ASR`        | Up to 5 keywords                                             |
| `--author NAME`              | none         | Author name, e.g. `"Tara Sainath"`. AND-ed with the keywords |
| `--from-year YEAR`           | `2024`       | Earliest submission year                                     |
| `--to-year YEAR`             | current year | Latest submission year                                       |
| `--max-results N`            | `5`          | Maximum number of papers to return                           |
| `--backend {requests,arxiv}` | `requests`   | Choice of [Backends](#backends)                              |

`--source`, `--storage-dir` and `--model` are accepted but not used yet.

####  Examples

```bash
# Several keywords, one of them multi-word; single year
python src/main.py --keywords "speech recognition" conformer --from-year 2024 --to-year 2024

# Same request with the other backend, to compare
python src/main.py --backend arxiv --keywords attention --author "Tara Sainath" --from-year 2022
```

Invalid requests fail before anything is sent:

- no keywords **and** no author
- more than 5 keywords
- `--from-year` later than `--to-year`

### Backends

Both backends send the **same** query string, so their results should match.

- `requests` builds the API URL by hand, fetches it with `requests` and parses
  the Atom feed with `feedparser`. It doesn't yet wait between calls, so leave
  ~3 s between runs.
- `arxiv` uses the [`arxiv`](https://github.com/lukasschwab/arxiv.py) package,
  which handles paging, the rate limit (3 s between requests) and retries.

### Testing queries directly against the API

To try query syntax without the script, call the API with `curl`. Spaces become
`%20` and double quotes become `%22`:

```bash
curl "https://export.arxiv.org/api/query?search_query=ti:%22speech%20recognition%22%20AND%20cat:cs.CL&max_results=2"
```

Use `https://`. arXiv redirects `http://`, and some clients (e.g. `feedparser`)
then silently return nothing.

arXiv query syntax, useful when experimenting:

| Prefix | Field                           |
| ------ | ------------------------------- |
| `ti:`  | title                           |
| `au:`  | author                          |
| `abs:` | abstract                        |
| `cat:` | category, e.g. `cs.CL`, `cs.LG` |
| `all:` | all of the above                |

- Operators: `AND`, `OR`, `ANDNOT`, with parentheses for grouping.
- `"..."` matches an exact phrase.
- Date filter: `submittedDate:[YYYYMMDDHHMM TO YYYYMMDDHHMM]`.

The script only uses `ti:`, `au:` and `submittedDate` for now. Full reference:
<https://info.arxiv.org/help/api/user-manual.html>.

### Things to be aware of

- Keywords only match **titles**. A paper that mentions your keyword only in
  its abstract won't show up.
- Author matching is by name, so people who share a name are mixed together.
  Very common names give noisy results.
- `--max-results` limits how many papers are returned, not how many match. Raise
  it if a year range seems to be missing papers.

## Features

- [ ] uv
- [ ] option for external provider
- [ ] Save to markdown file
- [ ] Summarization
- [ ] RAG training
