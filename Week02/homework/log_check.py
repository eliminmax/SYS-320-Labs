"""Simple module to search a log file for regex pattern matches
"""

import re
import sys
import yaml


# Load patterns and terms from a YAML file. I hate YAML.
try:
    with open("searchTerms.yaml", 'r') as yf:
        keywords = yaml.safe_load(yf)
except EnvironmentError as e:
    print(e.strerror)


def parse(log_file_path, service, term):
    """Return a list of matches for regex patterns in a log file
    """

    terms = keywords[service][term]

    re_patterns = terms.split(',')

    with open(log_file_path, 'r') as log_file:
        log_entries = log_file.readlines()

    # pre-compiling the patterns is more efficient than
    # compiling them every time they're needed
    _compiled_re_patterns = [re.compile(pattern) for pattern in re_patterns]

    results = list()
    # check for matches within the log entry
    for entry in log_entries:
        for pattern in _compiled_re_patterns:
            # save a list of all matches for the pattern to results list.
            matches = pattern.findall(entry)
            if matches:
                results.append(matches)

    return results
