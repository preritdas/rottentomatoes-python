# Rotten Tomatoes Python

This package is for easily getting Rotten Tomatoes scores and other data on movies, without the use of their API. The package scrapes their website for the data. Unfortunately, to get access to their API you have to submit a special request which takes an inordinate amount of time to process, or doesn't go through at all. 

Basic usage:

```python
import rottentomatoes_python as rt
print(rt.tomatometer("happy gilmore"))

# Result: 61 (of type int)
```
