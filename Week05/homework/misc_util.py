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
