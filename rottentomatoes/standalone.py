"""Standalone functions to fetch attributes about a movie."""

# Non-local imports
import requests  # interact with RT website

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


def tomatometer(movie_name: str) -> int:
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
    rt_url = _movie_url(movie_name)

    response = requests.get(rt_url)
    content = str(response.content)
    location_key = content.find('"ratingValue":"')
    if location_key == -1:
        raise LookupError(
            "Unable to find that movie on Rotten Tomatoes.", 
            f"Try this link to source the movie manually: {rt_url}"
        )
    rating_block_location = location_key + len('"ratingValue":"') - 1
    rating_block = content[rating_block_location:rating_block_location+5]

    # Split and parse
    no_first_quote = rating_block[1:]
    rating = no_first_quote.split('"')
    return int(rating[0])


def audience_score(movie_name: str) -> int:
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
    rt_url = _movie_url(movie_name)

    response = requests.get(rt_url)
    content = str(response.content)

    # Test movie exists
    if content.find('"ratingValue":"')== -1:
        raise LookupError(
            "Unable to find that movie on Rotten Tomatoes.", 
            f"Try this link to source the movie manually: {rt_url}"
        )
    location_key = content.find('"audienceScore":')
    rating_block_location = location_key + len('"audienceScore":')
    rating_block = content[rating_block_location:rating_block_location+5]

    # Split and parse
    rating = rating_block.split(',')
    return int(rating[0])


def genres(movie_name: str) -> list[str]:
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
    rt_url = _movie_url(movie_name)

    response = requests.get(rt_url)
    content = str(response.content)
    location_key = content.find('"genre":') 
    if location_key == -1:
        raise LookupError(
            "Unable to find that movie on Rotten Tomatoes.", 
            f"Try this link to source the movie manually: {rt_url}"
        )
    rating_block_location = location_key + len('"genre":')
    rating_block = content[rating_block_location:rating_block_location+50]
    genres = rating_block[1:].split(']')[0].split(',')  # list of genres
    return list(map(lambda x: x.replace('"', ''), genres))  # remove quotes from items    


def weighted_score(movie_name: str) -> int:
    """2/3 tomatometer, 1/3 audience score."""
    return int((2/3) * tomatometer(movie_name) + (1/3) * audience_score(movie_name))


def rating(movie_name: str) -> str:
    """Returns a `str` of PG, PG-13, R, etc."""
    rt_url = _movie_url(movie_name)

    response = requests.get(rt_url)
    content = str(response.content)

    # Test movie exists
    if content.find('"ratingValue":"')== -1:
        raise LookupError(
            "Unable to find that movie on Rotten Tomatoes.", 
            f"Try this link to source the movie manually: {rt_url}"
        )
    location_key = content.find('"contentRating":"')
    rating_block_location = location_key + len('"audienceScore":"')
    rating_block = content[rating_block_location:rating_block_location+5]

    # Split and parse
    return rating_block.split('"')[0]


def duration(movie_name: str) -> str:
    """Returns the duration, ex. 1h 32m."""
    rt_url = _movie_url(movie_name)

    response = requests.get(rt_url)
    content = str(response.content)

    # Test movie exists
    if content.find('"ratingValue":"')== -1:
        raise LookupError(
            "Unable to find that movie on Rotten Tomatoes.", 
            f"Try this link to source the movie manually: {rt_url}"
        )
    location_key = content.find('"rating":"')
    rating_block_end = location_key - 2
    return_duration = content[rating_block_end-10:rating_block_end].split(',')[-1]
    return return_duration.replace(' ', '', 1)
