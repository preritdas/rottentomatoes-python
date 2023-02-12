from rottentomatoes import movie
from rottentomatoes import exceptions


def test_movie():
    m = movie.Movie("top gun maverick")

    assert str(m)
    assert m.movie_title == "Top Gun: Maverick"
    assert all(actor in m.actors for actor in {"Tom Cruise", "Miles Teller"})
    assert all(director in m.directors for director in {"Joseph Kosinski"})
    assert m.duration == "2h 11m"
    assert all(genre in m.genres for genre in {"Action", "Adventure"})
    assert m.rating == "PG-13"
