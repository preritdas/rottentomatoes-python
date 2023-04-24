"""Search for movies. Use search page results to find absolute link. Write more/better docs later."""
import requests

import re
from typing import List

from . import utils
from .exceptions import LookupError


class SearchListing:
    """A search listing from the Rotten Tomatoes search page."""
    def __init__(self, has_tomatometer: bool, is_movie: bool, url: str) -> None:
        self.has_tomatometer = has_tomatometer
        self.is_movie = is_movie
        self.url = str(url)
        
    @classmethod
    def from_html(cls, html_snippet: str) -> "SearchListing":
        """
        Takes a snippet from the search page's HTML code.
        
        Use `re.findall(r"<search-page-media-row(.*?)</search-page-media-row>", content)`
        to separate the html into snippets, then feed each one to this method to create
        a `SearchListing` objects.
        """
        # Find the tomatometer
        tomato_qry = "tomatometerscore="
        tomato_loc = html_snippet.find(tomato_qry) + len(tomato_qry)
        tomato_snip = html_snippet[tomato_loc:tomato_loc+5]
        meter = tomato_snip.split('"')[1]
        has_tomatometer = bool(meter)
        
        # Find the url
        urls = re.findall(r'a href="(.*?)"', html_snippet)
        url = urls[0]
        
        # Determine if it's a movie
        is_movie = "/m/" in url
        
        return cls(has_tomatometer=has_tomatometer, is_movie=is_movie, url=url)
    
    def __str__(self) -> str:
        """Represent the SearchListing object."""
        return f"Tomatometer: {self.has_tomatometer}. URL: {self.url}. Is movie: {self.is_movie}."


def _movie_search_content(name: str) -> str:
    """Raw HTML content from searching for a movie."""
    url_name = "%20".join(name.split())
    url = f"https://www.rottentomatoes.com/search?search={url_name}"
    content = str(requests.get(url, headers=utils.REQUEST_HEADERS).content)
    
    # Remove misc quotes from conversion
    content = content[2:-1]
    return content


def search_results(name: str) -> List[SearchListing]:
    """Get a list of search results."""
    content = _movie_search_content(name)
    snippets = re.findall(r"<search-page-media-row(.*?)</search-page-media-row>", content)
    return [SearchListing.from_html(snippet) for snippet in snippets]


def filter_searches(results: List[SearchListing]) -> List[SearchListing]:
    """Filters search results for valid movies."""
    return list(filter(lambda result: result.is_movie and result.has_tomatometer, results))


def top_movie_result(name: str) -> SearchListing:
    """Get the first movie result that has a tomatometer."""
    results = search_results(name)
    filtered = filter_searches(results)
    
    if not filtered:
        raise LookupError("No movies found.")
        
    return filtered[0]
