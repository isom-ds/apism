from .utils import _flatten_json, _shorten_keys
import json
import csv
import os

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
                'commentThreads': [_flatten_json(i) for i in v['commentThreads']]
            } for k, v in data.items()
        }
        # Flatten replies.comments in commentThreads
        for k, v in output.items():
            for idx, comments in enumerate(v['commentThreads']):
                if 'replies.comments' in comments.keys():
                    output[k]['commentThreads'][idx]['replies.comments'] = [_flatten_json(i) for i in comments['replies.comments']]
    else:
        output = data

    with open(file_name, 'w') as json_file:
        json.dump(output, json_file, indent=4)

def save_as_csv(data, file_path=None, shorten_keys=False):
    """
    Save the search results to a file in CSV format.

    Args:
        data (dict): The search results data to save.
        file_path (str): The path to the file where data will be saved.
        shorten_keys (bool): Whether to shorten the keys of the dictionary.
    """
    # Function to write a dictionary to a CSV file
    def write_dict_to_csv(filename, data):
        """
        Write a dictionary to a CSV file.

        Args:
            filename (str): The name of the CSV file.
            data (list): The list of dictionaries to write to the CSV file.
        """
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=list(data[0].keys()), quoting=csv.QUOTE_ALL)
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
                flattened[k]['commentThreads'][idx]['replies.comments'] = [_flatten_json(i) for i in comments['replies.comments']]

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
        search_data = [_shorten_keys(i) for i in search_data]
        video_data = [_shorten_keys(i) for i in video_data]
        comment_threads_data = [_shorten_keys(i) for i in comment_threads_data]
        replies_data = [_shorten_keys(i) for i in replies_data]

    # Determine file path
    if file_path is None:
        file_path = os.getcwd()

    # Write data to CSV files
    write_dict_to_csv(os.path.join(file_path, 'search.csv'), search_data)
    write_dict_to_csv(os.path.join(file_path, 'video.csv'), video_data)
    write_dict_to_csv(os.path.join(file_path, 'commentThreads.csv'), comment_threads_data)
    write_dict_to_csv(os.path.join(file_path, 'replies.csv'), replies_data)