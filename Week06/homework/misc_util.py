"""This module contains, as the name implies, assorted utilities that
I have copied either from the internet or older submissions of mine from
previous weeks.
"""
import collections.abc
from pathlib import Path


def flatten_dict(d, parent_key='', sep=':'):
    """Flatten a multi-level dictionary into a one-level dictionary

    From https://stackoverflow.com/a/6027615, with the following changes:
    - Added this docstring
    - Renamed the function from flatten to flatten_dict
    - Changed the default value for sep
    - Replaced depracated collections.MutableMapping its modern replacement,
                          collections.abc.MutableMapping

    The following StackOverflow users contributed to the original:
    - https://stackoverflow.com/users/1897/imran - wrote answer
    - https://stackoverflow.com/users/12892/cristian-ciupitu - edited answer
    - https://stackoverflow.com/users/1645874/mythsmith - edited answer
    """
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + str(k) if parent_key else str(k)
        if isinstance(v, collections.abc.MutableMapping):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def get_file_list(rootdir, file_glob='*'):
    """Return a list of files in rootdir or its subdirectories
    This function was originally part of Week04/homework/scanner.py.
    I copied it out, because it's generic enough to be useful elsewhere.
    I rewrote the list constructor as a for loop for better readability.
    """
    # ensure that rootdir is a pathlib.Path object, and not relative
    rootdir = Path(rootdir).resolve()
    # recursively search rootdir for files matching file_glob
    # note that unlike POSIX systems, '*' matches hidden files
    file_list = []
    for subpath in rootdir.rglob(file_glob):
        if subpath.is_file():
            file_list.append(subpath.relative_to(rootdir))

    return file_list


def prompt_yn(prompt, default=None, max_tries=-1):
    """Prompt the user for a y/n response to a question, and return a bool
    Parameters:
        prompt is the string to use to prompt for user input.
        default can be set to 'y', 'n', 'Y', or 'N', to provide a default value
        if max_tries is a positive integer, an exception will be raised after
        that number is hit
    """
    default_set = default is not None
    hint = '(y/n)'
    if default_set:
        # set hint to capitalize the default option
        hint = '(Y/n)' if default.lower() == 'y' else '(y/N)'
        # Start with empty answer variable
    answer = ''

    while answer not in ('y', 'n'):
        if max_tries > 0:
            max_tries -= 1
        elif max_tries == 0:
            raise ValueError("Too many bad inputs.")
        # Print prompt, followed by an answer hint (y/n), with capital default
        answer = input(f"{prompt + ' ' if prompt else ''}{hint}: ").lower()
        # If no input was recieved, and a default was given, use the default
        if not answer:
            if default_set:
                answer = default
    return answer == 'y'
