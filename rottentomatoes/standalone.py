"""Standalone functions to fetch attributes about a movie."""

# Non-local imports
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


def _request(movie_name: str) -> str:
    """Scrapes Rotten Tomatoes for the raw website data, to be
    passed to each standalone function for parsing."""
    rt_url = _movie_url(movie_name)
    response = requests.get(rt_url)
    return str(response.content)


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
        rt_url = _movie_url(movie_name)
        response = requests.get(rt_url)
        content = str(response.content)
    
    location_key = content.find('"ratingValue":"')
    if location_key == -1:
        raise LookupError(
            "Unable to find that movie on Rotten Tomatoes.", 
            f"Try this link to source the movie manually: {_movie_url(movie_name)}"
        )
    rating_block_location = location_key + len('"ratingValue":"') - 1
    rating_block = content[rating_block_location:rating_block_location+5]

    # Split and parse
    no_first_quote = rating_block[1:]
    rating = no_first_quote.split('"')
    return int(rating[0])


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
        rt_url = _movie_url(movie_name)
        response = requests.get(rt_url)
        content = str(response.content)

    # Test movie exists
    if content.find('"ratingValue":"')== -1:
        raise LookupError(
            "Unable to find that movie on Rotten Tomatoes.", 
            f"Try this link to source the movie manually: {_movie_url(movie_name)}"
        )
    location_key = content.find('"audienceScore":')
    rating_block_location = location_key + len('"audienceScore":')
    rating_block = content[rating_block_location:rating_block_location+5]

    # Split and parse
    rating = rating_block.split(',')
    return int(rating[0])


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
        rt_url = _movie_url(movie_name)
        response = requests.get(rt_url)
        content = str(response.content)

    location_key = content.find('"genre":') 
    if location_key == -1:
        raise LookupError(
            "Unable to find that movie on Rotten Tomatoes.", 
            f"Try this link to source the movie manually: {_movie_url(movie_name)}"
        )
    rating_block_location = location_key + len('"genre":')
    rating_block = content[rating_block_location:rating_block_location+50]
    genres = rating_block[1:].split(']')[0].split(',')  # list of genres
    return list(map(lambda x: x.replace('"', ''), genres))  # remove quotes from items    


def weighted_score(movie_name: str, content: str = None) -> int:
    """2/3 tomatometer, 1/3 audience score."""
    if content is None:
        rt_url = _movie_url(movie_name)
        response = requests.get(rt_url)
        content = str(response.content)

    return int((2/3) * tomatometer(movie_name, content=content) + \
        (1/3) * audience_score(movie_name, content=content))


def rating(movie_name: str, content: str = None) -> str:
    """Returns a `str` of PG, PG-13, R, etc."""
    if content is None:
        rt_url = _movie_url(movie_name)
        response = requests.get(rt_url)
        content = str(response.content)

    # Test movie exists
    if content.find('"ratingValue":"')== -1:
        raise LookupError(
            "Unable to find that movie on Rotten Tomatoes.", 
            f"Try this link to source the movie manually: {_movie_url(movie_name)}"
        )
    location_key = content.find('"contentRating":"')
    rating_block_location = location_key + len('"audienceScore":"')
    rating_block = content[rating_block_location:rating_block_location+5]

    # Split and parse
    return rating_block.split('"')[0]


def duration(movie_name: str, content: str = None) -> str:
    """Returns the duration, ex. 1h 32m."""
    if content is None:
        rt_url = _movie_url(movie_name)
        response = requests.get(rt_url)
        content = str(response.content)

    # Test movie exists
    if content.find('"ratingValue":"')== -1:
        raise LookupError(
            "Unable to find that movie on Rotten Tomatoes.", 
            f"Try this link to source the movie manually: {_movie_url(movie_name)}"
        )
    location_key = content.find('"rating":"')
    rating_block_end = location_key - 2
    return_duration = content[rating_block_end-10:rating_block_end].split(',')[-1]
    return return_duration.replace(' ', '', 1)


def year_released(movie_name: str, content: str = None) -> str:
    """Returns a string of the year the movie was released."""
    if content is None:
        rt_url = _movie_url(movie_name)
        response = requests.get(rt_url)
        content = str(response.content)

    # Test movie exists
    if content.find('"ratingValue":"')== -1:
        raise LookupError(
            "Unable to find that movie on Rotten Tomatoes.", 
            f"Try this link to source the movie manually: {_movie_url(movie_name)}"
        )
    location_key = content.find('"cag[release]":"')
    start = location_key+len('"cag[release]":"')
    return content[start:start+4]


def actors(movie_name: str, max_actors: int = 100, content: str = None) -> List[str]:
    """Returns a list of all the actors listed
    by Rotten Tomatoes. Specify `max_actors` to only receive
    a certain number of the most prominent actors in the film."""
    if content is None:
        rt_url = _movie_url(movie_name)
        response = requests.get(rt_url)
        content = str(response.content)

    # Test movie exists
    if content.find('"ratingValue":"')== -1:
        raise LookupError(
            "Unable to find that movie on Rotten Tomatoes.", 
            f"Try this link to source the movie manually: {_movie_url(movie_name)}"
        )
    
    # Find all instances
    actors = []
    while True:
        location_key = content.find('<span class="characters subtle smaller" title="')
        # Check if there are more
        if location_key == -1:
            break
        actor_start = location_key + \
            len('<span class="characters subtle smaller" title="') 
        actor = content[actor_start:actor_start+50].split('"')[0]
        actors.append(actor)
        content = content[actor_start:]  # remove this actor, on to the next

    return actors[:max_actors]
