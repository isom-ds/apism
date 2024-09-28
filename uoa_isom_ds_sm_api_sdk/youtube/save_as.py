from .utils import _flatten_json, _shorten_keys
from .columns_names import _column_names
import json
import csv
import os
import re
import copy
import warnings

def save_as_json(data, file_name, flatten=False):
    """
    Save the search results to a file in JSON format.

    Args:
        data (dict): The search results data to save.
        file_name (str): The (path and) name of the file to save the data in.
    """
    if flatten:
        output = {
            k: {
                'search': _flatten_json(v['search']),
                'video': _flatten_json(v['video']),
                'commentThreads': [_flatten_json(i) for i in v['commentThreads'] if i]
            } for k, v in data.items()
        }
        # Flatten replies.comments in commentThreads
        for k, v in output.items():
            for idx, comments in enumerate(v['commentThreads']):
                if 'replies.comments' in comments.keys():
                    output[k]['commentThreads'][idx]['replies.comments'] = [_flatten_json(i) for i in comments['replies.comments'] if i]
    else:
        output = data

    with open(file_name, 'w') as json_file:
        json.dump(output, json_file, indent=4)

def save_as_csv(data, file_path=None, shorten_keys=False, **kwargs):
    """
    Save the search results to a file in CSV format.

    Args:
        data (dict): The search results data to save.
        file_path (str): The path to the file where data will be saved.
        shorten_keys (bool): Whether to shorten the keys of the dictionary.
    """
    # Kwargs
    infer_cols = kwargs.get('infer_cols', True)
    force_output = kwargs.get('force_output', False)

    # Assign column names
    if shorten_keys:
        search_cols = _column_names['shorten']['search']
        video_cols = _column_names['shorten']['video']
        commentThreads_cols = _column_names['shorten']['commentThreads']
        replies_cols = _column_names['shorten']['replies']
    else:
        search_cols = _column_names['original']['search']
        video_cols = _column_names['original']['video']
        commentThreads_cols = _column_names['original']['commentThreads']
        replies_cols = _column_names['original']['replies']

    # Function to remove line breaks and extra spaces from strings
    def preprocess_data(data_in):
        if data_in is None or len(data_in) == 0:
            return None
        else:
            data = copy.deepcopy(data_in)
            for row in data:
                for key, value in row.items():
                    if isinstance(value, str):
                        # Remove \r and \n, and replace multiple spaces with a single space
                        value = value.replace('\r', ' ').replace('\n', ' ')
                        value = re.sub(' +', ' ', value)
                        row[key] = value
            return data

    # Function to write a dictionary to a CSV file
    def write_dict_to_csv(filename, data, infer_cols=True, col_names=None):
        """
        Write a dictionary to a CSV file.

        Args:
            filename (str): The name of the CSV file.
            data (list): The list of dictionaries to write to the CSV file.
        """
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=col_names, quoting=csv.QUOTE_ALL)
            if data:
                writer.writeheader()
                for row in data:
                    writer.writerow(row)

    # Flatten dictionary
    flattened = {
        k: {
            'search': _flatten_json(v['search']),
            'video': _flatten_json(v['video']),
            'commentThreads': [_flatten_json(i) for i in v['commentThreads'] if i]
        } for k, v in data.items()
    }
    # Flatten replies.comments in commentThreads
    for k, v in flattened.items():
        for idx, comments in enumerate(v['commentThreads']):
            if 'replies.comments' in comments.keys():
                flattened[k]['commentThreads'][idx]['replies.comments'] = [_flatten_json(i) for i in comments['replies.comments'] if i]

    # Extract data for each CSV
    search_data = [v['search'] for v in flattened.values()]
    video_data = [v['video'] for v in flattened.values()]
    comment_threads_data = []
    replies_data = []

    for v in flattened.values():
        for comment_thread in v['commentThreads']:
            comment_threads_data.append({k: v for k, v in comment_thread.items() if k != 'replies.comments'})
            if 'replies.comments' in comment_thread:
                replies_data.extend(comment_thread['replies.comments'])

    # Shorten keys if specified
    if shorten_keys:
        search_data = [_shorten_keys(i) for i in search_data if i]
        video_data = [_shorten_keys(i) for i in video_data if i]
        comment_threads_data = [_shorten_keys(i) for i in comment_threads_data if i]
        replies_data = [_shorten_keys(i) for i in replies_data if i]

    # Check if all columns are present
    if infer_cols == False:
        for datalist, cols in zip(
            [search_data, video_data, comment_threads_data, replies_data],
            [search_cols, video_cols, commentThreads_cols, replies_cols]
        ):
            if datalist or any(item is not None for item in datalist):
                for row in datalist:
                    for col in cols:
                        if col not in row.keys():
                            row[col] = None

    # Preprocess data to remove \r and \n
    search_data = preprocess_data(search_data)
    video_data = preprocess_data(video_data)
    comment_threads_data = preprocess_data(comment_threads_data)
    replies_data = preprocess_data(replies_data)

    # Determine file path
    if file_path is None:
        file_path = os.getcwd()

    # Raise warning if no data is available
    if search_data is None or len(search_data) == 0:
        warnings.warn("No search data available. The search results are empty.")
    if video_data is None or len(video_data) == 0:
        warnings.warn("No video data available. The video results are empty.")
    if comment_threads_data is None or len(comment_threads_data) == 0:
        warnings.warn("No commentThreads data available. The commentThreads results are empty.")
    if replies_data is None or len(replies_data) == 0:
        warnings.warn("No replies data available. The replies results are empty.")

    # Write data to CSV files
    for output_list, file_name, cols in zip(
            [search_data, video_data, comment_threads_data, replies_data],
            ['search.csv', 'video.csv', 'commentThreads.csv', 'replies.csv'],
            [search_cols, video_cols, commentThreads_cols, replies_cols]
        ):
        if output_list is not None or len(output_list) > 0 or force_output:
            if infer_cols:
                col_names = list({key for row in output_list for key in row.keys()})
            else:
                col_names = cols
            write_dict_to_csv(os.path.join(file_path, file_name), output_list, col_names)