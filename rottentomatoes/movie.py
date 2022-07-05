"""Contains classes that auto fetch all attributes."""

from .standalone import tomatometer, genres
from .exceptions import *


class Movie:
    """Accepts the name of a movie and automatically fetches all attributes.
    Raises an error if the movie is not found on Rotten Tomatoes.
    """
    def __init__(self, movie_title: str):
        self.movie_title = movie_title
        self.tomatometer = tomatometer(self.movie_title)
        self.genres = genres(self.movie_title)

    def __str__(self):
        return f"{self.movie_title.title()}. Tomatometer: {self.tomatometer}. " \
            f"Genres - {self.genres}."
