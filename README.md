# Rotten Tomatoes in Python

This package allows you to easily fetch Rotten Tomatoes scores and other movie data such as genres, without the use of the official Rotten Tomatoes API. The package scrapes their website for the data. I built this because unfortunately, to get access to their API, you have to submit a special request which takes an inordinate amount of time to process, or doesn't go through at all. 

## Usage

You can either call the standalone functions `tomatometer`, `audience_score`, `genres`, etc., or use the `Movie` class to only pass the name and have each attribute be fetched automatically. If you use the `Movie` class, you can print all attributes by printing the object itself, or by accessing each attribute individually. 

The weighted score is calculated using the formula $\frac{2}{3}(tomatometer) + \frac{1}{3}(audience)$. The result is then rounded to the nearest integer.

Basic usage examples:

```python
import rottentomatoes_python as rt

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

# --- Using the Movie class ---
movie = rt.Movie('top gun')
print(movie)
# Output
    # Top Gun, PG.
    # Tomatometer: 58
    # Weighted score: 66
    # Audience Score: 83
    # Genres - ['Action', 'Adventure']
# Type: str

print(movie.weighted_score)
# Output: 66
# Type: int
```

## Exceptions

If you're using this package within a larger program, it's useful to know what exceptions are raised (and when) so they can be caught and handled.

### `LookupError`

When _any_ call is made to scrape the Rotten Tomatoes website (Tomatometer, Audience Score, Genres, etc.), if a proper movie page wasn't returned (can be due to a typo in name entry, duplicate movie names, etc.), a `LookupError` is raised, printing the attempted query url.
