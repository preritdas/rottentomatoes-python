# Non-local imports
import requests  # interact with RT website
import pyperclip as pc  # copy link to clipboard

# Project modules
from exceptions import *


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
    of `movie_name`. Copies the movie url to clipboard.

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
    rating = int(rating[0])

    # Try to copy url
    try:
        pc.copy(rt_url)
    except Exception as e:
        raise URLCopyError(e)
