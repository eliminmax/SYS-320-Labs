#!/usr/bin/python3
"Scan logs in directory for indications of various attack types"
import argparse
import re
import yaml
from pathlib import Path

import misc_util


def load_search_patterns(filepath):
    """Load search patterns from YAML file, using the following process:
    1: load the contents of the YAML file at `filepath` into a dict
    2: flatten the dict, so that 'a':{'b':{'c':'d'}} becomes 'a:b:c':'d'
    3: compile the regex patterns, to improve performance when repeatedly used
    """
    # load the data
    with open(filepath) as f:
        raw_yaml_data = yaml.safe_load(f)

    # flatten the data
    flattened_data = misc_util.flatten_dict(raw_yaml_data)

    # return dict of case-insensitive compiled patterns:
    return {k: re.compile(v, flags=re.I) for k, v in flattened_data.items()}


def get_file_list(rootdir, file_glob='*'):
    """Return a list of files in rootdir or its subdirectories
    """
    # ensure that rootdir is a pathlib.Path object, and not relative
    rootdir = Path(rootdir).resolve()
    # recursively search rootdir for files matching file_glob
    # note that unlike POSIX systems, '*' matches hidden files
    return [p.resolve().relative_to(rootdir) for p in rootdir.rglob(file_glob) if p.is_file()]


def search_logs(re_patterns, log_files, rootdir):
    """Search log_files for matches of any provided regex patterns"""
    rootdir = Path(rootdir).resolve()
    # ensure that rootdir is a pathlib.Path object, and not relative
    for file in log_files:
        with open(rootdir.joinpath(file)) as f:
            lines = f.readlines()
            # Iterate over lines
            for line_num, line_text in enumerate(lines):
                # re_patterns is a dict of format "category:searchterm": regex
                for pattern_name, pattern in re_patterns.items():
                    # if the line contains a match, print an alert
                    if pattern.search(line_text):
                        print(f'{file}:{line_num} {pattern_name}',
                              line_text, end='')
                        # end='' because the line already ends with a newline


def __process_args():
    parser = argparse.ArgumentParser(
        description="Traverses a directory and searches for regex matches" +
        " defined in SEARCHFILE",
        epilog="Developed by E. Array Minkoff, 12 Feb. 2022"
    )
    parser.add_argument("--directory", '-directory', required="True",
                        help="Directory to load log files from.")

    parser.add_argument("--searchfile", '-searchfile', required="True",
                        help="YAML file containing search patterns.")

    args = parser.parse_args()

    return args


# called if run directly, rather than imported
if __name__ == '__main__':
    # load args
    args = __process_args()
    # build list of files
    file_list = get_file_list(args.directory)
    # load search pattern dictionary
    search_patterns = load_search_patterns(args.searchfile)
    # actually search the logs for matches
    search_logs(search_patterns, file_list, args.directory)
