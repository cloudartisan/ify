#!/usr/bin/env python3

"""
$Id: constantify.py 1303 2003-07-02 13:40:31Z david $

A simply utility that reads variables and strings from stdin
and produces constant assignments on stdout.  This tool is
especially useful when cleaning up hardcoded strings.

Examples:
	1.
	[david@ws5 tmp]$ ./constantify.py 
	'HardcodedString'
	HARDCODED_STRING = 'HardcodedString'

	2.
	[david@ws5 tmp]$ ./constantify.py < strings > constants
"""

import sys


def is_upper(c):
    return (len(c) == 1) and ('A' <= c <= 'Z')

def is_digit(d):
    return (len(d) == 1) and ('0' <= d <= '9')


def constantify(val):
    """
    Takes a value and converts it into a constant expression.
    The return value is the constant expression.
    """
    # Clean unnecessary characters from the constant
    constant_value = val.strip()
    constant_value = constant_value.replace(' ', '_')
    constant_value = constant_value.replace('"', '')
    constant_value = constant_value.replace("'", '')
    # Capitalise and insert underscores where necessary
    prev_char = ''
    constant_expr = ''
    constant_name = ''
    for curr_char in constant_value:
        if is_upper(curr_char):
            # Are we changing case?
            if not is_upper(prev_char) and prev_char != '' and curr_char != '_':
                constant_name = constant_name + '_'
            # Are we following a digit?
            elif is_digit(prev_char) and not is_digit(curr_char) and curr_char != '_':
                constant_name = constant_name + '_'
        elif is_digit(curr_char) and not is_digit(prev_char):
            # Changed from character to digit
            constant_name = constant_name + '_'
        constant_name = constant_name + curr_char.upper()
        prev_char = curr_char
    # Build and produce the constant assignment
    constant_expr = f"{constant_name} = '{constant_value}'\n"
    return constant_expr


def main():
    line = sys.stdin.readline()
    while line:
        sys.stdout.write(constantify(line))
        line = sys.stdin.readline()


if __name__ == '__main__':
    main()
