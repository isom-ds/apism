from youtube.utils import _fetch_with_retries
import asyncio
import aiohttp
import copy

async def _fetch_comment_thread(video_id, params, retry_limit=3, retry_delay=1, session=aiohttp.ClientSession()):
    """
    Fetch the comment thread for a video.
    Args:
        video_id (str): Video ID to fetch comments for.
        params (dict): Parameters such as videoId, part, maxResults, etc.
        retry_limit (int): The number of retries to attempt. Default=3
        retry_delay (int): The delay between retries in seconds. Default=1
        session (aiohttp.ClientSession): The session used to make HTTP requests.

    Returns:
        list: All comments for the given video.
    """
    url = 'https://www.googleapis.com/youtube/v3/commentThreads'
    __params__ = copy.deepcopy(params)
    __params__['videoId'] = video_id  # Ensure videoId is included in the parameters

    all_comments = []
    next_page_token = None

    while True:
        if next_page_token:
            __params__['pageToken'] = next_page_token

        try:
            data, next_page_token = await _fetch_with_retries(url, __params__, retry_limit, retry_delay, session)

            if data and 'items' in data:
                all_comments.extend(data['items'])

            if not next_page_token:
                break
        
        except Exception as e:
            print(f"Error fetching comments for video {video_id}: {e}")
            break

    return all_comments

async def comment_threads(video_id, params, async_delay=0, retry_limit=3, retry_delay=1, sequential=False, session=aiohttp.ClientSession()):
    """
    Fetch comment threads for multiple video IDs concurrently, but staggered using asyncio.gather.
    Each video fetches comments independently, handling its own pagination with separate nextPageTokens.
    
    Args:
        video_ids (str/list): A single video ID or list of video IDs to fetch comments for.
        params (dict): Parameters such as videoId, part, maxResults, etc.
        async_delay(float/int): Delay in seconds between starting each task.
        retry_limit (int): The number of retries to attempt. Default=3
        retry_delay (int): The delay between retries in seconds. Default=1
        squential (bool): Concurrent (False) or sequential (True) API calls. Default=False
        session (aiohttp.ClientSession): The session used to make HTTP requests.

    Returns:
        dict: A dictionary mapping video IDs to their respective comments.
    """
    __params__ = copy.deepcopy(params)

    if type(video_id) == str:
        return await _fetch_comment_thread(video_id, __params__, retry_limit, retry_delay, session)
    
    elif type(video_id) == list:
        if sequential:
            return {
                i: await _fetch_comment_thread(i, __params__, retry_limit, retry_delay, session) 
                    for i in video_id
                }
        else:
            async with aiohttp.ClientSession() as session:
                tasks = []
                
                for __, id in enumerate(video_id):
                    # Create a separate task for each video with independent pagination
                    tasks.append(_fetch_comment_thread(id, __params__, retry_limit, retry_delay, session))
                    
                    # Introduce a delay before starting the next task
                    await asyncio.sleep(async_delay)
                
                # Gather the results of all tasks concurrently
                results = await asyncio.gather(*tasks)
                
                # Return a dictionary mapping video IDs to their comments
                return {id: result for id, result in zip(video_id, results)}

    else:
        print(f"Error fetching comments for video {video_id}")
