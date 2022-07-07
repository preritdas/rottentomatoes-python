"""Contains classes that auto fetch all attributes."""

from .standalone import audience_score, duration, rating, tomatometer, genres
from .exceptions import *


class Movie:
    """Accepts the name of a movie and automatically fetches all attributes.
    Raises an error if the movie is not found on Rotten Tomatoes.
    """
    def __init__(self, movie_title: str):
        self.movie_title = movie_title
        self.tomatometer = tomatometer(self.movie_title)
        self.audience_score = audience_score(self.movie_title)
        self.weighted_score = int((2/3) * self.tomatometer + (1/3) * self.audience_score)
        self.genres = genres(self.movie_title)
        self.rating = rating(self.movie_title)
        self.duration = duration(self.movie_title)

    def __str__(self):
        return f"{self.movie_title.title()}, {self.rating}, {self.duration}.\n" \
            f"Tomatometer: {self.tomatometer}\n" \
            f"Weighted score: {self.weighted_score}\n" \
            f"Audience Score: {self.audience_score}\nGenres - {self.genres}\n"
