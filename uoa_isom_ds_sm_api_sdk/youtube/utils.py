import aiohttp
import asyncio
import copy

class YouTubeAPIException(Exception):
    """Custom exception for YouTube API errors"""
    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message
        super().__init__(f"API Error {status_code}: {message}")

async def _fetch_with_retries(url, params, retry_limit=3, retry_delay=1, session=aiohttp.ClientSession()):
    """
    Fetch data from a URL with retries and handle errors related to disabled comments.
    
    Args:
        url (str): The URL to fetch data from.
        params (dict): Parameters to include in the request.
        retry_limit (int): The number of retries to attempt.
        retry_delay (int): The delay between retries in seconds.
        session (aiohttp.ClientSession): The session used to make HTTP requests.
        
    Returns:
        tuple: A tuple containing the response data and the nextPageToken if available.
    
    Raises:
        Exception: If retries are exhausted and the request still fails.
    """
    __params__ = copy.deepcopy(params)
    attempt = 0

    while attempt < retry_limit:
        try:
            async with session.get(url, params=__params__) as response:
                # Handle quota exceeded case
                if response.status == 403 and response.reason == 'Quota exceeded':
                    print(f"API quota exceeded")
                    return None, None

                response_data = await response.json()
                
                # Handle comments disabled case
                if response.status == 403 and 'disabled comments' in response_data['error'].get('message'):
                    print_params = {k:v for k,v in __params__.items() if k != 'key'}
                    print(f"Comments are disabled for video with params: {print_params}")
                    return None, None
                
                # Handle API limit errors and other issues
                if response.status == 200:
                    next_page_token = response_data.get('nextPageToken')
                    return response_data, next_page_token
                else:
                    print(f"Received error response: {response_data}")
                    response.raise_for_status()
        
        except (aiohttp.ClientError, asyncio.TimeoutError) as e:
            attempt += 1
            print(f"Attempt {attempt} failed: {e}. Retrying in {retry_delay} seconds...")
            await asyncio.sleep(retry_delay)
    
    # If all retries fail, raise an exception
    raise Exception(f"Failed to fetch data from {url} after {attempt} attempts.")
