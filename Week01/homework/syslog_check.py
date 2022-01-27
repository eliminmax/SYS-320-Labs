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
    # check for matches within the log entry
    for entry in log_entries:
        for pattern in _compiled_regex_patterns:
            # save a list of all matches for the pattern to results list.
            matches = pattern.findall(entry)
            if matches:
                results.append(matches)

    return results
