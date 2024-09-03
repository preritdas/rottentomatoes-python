from bs4 import BeautifulSoup

from api import build_movie
from rottentomatoes import movie, search
import requests
import json


def get_content(url):
    response = requests.get(url)
    return response.text


def _extract(content: str, start_string: str, end_string: str) -> str:
    """Retrieves parts of the RT website data given a start string
    and an end string.

    Args:
        content (str): The raw RT data for a movie.
        start_string (str): The start of the data to be extracted.
        end_string (str): The end of the data to be extracted.

    Returns:
        string: A part of the raw RT data, from the start string to the
                end string.
    """
    start_idx = content.find(start_string)

    if start_idx == -1:
        return None

    end_idx = content.find(end_string, start_idx)
    return content[start_idx + len(start_string):end_idx]


#
# c = get_content('https://www.rottentomatoes.com/m/')
# soup = BeautifulSoup(c, 'html.parser')
# print(soup.prettify())


m = movie.Movie("american psycho")
print(m)

# soup = BeautifulSoup(c, 'html.parser')
#
# # tomatometer_score = int(soup.find('rt-button', {'slot': 'criticsScore'}).text.strip("%\n"))
# # audience_score = int(soup.find('rt-button', {'slot': 'audienceScore'}).text.strip("%\n"))
# # rating = soup.find('rt-text', {'slot': 'ratingsCode'}).text
# # release_date = soup.find('rt-text', {'slot': 'releaseDate'}).text.strip("Released ")
# # duration = soup.find('rt-text', {'slot': 'duration'}).text
#
# num_of_reviews_tomatometer = soup.find('rt-link', {'slot': 'criticsReviews'}).text.strip().split(' ')[0]
#
# print(num_of_reviews_tomatometer)


results = search.filter_searches(results=search.search_results("grown ups"))


def idk(r):
    return {
        "movies": [
            build_movie(force_url=result.url) for result in r
        ]
    }


print(idk(results))
