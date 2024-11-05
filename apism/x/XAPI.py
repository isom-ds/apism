from .search_tweets import search_tweets
import asyncio
import aiohttp
from copy import deepcopy

class xAPI:
    """
    A class to interact with the YouTube Data API.
    Args:
        token (str): The token to access Twitter / X API.
        params (dict): A dictionary containing parameters.
        retry_limit (int): The number of retries to attempt. Default=3
        retry_delay (int): The delay between retries in seconds. Default=1
        session (aiohttp.ClientSession): The session used to make HTTP requests.
        verbose (bool): Print verbose output. Default=False
        async_delay(float/int): Delay in seconds between starting each task.
        sequential (bool): Concurrent (False) or sequential (True) API calls. Default=False
    """
    def __init__(self, token, params, **kwargs):
        # Required
        self.token = token
        self.params = deepcopy(params)

        # Kwargs
        self.retry_limit = kwargs.get('retry_limit', 3)
        self.retry_delay = kwargs.get('retry_delay', 1)
        self.verbose = kwargs.get('verbose', False)
        self.async_delay = kwargs.get('async_delay', 0)
        self.sequential = kwargs.get('sequential', False)

        # Dictionary to store output
        self.results = {}

    # ==============================================
    # Method to search for tweets
    # ==============================================
    async def search_tweets(self, type, session=aiohttp.ClientSession()):
        """
        Search for tweets based on a query.
        Args:
            type (str): The type of search results to return. Options are 'recent' or 'all'.
            params (dict): A dictionary containing search parameters.
            session (aiohttp.ClientSession): The session used to make HTTP requests.
        Returns:
            list: A list of search results.
        """
        # Assert if search parameters are present
        assert 'search_tweets' in self.params.keys(), "Search parameters not found in params."

        # Assert if type is either 'recent' or 'all'
        assert type in ['recent', 'all'], "Type must be either 'recent' or 'all'"

        # Search parameters
        search_params = deepcopy(self.params['search_tweets'])

        # Call search API
        self.results['search_tweets'] = await search_tweets(
            self.token, 
            type,
            search_params,
            self.retry_limit,
            self.retry_delay,
            session,
            self.verbose
        )

        if self.verbose:
            if 'data' in self.results['search_tweets'].keys():
                l_tweet_ids = [i['id'] for i in self.results['search_tweets']['data']]
            else:
                l_tweet_ids = [i['id'] for i in self.results['search_tweets']]
            print(f"{len(l_tweet_ids)} tweets found")