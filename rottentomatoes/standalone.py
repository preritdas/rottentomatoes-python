"""Standalone functions to fetch attributes about a movie."""

# Non-local imports
import json
import requests  # interact with RT website
from typing import List

# Project modules
from .exceptions import *


def _movie_url(movie_name: str) -> str:
    """Generates a target url on the Rotten Tomatoes website given
    the name of a movie.

    Args:
        movie_name (str): Title of the movie. Any number of words.

    Returns:
        str: `str` url that should point to the movie's real page.
    """
    movie_name = movie_name.lower()
    all_words = movie_name.split(sep=' ')
    underscored = '_'.join(all_words)
    return 'https://www.rottentomatoes.com/m/' + underscored


def _extract(content: str, start_string: str, end_string: str) -> str:
    """Retrieves parts of the RT website data given a start string
    and an end string.

    Args:
        content (str): The raw RT data for a movie.
        start_string (str): The start of the data to be extracted.
        end_string (str): The end of the data to be extracted.

    Returns:
        string: A part of the raw RT data, from the start string to the
                end string.
    """
    start_idx = content.find(start_string)

    if start_idx == -1:
        return None

    end_idx = content.find(end_string, start_idx)
    return content[start_idx+len(start_string):end_idx]


def _get_schema_json_ld(content: str) -> object:
    """Retrieves the schema.org data model for a movie. This data
    typically contains Tomatometer score, genre etc.

    Args:
        content (str): The raw RT data for a movie.

    Returns:
        object: The schema.org data model for the movie.
    """
    return json.loads(
        _extract(
            content,
            '<script type="application/ld+json">',
            '</script>'
        )
    )


def _get_score_details(content: str) -> object:
    """Retrieves the scoreboard data for a movie. Scoreboard data
    typically contains audience score, ratings, duration etc.

    Args:
        movie_name (str): Title of the movie. Case insensitive.

    Returns:
        object: The scoreboard data for the movie.
    """
    return json.loads(
        _extract(
            content,
            '<script id="score-details-json" type="application/json">',
            '</script>'
        )
    )


def _request(movie_name: str) -> str:
    """Scrapes Rotten Tomatoes for the raw website data, to be
    passed to each standalone function for parsing.

    Args:
        movie_name (str): Title of the movie. Case insensitive.

    Raises:
        LookupError: If the movie isn't found on Rotten Tomatoes.
        This could be due to a typo in entering the movie's name,
        duplicates, or other issues.

    Returns:
        str: The raw RT website data of the given movie.
    """
    rt_url = _movie_url(movie_name)
    response = requests.get(rt_url)

    if response.status_code == 404:
        raise LookupError(
            "Unable to find that movie on Rotten Tomatoes.",
            f"Try this link to source the movie manually: {rt_url}"
        )

    return response.text


def tomatometer(movie_name: str, content: str = None) -> int:
    """Returns an integer of the Rotten Tomatoes tomatometer
    of `movie_name`. 

    Args:
        movie_name (str): Title of the movie. Case insensitive.

    Raises:
        LookupError: If the movie isn't found on Rotten Tomatoes.
        This could be due to a typo in entering the movie's name,
        duplicates, or other issues.

    Returns:
        int: Tomatometer of `movie_name`.
    """
    if content is None:
        content = _request(movie_name)

    return _get_score_details(content)['scoreboard']['tomatometerScore']


def audience_score(movie_name: str, content: str = None) -> int:
    """Returns an integer of the Rotten Tomatoes tomatometer
    of `movie_name`. 

    Args:
        movie_name (str): Title of the movie. Case insensitive.

    Raises:
        LookupError: If the movie isn't found on Rotten Tomatoes.
        This could be due to a typo in entering the movie's name,
        duplicates, or other issues.

    Returns:
        int: Tomatometer of `movie_name`.
    """
    if content is None:
        content = _request(movie_name)

    return _get_score_details(content)['scoreboard']['audienceScore']


def genres(movie_name: str, content: str = None) -> List[str]:
    """Returns an integer of the Rotten Tomatoes tomatometer
    of `movie_name`. Copies the movie url to clipboard.

    Args:
        movie_name (str): Title of the movie. Case insensitive.

    Raises:
        LookupError: If the movie isn't found on Rotten Tomatoes.
        This could be due to a typo in entering the movie's name,
        duplicates, or other issues.

    Returns:
        list[str]: List of genres.
    """
    if content is None:
        content = _request(movie_name)

    return _get_schema_json_ld(content)['genre']


def weighted_score(movie_name: str, content: str = None) -> int:
    """2/3 tomatometer, 1/3 audience score."""
    if content is None:
        content = _request(movie_name)

    return int((2/3) * tomatometer(movie_name, content=content) +
               (1/3) * audience_score(movie_name, content=content))


def rating(movie_name: str, content: str = None) -> str:
    """Returns a `str` of PG, PG-13, R, etc."""
    if content is None:
        content = _request(movie_name)

    return _get_score_details(content)['scoreboard']['rating']


def duration(movie_name: str, content: str = None) -> str:
    """Returns the duration, ex. 1h 32m."""
    if content is None:
        content = _request(movie_name)

    return_duration = _get_score_details(
        content)['scoreboard']['info'].split(',')[-1]
    return return_duration.replace(' ', '', 1)


def year_released(movie_name: str, content: str = None) -> str:
    """Returns a string of the year the movie was released."""
    if content is None:
        content = _request(movie_name)

    release_year = _get_score_details(
        content)['scoreboard']['info'].split(',')[0]
    return release_year


def actors(movie_name: str, max_actors: int = 100, content: str = None) -> List[str]:
    """Returns a list of all the actors listed
    by Rotten Tomatoes. Specify `max_actors` to only receive
    a certain number of the most prominent actors in the film."""
    if content is None:
        content = _request(movie_name)

    # Find all instances
    actors = []
    start_string = '<span class="characters subtle smaller" title="'
    while len(actors) < max_actors:
        actor = _extract(content, start_string, '">')
        # If no other actors can be extracted
        if actor is None:
            break
        actors.append(actor)
        # Continue traversing content for more actors
        content = content[content.find(start_string)+len(start_string):]

    return actors[:max_actors]
