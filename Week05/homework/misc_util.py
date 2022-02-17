import collections.abc


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
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, collections.abc.MutableMapping):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)
