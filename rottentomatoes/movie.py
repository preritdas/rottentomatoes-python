"""Contains classes that auto fetch all attributes."""

from . import standalone
from .exceptions import *


class Movie:
    """Accepts the name of a movie and automatically fetches all attributes.
    Raises an error if the movie is not found on Rotten Tomatoes.
    """
    def __init__(self, movie_title: str):
        self.movie_title = movie_title
        self.tomatometer = standalone.tomatometer(self.movie_title)
        self.audience_score = standalone.audience_score(self.movie_title)
        self.weighted_score = int((2/3) * self.tomatometer + (1/3) * self.audience_score)
        self.genres = standalone.genres(self.movie_title)
        self.rating = standalone.rating(self.movie_title)
        self.duration = standalone.duration(self.movie_title)
        self.year_released = standalone.year_released(self.movie_title)

    def __str__(self):
        return f"{self.movie_title.title()}, {self.rating}, {self.duration}.\n" \
            f"Released in {self.year_released}.\n" \
            f"Tomatometer: {self.tomatometer}\n" \
            f"Weighted score: {self.weighted_score}\n" \
            f"Audience Score: {self.audience_score}\nGenres - {self.genres}\n"
