import log_check


def apache_events(filename, service, term):
    matches = log_check.parse(filename, service, term)

    # found list

    found = []

    # loop through the results
    for match in matches:
        if len(match) != 1:
            print("Warning: unexpected list size!",
                  len(match), match)
        else:
            sp_results = match[0].split(" ")
            found.append(' '.join([sp_results[3]] + sp_results[0:2]))

    for found_item in found:
        print(found_item)


if __name__ == "__main__":
    from sys import argv

    if len(argv[1:]) == 3:
        apache_events(*argv[1:])

    else:
        raise Exception
