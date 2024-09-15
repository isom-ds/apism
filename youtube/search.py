from youtube.utils import _fetch_with_retries
import aiohttp
import copy

async def fetch_search_results(query, params, retry_limit=3, retry_delay=1, session=aiohttp.ClientSession()):
    """
    Fetch search results for a single query with pagination support (sequential fetching).
    Args:
        query (str): Search query
        params (dict): Search parameters, such as published date range, and other search filters.
        retry_limit (int): The number of retries to attempt. Default=3
        retry_delay (int): The delay between retries in seconds. Default=1
        session (aiohttp.ClientSession): The session used to make HTTP requests.

    Returns:
        list: All video search results for the given query.
    """
    url = 'https://www.googleapis.com/youtube/v3/search'
    __params__ = copy.deepcopy(params)
    __params__['q'] = query

    all_results = []
    next_page_token = None

    # Sequentially fetch paginated results
    while True:
        if next_page_token:
            __params__['pageToken'] = next_page_token

        data, next_page_token = await _fetch_with_retries(url, __params__, retry_limit, retry_delay, session)

        if data and 'items' in data:
            all_results.extend(data['items'])

        # Break the loop when no more pages are available
        if not next_page_token:
            break

    return all_results

