from rottentomatoes import standalone


def test_tomatometer():
    assert standalone.tomatometer("top gun") == 58


def test_movie_url():
    assert standalone._movie_url("top gun") == "https://www.rottentomatoes.com/m/top_gun"


def test_audience_score():
    assert standalone.audience_score("happy gilmore") == 85


def test_genres():
    assert standalone.genres("happy gilmore") == ["Comedy"]


def test_weighted_score():
    assert standalone.weighted_score("top gun maverick") == 97


def test_rating():
    assert standalone.rating("top gun maverick") == "PG-13"