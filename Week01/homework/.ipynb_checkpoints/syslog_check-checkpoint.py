"""Simple module to search a log file for regex pattern matches
"""

import re

def parse(log_file_path, regex_patterns):
    """Return a list of matches for regex patterns in a log file
    """
    with open(log_file_path, 'r') as log_file:
        log_entries = log_file.readlines()
        
    # pre-compiling the patterns is more efficient than 
    # compiling them every time they're needed
    _compiled_regex_patterns = [
        re.compile(pattern) for pattern in regex_patterns
    ]
    
    results = list()
    for entry in log_entries:
        new_result = list()
        for pattern in _compiled_regex_patterns:
            match = pattern.findall(entry)
            if match:
                new_result.append(match)
        if new_result:
            results += new_result
                
    return results