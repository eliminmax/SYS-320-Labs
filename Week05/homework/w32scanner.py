#!/usr/bin/python3
"""Searches csv logs for signs of malicious activity.
"""
import misc_util


def search_logs(re_patterns, log_files, rootdir):
    """Search log files for regex matches, then return them in a dict
    structured as follows: 
    {
        filename: [
            "0,foo,C:\\bar\\foo",
            "1,spam,D:\\eggs"
        ]
    }
    Loosely adapted from last week's homework
    """
    # ensure that rootdir is a pathlib.Path object, and not relative
    rootdir = Path(rootdir).resolve()
    # create a dict to store matches
    matches = {}
    # Iterate overlog_files
    for _file in log_files:
        with open(_file) as f:
            # add each line which matches any re_pattern to matches[_file]
            for _line in f.readlines():
                for re_pattern in re_patterns:
                    # if _line matches, add it to matches[_file] then break
                    if re_pattern.search(_line):
                        # create the match list for file_ if it doesn't exist
                        if _file not in matches:
                            matches[_file] = []
                        matches[_file].append(_line)
                        break
    return matches


def main():
    """The main function, isolated for cleaner code. Called if run directly"""
    pass


if __name__ == '__main__':
    main()
