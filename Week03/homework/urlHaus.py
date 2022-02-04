# FIXED: added missing import of `re` module
# INFO: import re and csv modules
import re
import csv

# TODO: rename `_` and `x` - should have more meaninful names


# FIXED: renamed function `ur1HausOpen` to `urlHausOpen`
# FIXED: renamed parameter `searchTerm` to `searchTerms`
def urlHausOpen(filename, searchTerms):
    # FIXED: indented this and following lines
    # FIXED: replaced `while` with `with`
    # FIXED: removed quotes around `'filename'`
    # INFO: open file at path `filename`, save to variable `f`
    with open(filename) as f:
        # FIXED: replaced `csv.review` with `csv.reader`
        # FIXED: replace `==` with `=`
        # INFO: create a csv reader object
        contents = csv.reader(filename)
    # TODO: figure out why we're looping 9 times
    # INFO: Loop 9 times
    for _ in range(9):
        # TODO: figure out what this is supposed to do
        # INFO: next(csv.reader) is valid syntax, but
        # this line does not do anything with it
        # FIXED: saved return value to variable nextCSVEntry
        nextCSVEntry = next(contents)
        # INFO: iterate over searchTerms
        # FIXME: searchTerms is a string, so this iterates over characters.
        # I assume that that's not intentional
        for keyword in searchTerms:
            for eachLine in contents:
                # FIXME: do something with x
                # FIXME: eachline[2] is out-of-bounds
                # FIXED: replaced `r+keyword+` with `r'.*'+keyword+r'.*'`
                x = re.findall(r'.*'+keyword+r'.*', eachLine[2])
    # FIXME: determine proper indentation for this loop
    for _ in x:
        # Don't edit this line. It is here to show how it is possible
        # to remove the "tt" so programs don't convert the malicious
        # domains to links that an be accidentally clicked on.
        the_url = eachLine[2].replace("http", "hxxp")
        the_src = eachLine[4]

        # FIXED: replaced `"*"+60` with `"*60"` - cannot add int to string
        print("""
URL:
Info: 
{}""", format(the_url, the_src, "*"*60))
