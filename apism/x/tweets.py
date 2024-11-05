from .utils import _fetch_with_retries

import aiohttp
from copy import deepcopy

async def _tweets(bearer_token, url, params, retry_limit=3, retry_delay=1, session=aiohttp.ClientSession(), verbose=False):
    """
    Fetch search results using the Tweets endpoint with pagination support (sequential fetching).
    Args:
        bearer_token (str): The bearer token used for authentication.
        params (dict): Query, and search parameters, such as published date range, and other search filters.
        retry_limit (int): The number of retries to attempt. Default=3
        retry_delay (int): The delay between retries in seconds. Default=1
        session (aiohttp.ClientSession): The session used to make HTTP requests.
        verbose (bool): Print verbose output. Default=False

    Returns:
        list: All tweet results for the given query.
    """
    __params__ = deepcopy(params)

    all_results = []
    next_token = None

    # Sequentially fetch paginated results
    while True:
        if next_token:
            __params__['next_token'] = next_token

        data, next_token = await _fetch_with_retries(bearer_token, url, params, retry_limit, retry_delay, session, verbose)

        if data and 'data' in data:
            all_results.extend(data['data'])

        # Break the loop when no more pages are available
        if not next_token:
            break

    return all_results