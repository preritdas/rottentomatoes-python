"""Basic API to interact with the rottentomatoes-python package."""
from fastapi import FastAPI
from pydantic import BaseModel, Field

import rottentomatoes as rt


class MovieQuery(BaseModel):
    """Job request, querying for a movie."""
    name: str = Field(..., title="Name of the movie you're searching for.")

    class Config:
        schema_extra = {
            "example": {
                "name": "top gun"
            }
        }


class MovieAttributes(BaseModel):
    """Output, movie attributes."""
    name: str = Field(..., title="Name of the movie according to its page.")
    tomatometer: int = Field(..., title="Rotten Tomatoes Tomatometer.")
    audience_score: int = Field(..., title="Rotten Tomatoes audience score.")
    weighted_score: int = Field(
        ..., 
        title = "Internally formulated weighted score between tomatometer and audience score."
    )
    genres: list[str] = Field(..., title="List of genres.")
    rating: str = Field(..., title="Movie viewership rating, ex. PG.")
    duration: str = Field(..., title="String represented time, ex. 2h 11m.")
    year: str = Field(..., title="String represented year, ex. 1995.")
    actors: list[str] = Field(..., title="List of featured prominent actors.")
    directors: list[str] = Field(..., title="List of directors.")


app = FastAPI(
    name = "Rotten Tomatoes Scraper API",
    description = "Unofficial API getting data by scraping the Rotten Tomatoes website.",
    version = "0.5.11"
)


class Movies(BaseModel):
    movies: list[MovieAttributes] = Field(..., title="A list of movies with attributes.")


def build_movie(movie_name: str = "", force_url: str = "") -> MovieAttributes:
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


@app.get("/movie/{movie_name}", tags=["General"])
async def movie_attributes(movie_name: str) -> MovieAttributes:
    """Get a movie's attributes."""
    if "_" in movie_name:
        movie_name = movie_name.replace("_", " ")

    return build_movie(movie_name)


@app.get("/search/{movie_name}", tags=["General"])
async def multi_movie_search(movie_name: str) -> Movies:
    """Search for the movie and return a list of valid results."""
    results = rt.search.filter_searches(results=rt.search.search_results(movie_name))

    return {
        "movies": [
            build_movie(force_url=result.url) for result in results
        ]
    }
