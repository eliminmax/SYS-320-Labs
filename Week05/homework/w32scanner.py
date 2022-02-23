#!/usr/bin/python3
"""Searches csv logs for signs of malicious activity.
"""
import argparse
import csv
import re
import yaml
from pathlib import Path
import misc_util


def search_cols(searches, log_files, rootdir,
                col_ids=None, skip_header=True, highlight=False):
    """Search csv files by column for regex matches
    searches: a collection of iterables, with the following characteristics:
        - searches[n] always has at least 3 elements, for any index n
          - searches[n][0] is always a compiled regex pattern
          - searches[n][1] is the column to search
            - This can be an int or a string matching the name of a column
          - searches[n][2] is an identifier for the pattern
    """
    # Default to the format used in (REPO_ROOT)/logs/w32processes/*.csv
    if col_ids is None:
        col_ids = ',arguments,hostname,name,path,pid,username'.split(',')
    # create a dict to store matches
    matches = {}
    # Iterate over log_files
    for log in log_files:
        with open(Path(rootdir).joinpath(log)) as f:
            csv_reader = csv.reader(f.readlines())
        # skip header line (unless skip_header was set to False)
        if skip_header:
            next(csv_reader)
        # add each line which matches any search pattern to matches[log]
        for row in csv_reader:
            # if row matches, add it to matches[log][index] then break
            for index, (pattern, column, identifier) in enumerate(searches):
                # set col_num - if column is a string, get its index
                if type(column) == str:
                    col_num = col_ids.index(column)
                else:
                    col_num = column
                if pattern.search(row[col_num]):
                    # create the match dict for log[index] if needed
                    if log not in matches or identifier not in matches[log]:
                        matches[log] = {identifier: []}
                    # if highlight, highlight the match with ANSI esc sequences
                    # \x1b[30;103m colors black w/ yellow background
                    # \x1b[0m clears formatting
                    # '\1' is the matched pattern
                    if highlight:
                        row[col_num] = pattern.sub(
                            '\x1b[30;103m\\1\x1b[0m', row[col_num])
                    matches[log][identifier].append(row)
                    break
    return matches


def load_search_patterns(filepath):
    """Load search patterns from YAML file, using the following process:
    1: load the contents of the YAML file at `filepath` into a dict
    2: flatten the dict, so that 'a':{'b':{'c':'d'}} becomes 'a:b:c':'d'
    3: compile the regex patterns, to improve performance when repeatedly used

    This function was taken from Week04/homework/scanner.py, then modified to
    meet the requirements for search_col(searches)
    """
    # load the data
    with open(filepath) as f:
        raw_yaml_data = yaml.safe_load(f)

    # flatten the dataTEM\CurrentControlSet\Control\Lsa\
    flattened_data = misc_util.flatten_dict(raw_yaml_data)
    return [(re.compile(f'({v[0]})',  # Put in parenthases for highlighting
                        # Windows is case-insensitive, we should be too
                        re.IGNORECASE),
             v[1], k) for k, v in flattened_data.items()]


def main():
    """The main function, isolated for cleaner code. Called if run directly.
    """
    # First things first: load args
    parser = argparse.ArgumentParser(
        description="Find regex matches in specific column of a CSV file",
        epilog="Developed by E. Array Minkoff, 17-22 Feb. 2022"
    )
    parser.add_argument('-d', '--directory', '-directory',
                        help='directory containing csv files to search',
                        required=True)
    parser.add_argument('-s', '--search-file', '-search-file',
                        help='YAML file containing search data',
                        required=True)
    parser.add_argument('--color', '-color',
                        help="Edit the matches to highlight them when printed",
                        action=argparse.BooleanOptionalAction,
                        default=False
                        )
    args = parser.parse_args()
    # Load up the searches and get a list of CSV files to search
    csv_files = misc_util.get_file_list(args.directory, file_glob="*.csv")
    searches = load_search_patterns(args.search_file)
    # Parse the logs
    matches = search_cols(searches, csv_files, args.directory,
                          highlight=args.color)
    # get the values - matches is a
    for match in misc_util.flatten_dict(matches).values():
        for row in match:
            print(','.join(row[1:]))


if __name__ == '__main__':
    main()
