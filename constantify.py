#!/usr/bin/env python

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


isupper = lambda c: (len(c) == 1) and ('A' <= c <= 'Z')
isdigit = lambda d: (len(d) == 1) and ('0' <= d <= '9')


def constantify(val):
	"""
	Takes a value and converts it into a constant expression.
	The return value is the constant expression.
	"""
	# Clean unnecessary characters from the constant
	constantValue = val.strip()
	constantValue = constantValue.replace(' ', '_')
	constantValue = constantValue.replace('"', '')
	constantValue = constantValue.replace("'", '')
	# Capitalise and insert underscores where necessary
	prevChar = ''
	constantExpr = ''
	constantName = ''
	for currChar in constantValue:
		if isupper(currChar):
			# Are we changing case?
			if not isupper(prevChar) and not prevChar == '' and \
			   not currChar == '_':
				constantName = constantName + '_'
			# Are we following a digit?
			elif isdigit(prevChar)     and \
			     not isdigit(currChar) and \
			     not currChar == '_':
				constantName = constantName + '_'
		elif isdigit(currChar) and not isdigit(prevChar):
			# Changed from character to digit
			constantName = constantName + '_'
		constantName = constantName + currChar.upper()
		prevChar     = currChar
	# Build and produce the constant assignment
	constantExpr = "%s = '%s'\n" % (constantName, constantValue)
	return constantExpr


def main():
	line = sys.stdin.readline()
	while line:
		sys.stdout.write(constantify(line))
		line = sys.stdin.readline()


if __name__ == '__main__':
	main()
