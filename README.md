# Rotten Tomatoes in Python

This package is for easily getting Rotten Tomatoes scores and other data on movies, without the use of their API. The package scrapes their website for the data. Unfortunately, to get access to their API you have to submit a special request which takes an inordinate amount of time to process, or doesn't go through at all. 

You can either call the standalone functions `tomatometer`, `audience_score`, `genres`, etc., or use the `Movie` class to only pass the name and have each attribute be fetched automatically. If you use the `Movie` class, you can print all attributes by printing the object itself, or by accessing each attribute individually. 

The weighted score is calculated using the formula $\frac{2}{3}(tomatometer) + \frac{1}{3}(audience_{score})$. The result is then rounded to the nearest integer.

Basic usage:

```python
import rottentomatoes_python as rt

print(rt.tomatometer("happy gilmore"))
# Output: 61

print(rt.audience_score('top gun maverick'))
# Output: 99

print(rt.weighted_score('happy gilmore'))
# Output: 69

# --- Using the Movie class ---
movie = rt.Movie('top gun')
print(movie)
# Output: Top Gun. Tomatometer: 58. Audience Score: 83. Genres - ['Action', 'Adventure']. Weighted score: 66.

print(movie.weighted_score)
# Output: 66
```
