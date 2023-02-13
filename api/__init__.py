"""Basic API to interact with the rottentomatoes-python package."""
from fastapi import FastAPI

import rottentomatoes as rt

from . import models


app = FastAPI(
    title = "Rotten Tomatoes Scraper API",
    description = "Unofficial API getting data by scraping the Rotten Tomatoes website.",
    version = "0.5.12"
)


def build_movie(movie_name: str = "", force_url: str = "") -> models.MovieAttributes:
    """Construct a dictionary adhering to MovieAttributes."""
    if force_url:
        movie = rt.Movie(force_url=force_url)
    else:
        movie = rt.Movie(movie_title=movie_name)

    return {
        "name": movie.movie_title,
        "tomatometer": movie.tomatometer,
        "audience_score": movie.audience_score,
        "weighted_score": movie.weighted_score,
        "genres": movie.genres,
        "rating": movie.rating,
        "duration": movie.duration,
        "year": movie.year_released,
        "actors": movie.actors,
        "directors": movie.directors
    }


@app.get("/", tags=["Tests"])
async def test_homepage() -> str:
    """Check if the API is live."""
    return "API is live. See /docs or /redoc for endpoints and usage instructions."


@app.get("/movie/{movie_name}", tags=["General"])
async def movie_attributes(movie_name: str) -> models.MovieAttributes:
    """Get a movie's attributes."""
    if "_" in movie_name:
        movie_name = movie_name.replace("_", " ")

    return build_movie(movie_name)


@app.get("/search/{movie_name}", tags=["General"])
async def multi_movie_search(movie_name: str) -> models.Movies:
    """Search for the movie and return a list of valid results."""
    results = rt.search.filter_searches(results=rt.search.search_results(movie_name))

    return {
        "movies": [
            build_movie(force_url=result.url) for result in results
        ]
    }
