from rottentomatoes import movie
from rottentomatoes import exceptions


def test_movie():
    m = movie.Movie("top gun")

    assert str(m)
    assert m.movie_title == "Top Gun"
    assert all(actor in m.actors for actor in {"Tom Cruise", "Val Kilmer"})
    assert m.duration == "1h 49m"
    assert all(genre in m.genres for genre in {"Action", "Adventure"})
    assert m.rating == "PG"
