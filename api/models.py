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
    synopsis: str = Field(..., title="Synopsis of the movie.")
    tomatometer: int | None = Field(..., title="Rotten Tomatoes Tomatometer.")
    num_of_reviews: int | None = Field(..., title="Number of critic reviews")
    audience_score: int | None = Field(..., title="Rotten Tomatoes audience score.")
    weighted_score: int | None = Field(
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
            "synopsis": (
                "The wife and son of a Mexican drug lord embark on a vengeful quest to kill all those involved "
                "in his trial and imprisonment -- including Miami Detective Mike Lowrey. When Mike gets "
                "wounded, he teams up with partner Marcus Burnett and AMMO -- a special tactical squad -- to "
                "bring the culprits to justice. But the old-school, wisecracking cops must soon learn to get "
                "along with their new elite counterparts if they are to take down the vicious cartel that "
                "threatens their lives."
            ),
            "tomatometer": 76,
            "num_of_reviews": 270,
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
                    "synopsis": "The wife and son of a Mexican drug lord embark on a vengeful quest to kill all those "
                                "involved in his trial and imprisonment -- including Miami Detective Mike Lowrey. "
                                "When Mike gets wounded, he teams up with partner Marcus Burnett and AMMO -- a "
                                "special tactical squad -- to bring the culprits to justice. But the old-school, "
                                "wisecracking cops must soon learn to get along with their new elite counterparts if "
                                "they are to take down the vicious cartel that threatens their lives.",
                    "tomatometer": 76,
                    "num_of_reviews": 270,
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
                    "synopsis": "The drug ecstasy is flowing into Miami, and the police want it stopped. Police "
                                "Detective Marcus Burnett (Martin Lawrence) and his partner, Mike Lowrey (Will "
                                "Smith), are just the men to do it. They track the drugs to a Cuban smuggler, "
                                "Johnny Tapia (Jordi Mollà), who is also involved in a bloody war with Russian and "
                                "Haitian mobsters. If that isn't bad enough, there's tension between the two cops "
                                "because Lowrey is romantically involved with Burnett's sister, Syd (Gabrielle Union).",
                    "num_of_reviews": 186,
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
                    "synopsis": "Miami-Dade detectives Mike Lowrey (Will Smith) and Marcus Burnett (Martin Lawrence) "
                                "blow a fuse when $100 million worth of heroin they recently confiscated is heisted "
                                "from station headquarters. Suspecting it was an inside job, Internal Affairs gives "
                                "them five days to track down the drugs before they shut down the narcotics division. "
                                "Action meets farce when Marcus is compelled to masquerade as his partner in order to "
                                "gain the trust of a call girl (Tea Leoni), a key witness in their investigation.",
                    "tomatometer": 43,
                    "num_of_reviews": 69,
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
                    "synopsis": "Teen delinquent Mick O'Brien (Sean Penn) is sent to juvenile hall after "
                                "unintentionally killing the younger sibling of a rival gang leader, Paco Moreno ("
                                "Esai Morales), in a drug-deal con gone wrong. Prison life proves even more brutal "
                                "than the streets when Mick is forced to face off against reigning prison toughs "
                                "Viking (Clancy Brown) and Tweety (Robert Lee Rush). Worse yet, on the outside, "
                                "Paco is threatening to take revenge on those close to Mick -- including his "
                                "girlfriend (Ally Sheedy).",
                    "tomatometer": 90,
                    "num_of_reviews": 20,
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
