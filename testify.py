#!/usr/bin/env python

"""
$Id: testify.py 1033 2003-04-30 13:29:08Z david $

A quick, dirty hack to perform automated regression testing of code.

I didn"t like the "regtest.py" example in Mark Lutz"s Programming Python.
So, I tried to invent a better wheel.

The aim is to have a regression tester that will provide enough
functionality to perform automated regression tests.
"""

import os, sys, string, getopt
from filecmp import cmp
from glob import glob
from time import time, ctime

# Program details
PROGRAM = os.path.basename(sys.argv[0])
VERSION = "$Revision: 1033 $"
USAGE   = """\
Usage: %s [options]
Options:
  -p <program>      The program to test
  -t <directory>    The directory containing the tests
  -V                Verbose reporting
  -v                Display the version
  -h                Display this help
""" % PROGRAM

# Exit statuses
EXIT_SUCCESS = 0
EXIT_FAILURE = 1

# Truth values
FALSE = 0
TRUE  = 1

# Command line options
OPT         = 0
VAL         = 1
OPTS        = "p:t:b:Vvh"
OPT_PROGRAM = "-p"
OPT_TESTS   = "-t"
OPT_VERBOSE = "-V"
OPT_VERSION = "-v"
OPT_HELP    = "-h"

# Test keys
TEST_NUM = "TestNum"
TEST_OUT = "TestOut"
TEST_ERR = "TestErr"

# Test details
Program     = None
TestPath    = None
Date        = ctime(time())
Tester      = os.environ["USER"]
Path        = os.getcwd()
Successes   = []
Failures    = []
TotalFailed = 0
TotalPassed = 0
TotalTested = 0

# Options
Verbose = FALSE


def version():
	"""
	Simply prints the version.
	"""
	versionNum = string.split(VERSION, ":")[1]
	versionNum = string.strip(versionNum)
	versionNum = versionNum[:-2]
	print "%s %s" % (PROGRAM, versionNum)


def die(reason=None, status=EXIT_FAILURE):
	"""
	Simply prints a reason, if any, for the program exiting and
	will exit with the supplied status.
	"""
	if reason:
		sys.stderr.write("%s: %s\n" % (sys.argv[0], reason))
	sys.exit(status)


def parseArgs():
	"""
	Extracts the command line arguments, such as the program to test and
	the location of its tests.
	"""
	global Program, TestPath, Verbose

	opts = []

	try:
		opts = getopt.getopt(sys.argv[1:], OPTS)[0]
	except getopt.error, reason:
		die(reason, EXIT_FAILURE)
	
	for opt in opts:
		if opt[OPT] == OPT_PROGRAM:
			Program   = opt[VAL]
		if opt[OPT] == OPT_TESTS:
			TestPath  = opt[VAL]
		if opt[OPT] == OPT_VERSION:
			version()
			sys.exit(0)
		if opt[OPT] == OPT_HELP:
			print USAGE
			sys.exit(0)
		if opt[OPT] == OPT_VERBOSE:
			Verbose   = TRUE
	
	if Program and TestPath:
		if not os.path.exists(Program):
			die("program not found: %s" % Program)
	
		if not os.path.exists(TestPath):
			die("tests not found: %s" % TestPath)
	else:
		die("no tests to perform")


def displayEnviron():
	"""
	Displays a summary of the test environment used.
	"""
	print "Tester    : %s" % Tester
	print "Date      : %s" % Date
	print "Path      : %s" % Path
	print "Program   : %s" % Program


def displayStats():
	"""
	Displays a summary of the successes and failures of the tests.
	"""
	print "Passed    : %d" % TotalPassed
	print "Failed    : %d" % TotalFailed
	print "Total     : %d" % TotalTested


def displayFailures():
	"""
	Displays the captured output of the failures to stderr.  We do
	this so that the tester will have sufficient information to debug
	any problems that may (will!) arise.
	"""
	for failedTest in Failures:
		testOut  = "%s.out" % failedTest
		testNOut = "%s.out.new" % failedTest
		print
		print "Failed Test: %s" % failedTest
		print
		print "Expected..."
		if os.path.exists(testOut):
			print open(testOut).read()
		print
		print "Found..."
		print open(testNOut).read()
		print


def getTests(testPath):
	"""
	Locates the test inputs and records their names.
	"""
	tests = glob(testPath + "/*.in")
	tests = map(os.path.splitext, tests)
	return tests


def rmTempFiles(test):
	"""
	Attempts to remove temporary files for a specific test, just so
	that the tester isn"t confused by old test files lying around.
	"""
	noutFile = "%s.out.new" % test
	if os.path.exists(noutFile):
		os.unlink(noutFile)


def initTests():
	"""
	For the moment, this function simply resets the counters, etc.
	Now that I have a batch testing tool that makes use of this module
	I have to provide the facility to initialise all this info before
	each round of tests.
	"""
	# FIXME FIXME FIXME
	# We shouldn't need to make use of globals... they're evil!
	global Successes, Failures, TotalFailed, TotalPassed, TotalTested
	Successes   = []
	Failures    = []
	TotalFailed = 0
	TotalPassed = 0
	TotalTested = 0


def runTests(program, tests):
	"""
	Manages the running of all the tests and the accumulation of both
	output and statistical information.
	"""
	global TotalTested

	initTests()
	for testName, testExt in tests:
		# Clean up old results
		rmTempFiles(testName)
		try:
			# Obtain the necessary arguments for this test
			args = open(testName + ".args").readline()[:-1]
		except:
			# No arguments exist for this test
			args = ""
		# Run the test and store the output (incl. errors)
		os.system("%s %s < %s.in > %s.out.new 2>&1" %
		         (program, args, testName, testName))
	TotalTested = len(tests)


def passed(test):
	"""
	Handles the passing of a test.
	"""
	global Successes, TotalPassed
	Successes.append(test)
	TotalPassed = TotalPassed + 1
	# No need for the temporary files
	rmTempFiles(test)


def failed(test):
	"""
	Handles the failure of a test.
	"""
	global Failures, TotalFailed
	Failures.append(test)
	TotalFailed = TotalFailed + 1


def chkTests(tests):
	"""
	Checks that output was produced for each of the tests and manages
	the testing of this output.
	"""
	global TotalPassed, TotalFailed

	for testName, testExt in tests:
		oldout = "%s.out" % testName
		newout = "%s.out.new" % testName
		if os.path.exists(newout):
			if not os.path.exists(oldout):
				# No previous test exists so,
				# by default, the test fails
				print "New test output: %s" % newout
				failed(testName)
			else:
				# A previous test result exists
				# that we must compare against
				if cmp(oldout, newout):
					passed(testName)
				else:
					failed(testName)
	return Successes, Failures


def main():
	# Initialisation
	parseArgs()
	
	# Get and perform the tests
	tests = getTests(TestPath)
	runTests(Program, tests)
	chkTests(tests)

	# Display the environment and results
	displayEnviron()
	displayStats()
	if Verbose:
		displayFailures()


if __name__ == "__main__":
	main()
