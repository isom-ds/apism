from functions.utils import fetch_with_retries
from functions.search import fetch_search_results
import asyncio
import aiohttp

async def fetch_comment_thread(session, video_id, params, retry_limit=3, retry_delay=1):
    """
    Fetch the comment thread for a video.
    Args:
        session (aiohttp.ClientSession): The session used to make HTTP requests.
        video_id (str): Video ID to fetch comments for.
        params (dict): Parameters such as videoId, part, maxResults, etc.
        retry_limit (int): The number of retries to attempt. Default=3
        retry_delay (int): The delay between retries in seconds. Default=1

    Returns:
        list: All comments for the given video.
    """
    url = 'https://www.googleapis.com/youtube/v3/commentThreads'
    params['videoId'] = video_id  # Ensure videoId is included in the parameters

    all_comments = []
    next_page_token = None

    while True:
        if next_page_token:
            params['pageToken'] = next_page_token

        data, next_page_token = await fetch_with_retries(session, url, params, retry_limit, retry_delay)

        if data and 'items' in data:
            all_comments.extend(data['items'])

        if not next_page_token:
            break

    return all_comments