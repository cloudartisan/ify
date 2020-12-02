#!/usr/bin/env python

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


TRUE = 1
FALSE = 0

WRAP_COLUMN = 80
SPACE = " "


def splitLine(line, column=WRAP_COLUMN):
	"""
	Splits a line, if necessary, into two lines.  The first line
	contains the result after wrapping.  The second line contains
	whatever is left over, regardless of the length.  Both lines
	are returned, regardless of the result of the split.
	"""
	if len(line) > column:
		splitPoint = line.rfind(" ", 0, column)
	else:
		splitPoint = -1

	if splitPoint > 0:
		# We have a point at which to split the line
		line1 = line[:splitPoint]
		line2 = line[splitPoint+1:]
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
	newBlock = block[:]
	for i in range(len(newBlock)):
		# Split the line for wrapping, cleaning the new line and
		# excess for buffering
		newLine, excess = splitLine(newBlock[i], column)
		newBlock[i] = newLine.rstrip()
		excess = excess.rstrip()
		# Make sure we don't lose any excess
		if excess:
			if i + 1 < len(newBlock):
				newBlock[i+1] = excess + " " + newBlock[i+1]
			else:
				newBlock.append(excess)
	return newBlock


def main():
	try:
		column = int(sys.argv[1])
	except IndexError:
		column = WRAP_COLUMN
	block = sys.stdin.readlines()
	wrappedBlock = wrapify(block, column)
	for line in wrappedBlock:
		print line


if __name__ == '__main__':
	main()
