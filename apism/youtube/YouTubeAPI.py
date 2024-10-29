from .search import search
from .videos import videos
from .comment_threads import comment_threads
from .transcript import transcript
from .save_as import to_json, to_csv
from .defaults import _default_params
import asyncio
import aiohttp
from copy import deepcopy

class YouTubeAPI:
    """
    A class to interact with the YouTube Data API.
    Args:
        api_key (str): The API key to access the YouTube Data API.
        params (dict): A dictionary containing parameters for search, video, and commentThreads.
        retry_limit (int): The number of retries to attempt. Default=3
        retry_delay (int): The delay between retries in seconds. Default=1
        min_comments (int): Minimum number of comments per video.
        session (aiohttp.ClientSession): The session used to make HTTP requests.
        verbose (bool): Print verbose output. Default=False
        async_delay(float/int): Delay in seconds between starting each task.
        sequential (bool): Concurrent (False) or sequential (True) API calls. Default=False
    """
    def __init__(self, api_key, params=_default_params, **kwargs):
        # Required
        self.api_key = api_key
        self.params = deepcopy(params)

        # Kwargs
        self.retry_limit = kwargs.get('retry_limit', 3)
        self.retry_delay = kwargs.get('retry_delay', 1)
        self.min_comments = kwargs.get('min_comments', 0)
        self.verbose = kwargs.get('verbose', False)
        self.async_delay = kwargs.get('async_delay', 0)
        self.sequential = kwargs.get('sequential', False)

        # Dictionary to store output
        self.results = {}

    # ==============================================
    # Method to search for videos
    # ==============================================
    async def search(self, query, session=aiohttp.ClientSession()):
        """
        Search for videos based on a query.
        Args:
            query (str): The search query.
            session (aiohttp.ClientSession): The session used to make HTTP requests.
        Returns:
            list: A list of search results.
        """
        # Assert if search parameters are present
        assert 'search' in self.params.keys(), "Search parameters not found in params."

        # Add api_key to search parameters
        search_params = deepcopy(self.params['search'])
        search_params['key'] = self.api_key
        # Call search API
        self.results['search'] = await search(
                                            query, 
                                            search_params, 
                                            self.retry_limit, 
                                            self.retry_delay, 
                                            session, 
                                            self.verbose
                                        )

        if self.verbose:
            l_video_ids = list(set([i['id']['videoId'] for i in self.results['search']]))
            print(f"{len(l_video_ids)} videos found")

    # ==============================================
    # Method to fetch video data
    # ==============================================
    async def videos(self, video_id=None, session=aiohttp.ClientSession()):
        """
        Fetch video data for a single video ID or list of video IDs.
        Args:
            video_id (str/list): A single video ID or list of video IDs to fetch data for. Leave blank to use search results.
            session (aiohttp.ClientSession): The session used to make HTTP requests.
        Returns:
            dict: A list of video statistics.
        """
        # If video_id is not provided, use search results
        if video_id is None:
            video_id = list(set([i['id']['videoId'] for i in self.results['search']]))
        else:
            assert isinstance(video_id, str) or (isinstance(video_id, list) and all(isinstance(i, str) for i in video_id)), "video_id must be a string or a list of video IDs."

        # Assert if video parameters are present
        assert 'videos' in self.params.keys(), "Videos parameters not found in params."

        # Add api_key to videos parameters
        videos_params = deepcopy(self.params['videos'])
        videos_params['key'] = self.api_key
        # Call videos API
        self.results['videos'] = await videos(
                                            video_id, 
                                            videos_params, 
                                            self.async_delay, 
                                            self.retry_limit, 
                                            self.retry_delay, 
                                            self.sequential, 
                                            session, 
                                            self.verbose
                                        )

        if self.verbose:
            l_video_ids_filtered = [i['id'] for i in self.results['videos'] if i['statistics']['commentCount'] >= self.min_comments]
            print(f"{len(l_video_ids_filtered)} videos with {self.min_comments}+ comments")

    # ==============================================
    # Method to fetch comments
    # ==============================================
    async def comment_threads(self, video_id=None, session=aiohttp.ClientSession()):
        """
        Fetch comment threads for a single video ID or list of video IDs.
        Args:
            video_id (str/list): A single video ID or list of video IDs to fetch comments for. Leave blank to use video or search results.
            session (aiohttp.ClientSession): The session used to make HTTP requests.
        Returns:
            dict: A list of comment threads.
        """
        # If video_id is not provided, use video results
        if video_id is None:
            try:
                video_id = [i['id'] for i in self.results['videos'] if i['statistics']['commentCount'] >= self.min_comments]
            except:
                video_id = list(set([i['id']['videoId'] for i in self.results['search']]))
        else:
            assert isinstance(video_id, str) or isinstance(video_id, list), "video_id must be a string or a list of video IDs."

        # Assert if commentThreads parameters are present
        assert 'commentThreads' in self.params.keys(), "CommentThreads parameters not found in params."

        # Add api_key to commentThreads parameters
        commentThreads_params = deepcopy(self.params['commentThreads'])
        commentThreads_params['key'] = self.api_key
        # Call commentThreads API
        self.results['commentThreads'] = await comment_threads(
                                                    video_id, 
                                                    commentThreads_params, 
                                                    self.async_delay, 
                                                    self.retry_limit, 
                                                    self.retry_delay, 
                                                    self.sequential, 
                                                    session, 
                                                    self.verbose
                                                )
    
        if self.verbose:
            print(f"{sum([len(i) for i in self.results['commentThreads']])} comments retrieved for {len([i for i in self.results['commentThreads'] if len(i)])} videos")
    
    # ==============================================
    # Method to fetch transcript
    # ==============================================
    async def transcript(self, video_id=None, code_language='en', cookies=None, batch_size=5, batch_delay=1):
        """
        Fetch transcripts for a single video ID or list of video IDs.
        Args:
            video_id (str/list): A single video ID or list of video IDs to fetch transcripts for. Leave blank to use video or search results.
        Returns:
            dict: A list of transcripts.
        """
        # If video_id is not provided, use video results otherwise search results
        if video_id is None:
            try:
                video_id = [i['id'] for i in self.results['videos'] if i['statistics']['commentCount'] >= self.min_comments]
            except:
                video_id = list(set([i['id']['videoId'] for i in self.results['search']]))
        else:
            assert isinstance(video_id, str) or isinstance(video_id, list), "video_id must be a list of video IDs."
        
        # Call transcripts API
        self.results['transcripts'] = await transcript(
                                                video_id, 
                                                code_language, 
                                                cookies, 
                                                self.retry_limit, 
                                                self.retry_delay, 
                                                batch_size, 
                                                batch_delay, 
                                                self.verbose
                                            )

        if self.verbose:
            print(f"Transcripts for {len([i for i in self.results['transcripts'] if i])} videos retrieved")

    # ==============================================
    # Method to save output as JSON or CSV
    # ==============================================
    def to_json(self, file_path=None, **kwargs):
        """
        Save the search results to files in JSON format.

        Args:
            data (dict): The results data to save.
            file_path (str): The path where the files will be saved.
            default_cols (bool): Use default column names. Default=False
            shorten_cols (bool): Shorten column names. Default=False
            force_output (bool): Force output even if no data is available. Default=False
            verbose (bool): Print verbose output. Default=False
        """
        default_cols = kwargs.get('default_cols', False)
        shorten_cols = kwargs.get('shorten_cols', False)
        force_output = kwargs.get('force_output', False)
        verbose      = kwargs.get('verbose', False)
        to_json(self.results, file_path, default_cols=default_cols, shorten_cols=shorten_cols, force_output=force_output, verbose=verbose)
    
    def to_csv(self, file_path=None, **kwargs):
        """
        Save the search results to files in CSV format.

        Args:
            data (dict): The results data to save.
            file_path (str): The path where the files will be saved.
            default_cols (bool): Use default column names. Default=False
            shorten_cols (bool): Shorten column names. Default=False
            force_output (bool): Force output even if no data is available. Default=False
            verbose (bool): Print verbose output. Default=False
        """
        default_cols = kwargs.get('default_cols', False)
        shorten_cols = kwargs.get('shorten_cols', False)
        force_output = kwargs.get('force_output', False)
        verbose      = kwargs.get('verbose', False)
        to_csv(self.results, file_path, default_cols=default_cols, shorten_cols=shorten_cols, force_output=force_output, verbose=verbose)