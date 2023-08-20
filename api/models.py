"""Models for the API."""
from pydantic import ConfigDict, BaseModel, Field


class MovieQuery(BaseModel):
    """Job request, querying for a movie."""
    name: str = Field(..., title="Name of the movie you're searching for.")

    # Model configuration
    model_config = ConfigDict(json_schema_extra={"example": {"name": "top gun"}})


class MovieAttributes(BaseModel):
    """Output, movie attributes."""
    name: str = Field(..., title="Name of the movie according to its page.")
    tomatometer: int = Field(..., title="Rotten Tomatoes Tomatometer.")
    audience_score: int = Field(..., title="Rotten Tomatoes audience score.")
    weighted_score: int = Field(
        ...,
        title="Internally formulated weighted score between tomatometer and audience score.",
    )
    genres: list[str] = Field(..., title="List of genres.")
    rating: str = Field(..., title="Movie viewership rating, ex. PG.")
    duration: str = Field(..., title="String represented time, ex. 2h 11m.")
    year: str = Field(..., title="String represented year, ex. 1995.")
    actors: list[str] = Field(..., title="List of featured prominent actors.")
    directors: list[str] = Field(..., title="List of directors.")

    # Model configuration
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "name": "Bad Boys for Life",
            "tomatometer": 76,
            "audience_score": 96,
            "weighted_score": 82,
            "genres": ["Action", "Comedy"],
            "rating": "R",
            "duration": "2h 4m",
            "year": "2020",
            "actors": [
                "Will Smith",
                "Martin Lawrence",
                "Vanessa Hudgens",
                "Jacob Scipio",
                "Alexander Ludwig",
            ],
            "directors": ["Adil El Arbi", "Bilall Fallah"],
        }
    })


class Movies(BaseModel):
    movies: list[MovieAttributes] = Field(
        ..., title="A list of movies with attributes."
    )

    # Model configuration
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "movies": [
                {
                    "name": "Bad Boys for Life",
                    "tomatometer": 76,
                    "audience_score": 96,
                    "weighted_score": 82,
                    "genres": ["Action", "Comedy"],
                    "rating": "R",
                    "duration": "2h 4m",
                    "year": "2020",
                    "actors": [
                        "Will Smith",
                        "Martin Lawrence",
                        "Vanessa Hudgens",
                        "Jacob Scipio",
                        "Alexander Ludwig",
                    ],
                    "directors": ["Adil El Arbi", "Bilall Fallah"],
                },
                {
                    "name": "Bad Boys II",
                    "tomatometer": 23,
                    "audience_score": 78,
                    "weighted_score": 41,
                    "genres": ["Action", "Comedy"],
                    "rating": "R",
                    "duration": "2h 26m",
                    "year": "2003",
                    "actors": [
                        "Martin Lawrence",
                        "Will Smith",
                        "Jordi Mollà",
                        "Gabrielle Union",
                        "Peter Stormare",
                    ],
                    "directors": ["Michael Bay"],
                },
                {
                    "name": "Bad Boys",
                    "tomatometer": 43,
                    "audience_score": 78,
                    "weighted_score": 54,
                    "genres": ["Action", "Comedy"],
                    "rating": "R",
                    "duration": "1h 58m",
                    "year": "1995",
                    "actors": [
                        "Martin Lawrence",
                        "Will Smith",
                        "Téa Leoni",
                        "Tchéky Karyo",
                        "Theresa Randle",
                    ],
                    "directors": ["Michael Bay"],
                },
                {
                    "name": "Bad Boys",
                    "tomatometer": 90,
                    "audience_score": 82,
                    "weighted_score": 87,
                    "genres": ["Drama"],
                    "rating": "R",
                    "duration": "2h 3m",
                    "year": "1983",
                    "actors": [
                        "Sean Penn",
                        "Reni Santoni",
                        "Esai Morales",
                        "Jim Moody",
                        "Ally Sheedy",
                    ],
                    "directors": ["Rick Rosenthal 2"],
                },
            ]
        }
    })
