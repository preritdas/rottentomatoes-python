"""Standalone functions to fetch attributes about a movie."""
from bs4 import BeautifulSoup

# Non-local imports
import json
import requests  # interact with RT website
from typing import List, Dict, Union

# Project modules
from .exceptions import *
from . import search
from . import utils


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
    return content[start_idx + len(start_string):end_idx]


def _get_schema_json_ld(content: str) -> Dict:
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


def _get_score_details(content: str) -> Dict[str, Union[str, int, None]]:
    """Retrieves the scoreboard data for a movie. Scoreboard data
    typically contains audience score, ratings, duration etc.

    Args:
       content (str): The raw RT data for a movie.

    Returns:
        object: The scoreboard data for the movie.
    """
    soup = BeautifulSoup(content, 'html.parser')

    try:
        tomatometer_score = int(soup.find('rt-button', {'slot': 'criticsScore'}).text.strip("%\n"))
    except AttributeError:
        tomatometer_score = None
    try:
        audience_score = int(soup.find('rt-button', {'slot': 'audienceScore'}).text.strip("%\n"))
    except AttributeError:
        audience_score = None
    try:
        rating = soup.find('rt-text', {'slot': 'ratingsCode'}).text
    except AttributeError:
        rating = None
    try:
        release_date = soup.find('rt-text', {'slot': 'releaseDate'}).text.strip("Released ")
    except AttributeError:
        release_date = None
    try:
        duration = soup.find('rt-text', {'slot': 'duration'}).text
    except AttributeError:
        duration = None
    try:
        num_of_reviews_tomatometer = int(soup.find('rt-link', {'slot': 'criticsReviews'}).text.strip().split(" ")[0])
    except AttributeError:
        num_of_reviews_tomatometer = None
    try:
        synopsis = soup.find('rt-text', {'slot': 'content'}).text.strip()
    except AttributeError:
        synopsis = None

    return {"tomatometerScore": tomatometer_score, "audienceScore": audience_score, "rating": rating,
            "releaseDate": release_date, "duration": duration, "num_of_reviews_tomatometer": num_of_reviews_tomatometer,
            "synopsis": synopsis}


def _request(movie_name: str, raw_url: bool = False, force_url: str = "") -> str:
    """Scrapes Rotten Tomatoes for the raw website data, to be
    passed to each standalone function for parsing.

    Args:
        movie_name (str): Title of the movie. Case insensitive.
        raw_url (bool): Don't search for the movie, build the url manually.
        force_url (str): Use this url to scrape the site. Don't use this.

    Raises:
        LookupError: If the movie isn't found on Rotten Tomatoes.
        This could be due to a typo in entering the movie's name,
        duplicates, or other issues.

    Returns:
        str: The raw RT website data of the given movie.
    """
    if raw_url or force_url:
        rt_url = _movie_url(movie_name) if movie_name else force_url
    else:
        search_result = search.top_movie_result(movie_name)
        rt_url = search_result.url

    response = requests.get(rt_url, headers=utils.REQUEST_HEADERS)

    if response.status_code == 404:
        raise LookupError(
            "Unable to find that movie on Rotten Tomatoes.",
            f"Try this link to source the movie manually: {rt_url}"
        )

    return response.text


def movie_title(movie_name: str, content: str = None) -> str:
    """Search for the movie and return the queried title."""
    if content is None:
        content = _request(movie_name)

    soup = BeautifulSoup(content, 'html.parser')
    return soup.find('h1', {"slot": "titleIntro"}).text.strip()


def num_of_reviews(movie_name: str, content: str = None) -> Union[int, None]:
    """Search for the movie and return the number of critic
    reviews for the Tomatometer score."""

    if content is None:
        content = _request(movie_name)

    value = _get_score_details(content)['num_of_reviews_tomatometer']

    if not value:
        return None
    return value


def synopsis(movie_name: str, content: str = None) -> str:
    """ Search for the movie and return the synopsis """

    if content is None:
        content = _request(movie_name)

    value = _get_score_details(content)['synopsis']

    return value


def tomatometer(movie_name: str, content: str = None) -> Union[int, None]:
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
        None: If the movie doesn't have a tomatometer.
    """
    if content is None:
        content = _request(movie_name)

    value = _get_score_details(content)['tomatometerScore']

    if not value:
        return None
    return value


def audience_score(movie_name: str, content: str = None) -> Union[int, None]:
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
        None: If the movie doesn't have an audience score.
    """
    if content is None:
        content = _request(movie_name)

    value = _get_score_details(content)['audienceScore']

    if not value:
        return None
    return value


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


def weighted_score(movie_name: str, content: str = None) -> Union[int, None]:
    """
    2/3 tomatometer, 1/3 audience score. Returns None if both scores are None.
    If one score is None, the other is returned.
    """
    if content is None:
        content = _request(movie_name)

    t_score = tomatometer(movie_name, content)
    a_score = audience_score(movie_name, content)

    if t_score is None and a_score is None:
        return None

    if t_score is None:
        return a_score

    if a_score is None:
        return t_score

    return int((2 / 3) * t_score + ((1 / 3) * a_score))


def rating(movie_name: str, content: str = None) -> str:
    """Returns a `str` of PG, PG-13, R, etc."""
    if content is None:
        content = _request(movie_name)

    return _get_score_details(content)['rating']


def duration(movie_name: str, content: str = None) -> str:
    """Returns the duration, ex. 1h 32m."""
    if content is None:
        content = _request(movie_name)

    return _get_score_details(content)['duration']


def year_released(movie_name: str, content: str = None) -> str:
    """Returns a string of the year the movie was released."""
    if content is None:
        content = _request(movie_name)

    release_year = _get_score_details(
        content)['releaseDate'].split(',')[1].strip()

    return release_year


def actors(movie_name: str, max_actors: int = 5, content: str = None) -> List[str]:
    """
    Returns a list of the top 5 actors listed by Rotten Tomatoes.
    """
    if content is None:
        content = _request(movie_name)

    def _get_top_n_actors(html, n):
        soup = BeautifulSoup(html, 'html.parser')
        cast_items = soup.find_all('a', {'data-qa': 'person-item'})

        top_actors = []
        i = 0
        for cast_item in cast_items:
            if i == n:
                break
            name = cast_item.find('p', {'data-qa': 'person-name'}).text
            role = cast_item.find('p', {'data-qa': 'person-role'}).text
            if "Director" in role:
                continue
            top_actors.append(name)
            i += 1
        return top_actors

    return _get_top_n_actors(content, max_actors)


def directors(movie_name: str, max_directors: int = 10, content: str = None) -> List[str]:
    """Returns a list of all the directors listed
    by Rotten Tomatoes. Specify `max_directors` to only receive
    a certain number."""
    get_name = lambda x: x.split("/")[-1].replace("_", " ").title()
    if content is None:
        content = _request(movie_name)

    directors = _get_schema_json_ld(content)["director"][:max_directors]

    return [get_name(n["sameAs"]).replace("-", " ") for n in directors]


def image(movie_name: str, content: str = None) -> str:
    if content is None:
        content = _request(movie_name)

    return _get_schema_json_ld(content)['image']


def url(movie_name: str, content: str = None) -> str:
    if content is None:
        content = _request(movie_name)

    return _get_schema_json_ld(content)['url']


def critics_consensus(movie_name: str, content: str = None) -> str:
    if content is None:
        content = _request(movie_name)

    soup = BeautifulSoup(content, 'html.parser')

    return soup.find('div', {'id': 'critics-consensus'}).text.replace("Critics Consensus", "").replace(
        "\nRead Critics Reviews", "").strip()
