#!/usr/bin/env python3

"""
$Id: wrapify.py 1306 2003-07-02 14:23:06Z david $

Wraps a block of text at a given margin.  Reads from stdin.  Writes to
stdout.

The block of text is never wrapped within a word.  If the text cannot be
wrapped it is returned "as is".  This is to allow for the likelihood that
this script will be used on code, which, of course, cannot have its tokens
split in two.  Even if they're hyphenated!  Trust me on this...  :-)
"""

import sys


# Use Python's built-in True/False
WRAP_COLUMN = 80
SPACE = " "


def split_line(line, column=WRAP_COLUMN):
    """
    Splits a line, if necessary, into two lines.  The first line
    contains the result after wrapping.  The second line contains
    whatever is left over, regardless of the length.  Both lines
    are returned, regardless of the result of the split.
    """
    if len(line) > column:
        split_point = line.rfind(" ", 0, column)
    else:
        split_point = -1

    if split_point > 0:
        # We have a point at which to split the line
        line1 = line[:split_point]
        line2 = line[split_point+1:]
    else:
        # There is nowhere to split this line
        line1 = line
        line2 = ""

    return line1, line2


def wrapify(block, column=WRAP_COLUMN):
    """
    Manages the wrapping of text.  We simply split each line, if
    necessary, pushing the overhang onto the next line.  This next
    line is then split, and so on, and so on.
    """
    new_block = block[:]
    for i in range(len(new_block)):
        # Split the line for wrapping, cleaning the new line and
        # excess for buffering
        new_line, excess = split_line(new_block[i], column)
        new_block[i] = new_line.rstrip()
        excess = excess.rstrip()
        # Make sure we don't lose any excess
        if excess:
            if i + 1 < len(new_block):
                new_block[i+1] = excess + " " + new_block[i+1]
            else:
                new_block.append(excess)
    return new_block


def main():
    try:
        column = int(sys.argv[1])
    except IndexError:
        column = WRAP_COLUMN
    block = sys.stdin.readlines()
    wrapped_block = wrapify(block, column)
    for line in wrapped_block:
        print(line)


if __name__ == '__main__':
    main()
