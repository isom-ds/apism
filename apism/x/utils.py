import aiohttp
import asyncio
import copy

async def _fetch_with_retries(bearer_token, url, params, retry_limit=3, retry_delay=1, session=aiohttp.ClientSession(), verbose=False):
    """
    Fetch data from a URL with retries and handle errors related to disabled comments.
    
    Args:
        bearer_token (str): The bearer token used for authentication.
        url (str): The URL to fetch data from.
        params (dict): Parameters to include in the request.
        retry_limit (int): The number of retries to attempt.
        retry_delay (int): The delay between retries in seconds.
        session (aiohttp.ClientSession): The session used to make HTTP requests.
        verbose (bool): Print verbose output. Default=False
        
    Returns:
        tuple: A tuple containing the response data and the nextPageToken if available.
    
    Raises:
        Exception: If retries are exhausted and the request still fails.
    """
    headers = {"Authorization": f"Bearer {bearer_token}"}
    __params__ = copy.deepcopy(params)
    attempt = 0

    while attempt < retry_limit:
        try:
            async with session.get(url, headers=headers, params=__params__) as response:
                response_data = await response.json()
                
                # Handle API limit errors and other issues
                if response.status == 200:
                    next_page_token = response_data.get('next_token')
                    return response_data, next_page_token
                else:
                    if verbose:
                        print(f"Received error response: {response_data}")
                    response.raise_for_status()
        
        except (aiohttp.ClientError, asyncio.TimeoutError) as e:
            attempt += 1
            if verbose:
                print(f"Attempt {attempt} failed: {e}. Retrying in {retry_delay} seconds...")
            await asyncio.sleep(retry_delay)
    
    # If all retries fail, raise an exception
    raise Exception(f"Failed to fetch data from {url} after {attempt} attempts.")