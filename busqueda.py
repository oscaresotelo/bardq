# from duckduckgo_search import DDGS

# with DDGS() as ddgs:
#     for r in ddgs.answers("manuel belgrano"):
#         print(r)
from duckduckgo_search import DDGS
from typing import Iterator, Dict, Optional

def text(
    keywords: str,
    region: str = "wt-wt",
    safesearch: str = "moderate",
    timelimit: Optional[str] = None,
    backend: str = "api",
) -> Iterator[Dict[str, Optional[str]]]:
    """DuckDuckGo text search generator. Query params: https://duckduckgo.com/params

    Args:
        keywords: keywords for query.
        region: wt-wt, us-en, uk-en, ru-ru, etc. Defaults to "wt-wt".
        safesearch: on, moderate, off. Defaults to "moderate".
        timelimit: d, w, m, y. Defaults to None.
        backend: api, html, lite. Defaults to api.
            api - collect data from https://duckduckgo.com,
            html - collect data from https://html.duckduckgo.com,
            lite - collect data from https://lite.duckduckgo.com.
    Yields:
        dict with search results.

    """
# with DDGS() as ddgs:
#     for r in ddgs.text('live free or die', region='wt-wt', safesearch='Off', timelimit='y'):
#         print(r)

# # Searching for pdf files
# with DDGS() as ddgs:
#     for r in ddgs.text('russia filetype:pdf', region='wt-wt', safesearch='Off', timelimit='y'):
#         print(r)

# # Using lite backend and limit the number of results to 10
from itertools import islice

with DDGS() as ddgs:
    ddgs_gen = ddgs.text("jorge alperovich", backend="lite")
    for r in islice(ddgs_gen, 10):
        print(r)