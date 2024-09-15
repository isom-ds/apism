from youtube.utils import _fetch_with_retries
from youtube.search import fetch_search_results
from youtube.videos import fetch_videos
from youtube.comment_threads import fetch_comment_threads
import asyncio
import aiohttp
import copy

async def search_videos_comments(query, search_params, video_params, comment_params, min_comments=0, async_delay=0, retry_limit=3, retry_delay=1, sequential=False, session=aiohttp.ClientSession()):
    """
    Pipeline to fetch search results, video data, and comments for all videos for the query.
    Args:
        query (str): Search query
        search_params (dict): Search parameters, such as published date range, and other search filters.
        video_params (dict): Video parameters such as id, part, maxResults, etc.
        comment_params (dict): Video parameters such as id, part, maxResults, etc.
        min_comments (int): Minimum number of comments per video.
        async_delay(float/int): Delay in seconds between starting each task.
        retry_limit (int): The number of retries to attempt. Default=3
        retry_delay (int): The delay between retries in seconds. Default=1
        squential (bool): Concurrent (False) or sequential (True) API calls. Default=False

    Returns:
        dict: A dictionary mapping video IDs to their respective search result, video data, and comments.
    """

    # Fetch Search Results
    search_results = await fetch_search_results(query, search_params, retry_limit, retry_delay, session)
    l_video_ids = list(set([i['id']['videoId'] for i in search_results]))
    print(f"{len(l_video_ids)} videos found")

    # Fetch video data
    video_results = await fetch_videos(l_video_ids, video_params, async_delay, retry_limit, retry_delay, sequential, session)
    # Remove videos with less than n comments
    l_video_ids_filtered = [v['id'] for k,v in video_results.items() if v['statistics']['commentCount'] >= min_comments]
    print(f"{len(l_video_ids_filtered)} videos with {min_comments}+ comments")

    # Fetch comments
    comments_results = await fetch_comment_threads(l_video_ids_filtered, comment_params, async_delay, retry_limit, retry_delay, sequential, session)

    # Consolidate outputs
    output_dict = {}
    for i, v in enumerate(l_video_ids_filtered):
        # Add search results
        output_dict[v] = {'search': search_results[i]}
        # Add video data
        output_dict[v]['video'] = video_results[v]
        # Add comments data
        if v not in comments_results.keys():
            output_dict[v]['commentThreads'] = None
        else:
            output_dict[v]['commentThreads'] = comments_results[v]

    return output_dict
