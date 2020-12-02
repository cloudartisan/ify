#!/usr/bin/env python

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


import sys, string, getopt


# Possible exit statuses
EXIT_SUCCESS = 0
EXIT_FAILURE = 1

# Supported short command line options
OPT_INDICATOR = "-i"
OPT_RIGHTMOST = "-r"
OPT_LEFTMOST  = "-l"
OPT_PADDING   = "-p"
OPTS          = "i:p:rl"

# Option indexes
OPT = 0
VAL = 1

# Alignment types
ALIGN_RIGHTMOST = "R"
ALIGN_LEFTMOST  = "L"

# Defaults
ALIGN_INDICATOR = "="
ALIGN_TYPE      = ALIGN_RIGHTMOST

# Globals
AlignType      = ALIGN_TYPE
AlignIndicator = ALIGN_INDICATOR
Padding        = 0


def getAlignIndex(block, alignStr=ALIGN_INDICATOR, alignType=ALIGN_TYPE):
	"""
	Accepts a block of text and returns the length at which to
	align the block.  Of course, this length is dependent upon
	the location of the alignment indicator.
	"""
	alignIndex = -1

	for line in block:
		lval = ""
		# Skip lines that do not contain an alignment indicator
		if line.find(alignStr) == -1:
			continue
		try:
			lval = line.split(alignStr)[0]
		except ValueError:
			continue
		lvalLen = len(lval)
		# Length of align is dependent on alignment type
		if alignIndex == -1:
			alignIndex = lvalLen
		elif alignType == ALIGN_RIGHTMOST:
			alignIndex = max(lvalLen, alignIndex)
		elif alignType == ALIGN_LEFTMOST:
			alignIndex = min(lvalLen, alignIndex)
	return alignIndex


def alignLine(line, alignIndex, alignStr=ALIGN_INDICATOR):
	"""
	Accepts a line of text, the alignment length, and the string with
	which to align the block.  Attempts to align the block of text.
	If an unexpected exception occurs, the original line is returned.
	Otherwise, the aligned block of text is returned.
	"""
	try:
		lval, rval = line.split(alignStr, 1)
		lval = lval.rstrip()
		diffLen = alignIndex - len(lval)
		lval = lval + (" " * diffLen) + (" " * Padding)
		result = "%s%s%s" % (lval, alignStr, rval)
	except:
		result = line
	return result


def alignBlock(block, alignStr=ALIGN_INDICATOR, alignType=ALIGN_TYPE):
	"""
	Accepts a block of text (a list of lines), the string with which
	to align the block, and the alignment type.  Returns the aligned
	block of text.
	"""
	# Determine the length at which to align the block
	alignIndex = getAlignIndex(block, alignStr, alignType)

	# Align the block now
	alignedBlock = []
	for line in block:
		if line.find(alignStr) == -1:
			alignedLine = line
		else:
			alignedLine = alignLine(line, alignIndex, alignStr)
		alignedBlock.append(alignedLine)
	return alignedBlock


def usage():
	"""
	Simply prints the usage information.
	"""
	print "Usage: %s [-i indicator] [-p padding] [-r|-l]" % sys.argv[0]


def dieUsage(status, reason=None):
	"""
	Prints the usage information and an optional error message.
	"""
	if reason:
		sys.stderr.write("Error: %s\n" % reason)
	usage()
	sys.exit(status)


def parseCmdLine():
	"""
	Parses the command line options looking for a given align
	indicator or a flag to specify the type of align that
	should be performed.
	"""
	global AlignType, AlignIndicator, Padding

	opts = []
	try:
		opts = getopt.getopt(sys.argv[1:], OPTS)[0]
	except getopt.error, reason:
		dieUsage(EXIT_FAILURE, reason)
	for opt in opts:
		if opt[OPT] == OPT_INDICATOR:
			AlignIndicator = opt[VAL]
		if opt[OPT] == OPT_RIGHTMOST:
			AlignType = ALIGN_RIGHTMOST
		if opt[OPT] == OPT_LEFTMOST:
			AlignType = ALIGN_LEFTMOST
		if opt[OPT] == OPT_PADDING:
			Padding = int(opt[VAL])


def main():
	parseCmdLine()
	block = sys.stdin.readlines()
	block = alignBlock(block, AlignIndicator, AlignType)
	for line in block:
		sys.stdout.write(line)


if __name__ == "__main__":
	main()
