import log_check


def print_matched_events(filename, service, term, fields):
    matches = log_check.parse(filename, service, term)
    # list for found matches
    found = []
    # loop through the results of log_check, parse results
    for match in matches:
        # match will be a list of all regex matches on a given line.
        # only expect 1 match per line; print warning if more than 1
        if len(match) != 1:
            print("Warning: unexpected list size!",
                  len(match), match)
        else:
            # split the match at each space
            sp_results = match[0].split(" ")
            # reassemble it, with only the parts we want
            found.append(' '.join(sp_results[i] for i in fields))
    # print reassembled events
    for found_item in found:
        print(found_item)
