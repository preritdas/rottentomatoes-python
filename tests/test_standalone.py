from rottentomatoes import standalone
import pytest


def test_tomatometer(top_gun_mav_content):
    assert standalone.tomatometer("top gun maverick", content=top_gun_mav_content) == 96


def test_movie_url():
    """The old version, before using search."""
    assert standalone._movie_url("top gun") == "https://www.rottentomatoes.com/m/top_gun"


def test_movie_title(top_gun_mav_content):
    assert standalone.movie_title("top gun", top_gun_mav_content) == "Top Gun: Maverick"


def test_audience_score(happy_gilmore_content):
    assert standalone.audience_score("happy gilmore", happy_gilmore_content) == 85


@pytest.mark.skip(reason="Audience score for this movie was added.")
def test_no_audience_score(the_beast_content):
    assert standalone.audience_score("the beast", the_beast_content) is None


def test_genres(happy_gilmore_content):
    assert standalone.genres("happy gilmore", happy_gilmore_content) == ["Comedy"]


def test_weighted_score(top_gun_mav_content):
    assert standalone.weighted_score("top gun maverick", top_gun_mav_content) == 97


def test_rating(top_gun_mav_content):
    assert standalone.rating("top gun maverick", top_gun_mav_content) == "PG-13"


def test_duration(top_gun_mav_content):
    assert standalone.duration("top gun", top_gun_mav_content) == "2h 11m"


def test_year_released(forrest_gump_content):
    assert standalone.year_released("forrest gump", forrest_gump_content) == "1994"


def test_actors(forrest_gump_content):
    res = standalone.actors("forrest gump", 5, forrest_gump_content)

    for actor in [
        'Tom Hanks', 'Robin Wright', 'Gary Sinise', 'Mykelti Williamson', 'Sally Field'
    ]:
        assert actor in res


def test_directors(happy_gilmore_content):
    res = standalone.directors("happy gilmore", content=happy_gilmore_content)
    assert "Dennis Dugan" in res


def test_image(happy_gilmore_content):
    assert standalone.image("happy gilmore", happy_gilmore_content) == \
           'https://resizing.flixster.com/-XZAfHZM39UwaGJIFWKAE8fS0ak=/v3/t/assets/p17735_p_v8_aj.jpg'


def test_url(happy_gilmore_content):
    assert standalone.url("happy gilmore", happy_gilmore_content) == \
           'https://www.rottentomatoes.com/m/happy_gilmore'


def test_critics_consensus(happy_gilmore_content):
    assert standalone.critics_consensus("happy gilmore", happy_gilmore_content) == (
        "Those who enjoy Adam Sandler's schtick will find plenty to love "
        "in this gleefully juvenile take on professional golf; "
        "those who don't, however, will find it unfunny and forgettable."
    )


def test_num_of_reviews(happy_gilmore_content):
    num_reviews: int = standalone.num_of_reviews("happy gilmore", happy_gilmore_content)
    assert isinstance(num_reviews, int)
    assert num_reviews >= 55


def test_synopsis(happy_gilmore_content):
    assert standalone.synopsis("happy gilmore", happy_gilmore_content) == (
        "All Happy Gilmore (Adam Sandler) has ever wanted is to be a professional hockey player. But he soon "
        "discovers he may actually have a talent for playing an entirely different sport: golf. When his grandmother "
        "(Frances Bay) learns she is about to lose her home, Happy joins a golf tournament to try and win enough "
        "money to buy it for her. With his powerful driving skills and foulmouthed attitude, Happy becomes an "
        "unlikely golf hero -- much to the chagrin of the well-mannered golf professionals."
    )
