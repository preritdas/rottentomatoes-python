"""Contains classes that auto fetch all attributes."""
from . import standalone


class Movie:
    """
    Accepts the name of a movie and automatically fetches all attributes.
    Raises `exceptions.LookupError` if the movie is not found on Rotten Tomatoes.
    """
    def __init__(self, movie_title: str = "", force_url: str = "") -> None:
        if not movie_title and not force_url:
            raise ValueError("You must provide either a movie_title or force_url.")

        if force_url:
            content = standalone._request(movie_name="", force_url=force_url)
        else:
            content = standalone._request(movie_name=movie_title)

        self.movie_title = standalone.movie_title(movie_title, content=content)
        self.tomatometer = standalone.tomatometer(self.movie_title, content=content)
        self.audience_score = standalone.audience_score(self.movie_title, content=content)
        self.weighted_score = standalone.weighted_score(self.movie_title, content=content)
        self.genres = standalone.genres(self.movie_title, content=content)
        self.rating = standalone.rating(self.movie_title, content=content)
        self.duration = standalone.duration(self.movie_title, content=content)
        self.year_released = standalone.year_released(self.movie_title, content=content)
        self.actors = standalone.actors(self.movie_title, content=content)
        self.directors = standalone.directors(self.movie_title, max_directors=5, content=content)
        self.image = standalone.image(self.movie_title, content=content)
        self.url = standalone.url(self.movie_title, content=content)
        self.critics_consensus = standalone.critics_consensus(self.movie_title, content=content)

    def __str__(self) -> str:
        return f"{self.movie_title.title()}, {self.rating}, {self.duration}.\n" \
            f"Released in {self.year_released}.\n" \
            f"Directed by {', '.join(self.directors)}.\n" \
            f"Tomatometer: {self.tomatometer}\n" \
            f"Weighted score: {self.weighted_score}\n" \
            f"Audience Score: {self.audience_score}\nGenres - {self.genres}\n" \
            f"Prominent actors: {', '.join(self.actors)}."

    def __eq__(self, other: "Movie") -> bool:
        return self.movie_title == other.movie_title
