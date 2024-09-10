from functions.utils import fetch_with_retries

async def fetch_search_results(session, query, params, retry_limit=3, retry_delay=1):
    """
    Fetch search results for a single query with pagination support (sequential fetching).
    Args:
        session (aiohttp.ClientSession): The session used to make HTTP requests.
        params (dict): Search parameters, such as the query, published date range, and other search filters.

    Returns:
        list: All video search results for the given query.
    """
    url = 'https://www.googleapis.com/youtube/v3/search'
    params['q'] = query

    all_results = []
    next_page_token = None

    # Sequentially fetch paginated results
    while True:
        if next_page_token:
            params['pageToken'] = next_page_token

        data, next_page_token = await fetch_with_retries(session, url, params, retry_limit, retry_delay)

        if data and 'items' in data:
            all_results.extend(data['items'])

        # Break the loop when no more pages are available
        if not next_page_token:
            break

    return all_results

