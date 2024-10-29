import aiohttp
import asyncio
import copy
import csv
import re

class YouTubeAPIException(Exception):
    """Custom exception for YouTube API errors"""
    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message
        super().__init__(f"API Error {status_code}: {message}")

async def _fetch_with_retries(url, params, retry_limit=3, retry_delay=1, session=aiohttp.ClientSession(), verbose=False):
    """
    Fetch data from a URL with retries and handle errors related to disabled comments.
    
    Args:
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
                    if verbose:
                        print(f"Comments are disabled for video ID: {__params__['videoId']}")
                    return None, None
                
                # Handle API limit errors and other issues
                if response.status == 200:
                    next_page_token = response_data.get('nextPageToken')
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

def _flatten_json(nested_json, parent_key='', sep='.'):
    """
    Flatten a nested JSON dictionary.

    Args:
        nested_json (dict): The JSON dictionary to flatten.
        parent_key (str): The base key string for recursion.
        sep (str): The separator between keys.

    Returns:
        dict: The flattened JSON dictionary.
    """
    if nested_json is None or len(nested_json) == 0:
        return None
    else:
        items = []
        for k, v in nested_json.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(_flatten_json(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)

def _flatten_results(results):
    """
    Flatten the results dictionary to remove nested dictionaries.
    """
    data = copy.deepcopy(results)
    output = {}
    for k,v in data.items():
        if k == 'commentThreads':
            output[k] = sum([[_flatten_json(i) for i in j] for j in v if j], [])
            # Flatten replies.comments in commentThreads
            replies = []
            for idx, comments in enumerate(output['commentThreads']):
                if 'replies.comments' in comments.keys():
                    replies_comments = output['commentThreads'][idx].pop('replies.comments', None)
                    replies.append([_flatten_json(i) for i in replies_comments if i])
            # Add replies to output
            if replies:
                output['commentThreadsreplies'] = sum([i for i in replies if i], [])
            else:
                output['commentThreadsreplies'] = None
        elif k == 'transcripts':
            output[k] = v
        else:
            output[k] = [_flatten_json(i) for i in v]
    return output

def _shorten_keys(data):
    """
    Shorten the keys of a dictionary to the last string after the separator '.'.

    Args:
        data (dict): The dictionary with keys to be shortened.

    Returns:
        dict: The dictionary with shortened keys.
    """
    if data is None or len(data) == 0:
        return None
    else:
        return {key.split('.')[-1]: value for key, value in data.items()}

# Function to remove line breaks and extra spaces from strings
def _preprocess_data(data_in):
    """
    Preprocess data by removing line breaks and extra spaces from strings.
    """
    if data_in is None or len(data_in) == 0:
        return None
    else:
        data = copy.deepcopy(data_in)
        for row in data:
            for key, value in row.items():
                if isinstance(value, str):
                    # Remove \r and \n and commas, and replace multiple spaces with a single space
                    row[key] = re.sub(r'[\r\n\s]+', ' ', value).replace(',', '')
        return data

# Function to write a dictionary to a CSV file
def _write_dict_to_csv(filename, data, col_names=None):
    """
    Write a dictionary to a CSV file.

    Args:
        filename (str): The name of the CSV file.
        data (list): The list of dictionaries to write to the CSV file.
    """
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=col_names, quoting=csv.QUOTE_ALL, escapechar='\\')
        writer.writeheader()
        if data:
            for row in data:
                writer.writerow(row)

# Function to reorder a list of dictionaries based on column list
def _reorder_dict(data, columns):
    """
    Reorder the list of dictionaries based on the column order.

    Args:
        data (dict): The list of dictionaries to reorder.
        columns (list): The list of column names in the desired order.

    Returns:
        dict: The reordered list of dictionaries.
    """
    if data is None or len(data) == 0:
        return None
    else:
        output = []
        for i in data:
            if i:
                dict_data = {}
                for col in columns:
                    if col in i.keys():
                        dict_data[col] = i[col]
                    else:
                        dict_data[col] = None
                output.append(dict_data)
        return output