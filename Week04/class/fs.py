#!/usr/bin/python3
# File to traverse a given directoru and retrieve all the files

import os
import sys
import argparse


def stat_file(to_stat):
    """Print out metadata for the file to_stat in a pipe-delimited format"""
    stat = os.stat(to_stat, follow_symlinks=False)
    # mode/umask
    mode = stat[0]
    # inode
    inode = stat[1]
    # uid
    uid = stat[4]
    # gid
    gid = stat[5]
    # file size
    fsize = stat[6]
    # access time
    atime = stat[7]
    # modification time
    mtime = stat[8]

    # ctime on Windows is the file creation time
    # ctime on on UNIX and UNIX-like systems is attribute modification time
    ctime = stat[9]
    crtime = stat[9]

    print(0, to_stat, inode, mode, uid, gid, fsize,
          atime, mtime, ctime, crtime, sep='|')


def body_builder(rootdir):
    """Build a forensic body file of the contents of rootdir"""

    # ensure that rootdir is actually a directory
    if not os.path.isdir(rootdir):
        raise ValueError(f'Not a directory: {rootdir}')

    file_list = []

    for root, subdirs, filenames in os.walk(rootdir):
        for f in filenames:
            # platform-agnostic way to concatenate paths
            file_list.append(os.path.join(root, f))

    for file in file_list:
        stat_file(file)


def __process_args():
    parser = argparse.ArgumentParser(
        description="Traverses a directory and builds a forensic body file",
        epilog="Developed by E. Array Minkoff, 10 Feb. 2022"
    )
    parser.add_argument("--directory", '-directory', required="True",
                        help="Directory to traverse.")

    args = parser.parse_args()

    return args.directory


# run if script is called
if __name__ == "__main__":
    # Raise an error if too few arguments are provided
    if len(sys.argv) < 2:
        sys.stderr.write("Not enough arguments.\n")
        sys.exit()
    # traverse dir
    try:
        body_builder(__process_args())
    except Exception as e:
        sys.stderr.write(str(e))
