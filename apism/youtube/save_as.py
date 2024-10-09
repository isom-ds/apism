from .utils import _flatten_results, _shorten_keys, _preprocess_data, _reorder_dict, _write_dict_to_csv
from .defaults import _default_columns
import json
import os
import re
import warnings

def to_json(results, file_path=None):
    """
    Save the search results to a file in JSON format.

    Args:
        data (dict): The search results data to save.
        file_path (str): The path where the files will be saved.
    """
    # Determine file path
    if file_path is None:
        output_path = os.path.join(os.getcwd(), 'results.json')
    else:
        output_path = os.path.join(file_path, 'results.json')

    with open(output_path, 'w') as json_file:
        json.dump(results, json_file)

def to_csv(results, file_path=None, **kwargs):
    """
    Save the search results to files in CSV format.

    Args:
        data (dict): The results data to save.
        file_path (str): The path where the files will be saved.
    Kwargs:
        default_cols (bool): Use default column names. Default=False
        shorten_cols (bool): Shorten column names. Default=False
        force_output (bool): Force output even if no data is available. Default=False
        verbose (bool): Print verbose output. Default=False
    """
    # Kwargs
    default_cols = kwargs.get('default_cols', False)
    shorten_cols = kwargs.get('shorten_cols', False)
    force_output = kwargs.get('force_output', False)
    verbose      = kwargs.get('verbose', False)

    # Determine file path
    if file_path is None:
        file_path = os.getcwd()

    # Flatten dictionary
    flattened = _flatten_results(results)

    output = {}
    col_names = {}
    for k, v in flattened.items():
        # Transcripts
        if k in ['search', 'videos', 'commentThreads', 'commentThreadsreplies']:
            # Shorten wikipedia link for video topics
            if k == 'videos':
                for i in v:
                    if 'topicDetails.topicCategories' in i.keys():
                        i['topicDetails.topicCategories'] = '|'.join([re.search(r'/([^/]+)$', i).group(1) for i in i['topicDetails.topicCategories']])
            
            # Shorten keys if specified
            if shorten_cols:
                flattened[k] = [_shorten_keys(i) for i in v if i]
            
            # Preprocess data to remove \r and \n
            flattened[k] = _preprocess_data(flattened[k])

        # Column names
        if default_cols:
            if shorten_cols:
                col_names[k] = _default_columns['shorten'][k]
            else:
                col_names[k] = _default_columns['default'][k]
        else:
            col_names[k] = list({key for row in v if row for key in row.keys()})

        # Reorder dict
        output[k] = _reorder_dict(flattened[k], col_names[k])
        
        # Raise warning if no data is available
        if (output[k] is None or len(output[k]) == 0) and verbose:
            warnings.warn(f"No {k} data available.")

        # Write data to CSV files
        if output[k] or force_output:
            _write_dict_to_csv(os.path.join(file_path, f"{k}.csv"), output[k], col_names[k])