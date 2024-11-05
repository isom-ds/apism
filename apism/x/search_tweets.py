from .tweets import _tweets

import aiohttp
from copy import deepcopy

def search_tweets(bearer_token, type, params, retry_limit=3, retry_delay=1, session=aiohttp.ClientSession(), verbose=False):
    """
    Search for tweets using the Twitter API.
    Args:
        bearer_token (str): The bearer token used for authentication.
        query (str): The search query string.
        start_time (str): The start time for the search query (ISO 8601 format).
        end_time (str): The end time for the search query (ISO 8601 format).
        max_results (int): The maximum number of results to return. Default=10
        type (str): The type of search results to return. Options are 'recent' or 'all'. Default='recent'
        verbose (bool): Print verbose output. Default=False
    Returns:
        list: A list of tweet objects matching the search query.
    """
    # Check if type is either 'recent' or 'all'
    if type not in ['recent', 'all']:
        raise ValueError("Type must be either 'recent' or 'all'")

    # Set the URL based on the search type
    url = f"https://api.twitter.com/2/tweets/search/{type}"

    # Set the query parameters
    __params__ = deepcopy(params)

    # Use the _tweets function to fetch search results
    return _tweets(bearer_token, url, __params__, retry_limit, retry_delay, session, verbose)

