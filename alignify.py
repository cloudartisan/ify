#!/usr/bin/env python3

"""
$Id: alignify.py 1302 2003-07-02 13:34:15Z david $

Aligns text around a given align indicator.
If run from the command line, it will read from stdin
and write the result to stdout.

Examples:
    ./alignify -l < code.py > newcode.py
    ./alignify -r < code.py > newcode.py
    ./alignify -i and < code.py > newcode.py
"""

import sys
import getopt

# Possible exit statuses
EXIT_SUCCESS = 0
EXIT_FAILURE = 1

# Supported short command line options
OPT_INDICATOR = "-i"
OPT_RIGHTMOST = "-r"
OPT_LEFTMOST = "-l"
OPT_PADDING = "-p"
OPTS = "i:p:rl"

# Option indexes
OPT = 0
VAL = 1

# Alignment types
ALIGN_RIGHTMOST = "R"
ALIGN_LEFTMOST = "L"

# Defaults
ALIGN_INDICATOR = "="
ALIGN_TYPE = ALIGN_RIGHTMOST

# Globals
align_type = ALIGN_TYPE
align_indicator = ALIGN_INDICATOR
padding = 0


def get_align_index(block, align_str=ALIGN_INDICATOR, align_type=ALIGN_TYPE):
    """
    Accepts a block of text and returns the length at which to
    align the block.  Of course, this length is dependent upon
    the location of the alignment indicator.
    """
    align_index = -1

    for line in block:
        left_val = ""
        # Skip lines that do not contain an alignment indicator
        if line.find(align_str) == -1:
            continue
        try:
            left_val = line.split(align_str)[0]
        except ValueError:
            continue
        left_val_len = len(left_val)
        # Length of align is dependent on alignment type
        if align_index == -1:
            align_index = left_val_len
        elif align_type == ALIGN_RIGHTMOST:
            align_index = max(left_val_len, align_index)
        elif align_type == ALIGN_LEFTMOST:
            align_index = min(left_val_len, align_index)
    return align_index


def align_line(line, align_index, align_str=ALIGN_INDICATOR):
    """
    Accepts a line of text, the alignment length, and the string with
    which to align the block.  Attempts to align the block of text.
    If an unexpected exception occurs, the original line is returned.
    Otherwise, the aligned block of text is returned.
    """
    try:
        left_val, right_val = line.split(align_str, 1)
        left_val = left_val.rstrip()
        diff_len = align_index - len(left_val)
        left_val = left_val + (" " * diff_len) + (" " * padding)
        result = f"{left_val}{align_str}{right_val}"
    except Exception:
        result = line
    return result


def align_block(block, align_str=ALIGN_INDICATOR, align_type=ALIGN_TYPE):
    """
    Accepts a block of text (a list of lines), the string with which
    to align the block, and the alignment type.  Returns the aligned
    block of text.
    """
    # Determine the length at which to align the block
    align_index = get_align_index(block, align_str, align_type)

    # Align the block now
    aligned_block = []
    for line in block:
        if line.find(align_str) == -1:
            aligned_line = line
        else:
            aligned_line = align_line(line, align_index, align_str)
        aligned_block.append(aligned_line)
    return aligned_block


def usage():
    """
    Simply prints the usage information.
    """
    print(f"Usage: {sys.argv[0]} [-i indicator] [-p padding] [-r|-l]")


def die_usage(status, reason=None):
    """
    Prints the usage information and an optional error message.
    """
    if reason:
        sys.stderr.write(f"Error: {reason}\n")
    usage()
    sys.exit(status)


def parse_cmd_line():
    """
    Parses the command line options looking for a given align
    indicator or a flag to specify the type of align that
    should be performed.
    """
    global align_type, align_indicator, padding

    opts = []
    try:
        opts = getopt.getopt(sys.argv[1:], OPTS)[0]
    except getopt.error as reason:
        die_usage(EXIT_FAILURE, reason)
    for opt in opts:
        if opt[OPT] == OPT_INDICATOR:
            align_indicator = opt[VAL]
        if opt[OPT] == OPT_RIGHTMOST:
            align_type = ALIGN_RIGHTMOST
        if opt[OPT] == OPT_LEFTMOST:
            align_type = ALIGN_LEFTMOST
        if opt[OPT] == OPT_PADDING:
            padding = int(opt[VAL])


def main():
    parse_cmd_line()
    block = sys.stdin.readlines()
    block = align_block(block, align_indicator, align_type)
    for line in block:
        sys.stdout.write(line)


if __name__ == "__main__":
    main()
