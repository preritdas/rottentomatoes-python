![tests](https://github.com/preritdas/rottentomatoes-python/actions/workflows/pytest.yml/badge.svg)
![pypi](https://github.com/preritdas/rottentomatoes-python/actions/workflows/python-publish.yml/badge.svg)
[![PyPI version](https://badge.fury.io/py/rottentomatoes-python.svg)](https://badge.fury.io/py/rottentomatoes-python)
![PyPI - Downloads](https://img.shields.io/pypi/dm/rottentomatoes-python)
![versions](https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10%20%7C%203.11-blue)


# :movie_camera: Rotten Tomatoes in Python (and API) :clapper:

> **Note**
> If at any point in your project this library stops working, returning errors for standalone functions or the `Movie` class, first try updating it with `pip install -U rottentomatoes-python`, and if it's still not working, submit an issue on this repo. 99% of the time it'll "stop working" because the Rotten Tomatoes site schema has changed, meaning some changes to web scraping and extraction under the hood are necessary to make everything work again. Tests run on this repo automatically once a day, so breaking changes to the Rotten Tomatoes site should be caught by myself or a maintainer pretty quickly.

This package allows you to easily fetch Rotten Tomatoes scores and other movie data such as genres, without the use of the official Rotten Tomatoes API. The package scrapes their website for the data. I built this because unfortunately, to get access to their API, you have to submit a special request which takes an inordinate amount of time to process, or doesn't go through at all. 

The package now, by default, scrapes the Rotten Tomatoes search page to find the true url of the first valid movie response (is a movie and has a tomatometer). This means queries that previously didn't work because their urls had a unique identifier or a year-released prefix, now work. The limitation of this new mechanism is that you only get the top response, and when searching for specific movies (sequels, by year, etc.) Rotten Tomatoes seems to return the same results as the original query. So, it's difficult to use specific queries to try and get the desired result movie as the top response. See #4 for more info on this.

There is now an API deployed to make querying multiple movies and getting several responses easier. The endpoint is https://rotten-tomatoes-api.ue.r.appspot.com and it's open and free to use. Visit `/docs` or `/redoc` in the browser to view the endpoints. Both endpoints live right now are browser accessible meaning you don't need an HTTP client to use the API. 

- https://rotten-tomatoes-api.ue.r.appspot.com/movie/bad_boys for JSON response of the top result
- https://rotten-tomatoes-api.ue.r.appspot.com/search/bad_boys for a JSON response of all valid results


## Usage

You can either call the standalone functions `tomatometer`, `audience_score`, `genres`, etc., or use the `Movie` class to only pass the name and have each attribute be fetched automatically. If you use the `Movie` class, you can print all attributes by printing the object itself, or by accessing each attribute individually. 

The weighted score is calculated using the formula $\frac{2}{3}(tomatometer) + \frac{1}{3}(audience)$. The result is then rounded to the nearest integer.

Basic usage examples:

```python
import rottentomatoes as rt

print(rt.tomatometer("happy gilmore"))
# Output: 61
# Type: int

print(rt.audience_score('top gun maverick'))
# Output: 99
# Type: int

print(rt.rating('everything everywhere all at once'))
# Output: R
# Type: str

print(rt.genres('top gun'))
# Output: ['Action', 'Adventure']
# Type: list[str]

print(rt.weighted_score('happy gilmore'))
# Output: 69
# Type: int

print(rt.year_released('happy gilmore'))
# Output: 1996
# Type: str

print(rt.actors('top gun maverick', max_actors=5))
# Output: ['Tom Cruise', 'Miles Teller', 'Jennifer Connelly', 'Jon Hamm', 'Glen Powell']
# Type: list[str]

# --- Using the Movie class ---
movie = rt.Movie('top gun')
print(movie)
# Output
    # Top Gun, PG, 1h 49m.
    # Released in 1986.
    # Tomatometer: 58
    # Weighted score: 66
    # Audience Score: 83
    # Genres - ['Action', 'Adventure']
    # Prominent actors: Tom Cruise, Kelly McGillis, Anthony Edwards, Val Kilmer, Tom Skerritt.
# Type: str

print(movie.weighted_score)
# Output: 66
# Type: int
```

## Exceptions

If you're using this package within a larger program, it's useful to know what exceptions are raised (and when) so they can be caught and handled.

### `LookupError`

When _any_ call is made to scrape the Rotten Tomatoes website (Tomatometer, Audience Score, Genres, etc.), if a proper movie page wasn't returned (can be due to a typo in name entry, duplicate movie names, etc.), a `LookupError` is raised, printing the attempted query url.


## Performance

`v0.3.0` makes the `Movie` class 19x more efficient. Data attained from scraping Rotten Tomatoes is temporarily cached and used to parse various other attributes. To test the performance difference, I used two separate virtual environments, `old` and `venv`. `rottentomatoes-python==0.2.5` was installed on `old`, and `rottentomatoes-python==0.3.0` was installed on `venv`. I then ran the same script, shown below, using each environment (Python 3.10.4). 

```python
import rottentomatoes as rt
from time import perf_counter


def test() -> None:
    start = perf_counter()
    movie = rt.Movie('top gun maverick')
    print('\n', movie, sep='')
    print(f"That took {perf_counter() - start} seconds.")


if __name__ == "__main__":
    test()
```

The results:

```console
❯ deactivate && source old/bin/activate && python test.py

Top Gun Maverick, PG-13, 2h 11m.
Released in 2022.
Tomatometer: 97
Weighted score: 97
Audience Score: 99
Genres - ['Action', 'Adventure']

That took 6.506246249999094 seconds.
❯ deactivate && source venv/bin/activate && python test.py

Top Gun Maverick, PG-13, 2h 11m.
Released in 2022.
Tomatometer: 97
Weighted score: 97
Audience Score: 99
Genres - ['Action', 'Adventure']
Prominent actors: Tom Cruise, Miles Teller, Jennifer Connelly, Jon Hamm, Glen Powell.

That took 0.3400420409961953 seconds.
```

## API

The API is deployed at https://rotten-tomatoes-api.ue.r.appspot.com/. It has two endpoints currently, `/movie/{movie_name}` and `/search/{movie_name}`. The first will pull one movie, the top result. The second will pull a list of _all_ valid movie results.

The first, with `movie_name="bad boys"`:

```json
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
}
```

The second, with `movie_name="bad boys"`:

```json
{
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
```
