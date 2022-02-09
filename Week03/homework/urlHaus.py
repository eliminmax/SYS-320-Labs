# FIXED: added missing import of `re` module
# INFO: import re and csv modules
import re
import csv


# FIXED: renamed function `ur1HausOpen` to `urlHausOpen`
# FIXED: renamed parameter `searchTerm` to `searchTerms`
def urlHausOpen(filename, searchTerms):
    # FIXED: indented this and following lines
    # FIXED: replaced `while` with `with`
    # FIXED: removed quotes around `'filename'`
    # INFO: open file at path `filename`, save to variable `f`
    with open(filename) as f:
        # FIXED: replaced `csv.review` with `csv.reader`
        # FIXED: replaced `==` with `=`
        # FIXED: replaced reference to string `filename` with file buffer `f`
        # FIXED: replaced `f` with `f.readlines()`
        # | EXPLANATION: using the file object `f` directly means closing it
        # |---| causes a ValueError: I/O operation on closed file.
        # INFO: create a csv reader object
        contents = csv.reader(f.readlines())
    # INFO: skip the first 9 lines - these are file metadata we don't need.
    for skipped_line in range(9):
        # INFO: skip to the next item in the iterator
        next(contents)
    # FIXED: loops were nested in the opposite of the right order.
    # INFO: iterate over contents
    for eachLine in contents:
        # INFO: iterate over searchTerms
        for keyword in searchTerms:
            # FIXED: replaced `r+keyword+` with `r'.*'+keyword+r'.*'`
            x = re.findall(r'.*'+keyword+r'.*', eachLine[2])
            # Print info about the match
            for _ in x:
                # Don't edit this line. It is here to show how it is possible
                # to remove the "tt" so programs don't convert the malicious
                # domains to links that an be accidentally clicked on.
                the_url = eachLine[2].replace("http", "hxxp")
                the_src = eachLine[4]

                # FIXED: replaced `"+60` with `"*60` - can't add int to string
                # FIXED: included formatting place for url and info
                # FIXED: replaced `""",format` with proper syntax `""".format`
                print("""
URL: {}
Info: {}
{}""".format(the_url, the_src, "*"*60))
