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

    class Config:
        schema_extra = {
            "example": {
                "name": "Bad Boys for Life",
                "tomatometer": 76,
                "audience_score": 96,
                "weighted_score": 82,
                "genres": [
                    "Action",
                    "Comedy"
                ],
                "rating": "R",
                "duration": "2h 4m",
                "year": "2020",
                "actors": [
                    "Will Smith",
                    "Martin Lawrence",
                    "Vanessa Hudgens",
                    "Jacob Scipio",
                    "Alexander Ludwig"
                ],
                "directors": [
                    "Adil El Arbi",
                    "Bilall Fallah"
                ]
            }
        }


app = FastAPI(
    title = "Rotten Tomatoes Scraper API",
    description = "Unofficial API getting data by scraping the Rotten Tomatoes website.",
    version = "0.5.11"
)


class Movies(BaseModel):
    movies: list[MovieAttributes] = Field(..., title="A list of movies with attributes.")

    class Config:
        schema_extra = {
            "example": {
                "movies": [
                    {
                    "name": "Bad Boys for Life",
                    "tomatometer": 76,
                    "audience_score": 96,
                    "weighted_score": 82,
                    "genres": [
                        "Action",
                        "Comedy"
                    ],
                    "rating": "R",
                    "duration": "2h 4m",
                    "year": "2020",
                    "actors": [
                        "Will Smith",
                        "Martin Lawrence",
                        "Vanessa Hudgens",
                        "Jacob Scipio",
                        "Alexander Ludwig"
                    ],
                    "directors": [
                        "Adil El Arbi",
                        "Bilall Fallah"
                    ]
                    },
                    {
                    "name": "Bad Boys II",
                    "tomatometer": 23,
                    "audience_score": 78,
                    "weighted_score": 41,
                    "genres": [
                        "Action",
                        "Comedy"
                    ],
                    "rating": "R",
                    "duration": "2h 26m",
                    "year": "2003",
                    "actors": [
                        "Martin Lawrence",
                        "Will Smith",
                        "Jordi Mollà",
                        "Gabrielle Union",
                        "Peter Stormare"
                    ],
                    "directors": [
                        "Michael Bay"
                    ]
                    },
                    {
                    "name": "Bad Boys",
                    "tomatometer": 43,
                    "audience_score": 78,
                    "weighted_score": 54,
                    "genres": [
                        "Action",
                        "Comedy"
                    ],
                    "rating": "R",
                    "duration": "1h 58m",
                    "year": "1995",
                    "actors": [
                        "Martin Lawrence",
                        "Will Smith",
                        "Téa Leoni",
                        "Tchéky Karyo",
                        "Theresa Randle"
                    ],
                    "directors": [
                        "Michael Bay"
                    ]
                    },
                    {
                    "name": "Bad Boys",
                    "tomatometer": 90,
                    "audience_score": 82,
                    "weighted_score": 87,
                    "genres": [
                        "Drama"
                    ],
                    "rating": "R",
                    "duration": "2h 3m",
                    "year": "1983",
                    "actors": [
                        "Sean Penn",
                        "Reni Santoni",
                        "Esai Morales",
                        "Jim Moody",
                        "Ally Sheedy"
                    ],
                    "directors": [
                        "Rick Rosenthal 2"
                    ]
                    }
                ]
            }
        }


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


@app.get("/", tags=["Tests"])
async def test_homepage() -> str:
    """Check if the API is live."""
    return "API is live. See /docs or /redoc for endpoints and usage instructions."


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
