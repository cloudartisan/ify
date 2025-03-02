#!/usr/bin/env python3

"""
$Id: testify.py 1033 2003-04-30 13:29:08Z david $

A quick, dirty hack to perform automated regression testing of code.

I didn't like the "regtest.py" example in Mark Lutz's Programming Python.
So, I tried to invent a better wheel.

The aim is to have a regression tester that will provide enough
functionality to perform automated regression tests.
"""

import os
import sys
import getopt
from filecmp import cmp
from glob import glob
from time import time, ctime

# Program details
PROGRAM = os.path.basename(sys.argv[0])
VERSION = "$Revision: 1033 $"
USAGE   = f"""\
Usage: {PROGRAM} [options]
Options:
  -p <program>      The program to test
  -t <directory>    The directory containing the tests
  -V                Verbose reporting
  -v                Display the version
  -h                Display this help
"""

# Exit statuses
EXIT_SUCCESS = 0
EXIT_FAILURE = 1

# Truth values
FALSE = False
TRUE  = True

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
program = None
test_path = None
date = ctime(time())
tester = os.environ["USER"]
path = os.getcwd()
successes = []
failures = []
total_failed = 0
total_passed = 0
total_tested = 0

# Options
verbose = FALSE


def version():
	"""
	Simply prints the version.
	"""
	versionNum = VERSION.split(":")[1]
	versionNum = versionNum.strip()
	versionNum = versionNum[:-2]
	print(f"{PROGRAM} {versionNum}")


def die(reason=None, status=EXIT_FAILURE):
	"""
	Simply prints a reason, if any, for the program exiting and
	will exit with the supplied status.
	"""
	if reason:
		sys.stderr.write(f"{sys.argv[0]}: {reason}\n")
	sys.exit(status)


def parse_args():
    """
    Extracts the command line arguments, such as the program to test and
    the location of its tests.
    """
    global program, test_path, verbose

    opts = []

    try:
        opts = getopt.getopt(sys.argv[1:], OPTS)[0]
    except getopt.error as reason:
        die(reason, EXIT_FAILURE)
    
    for opt in opts:
        if opt[OPT] == OPT_PROGRAM:
            program = opt[VAL]
        if opt[OPT] == OPT_TESTS:
            test_path = opt[VAL]
        if opt[OPT] == OPT_VERSION:
            version()
            sys.exit(0)
        if opt[OPT] == OPT_HELP:
            print(USAGE)
            sys.exit(0)
        if opt[OPT] == OPT_VERBOSE:
            verbose = TRUE
    
    if program and test_path:
        if not os.path.exists(program):
            die(f"program not found: {program}")
    
        if not os.path.exists(test_path):
            die(f"tests not found: {test_path}")
    else:
        die("no tests to perform")


def display_environ():
    """
    Displays a summary of the test environment used.
    """
    print(f"Tester    : {tester}")
    print(f"Date      : {date}")
    print(f"Path      : {path}")
    print(f"Program   : {program}")


def display_stats():
    """
    Displays a summary of the successes and failures of the tests.
    """
    print(f"Passed    : {total_passed}")
    print(f"Failed    : {total_failed}")
    print(f"Total     : {total_tested}")


def display_failures():
    """
    Displays the captured output of the failures to stderr.  We do
    this so that the tester will have sufficient information to debug
    any problems that may (will!) arise.
    """
    for failed_test in failures:
        test_out = f"{failed_test}.out"
        test_new_out = f"{failed_test}.out.new"
        print()
        print(f"Failed Test: {failed_test}")
        print()
        print("Expected...")
        if os.path.exists(test_out):
            with open(test_out, 'r') as f:
                print(f.read())
        print()
        print("Found...")
        with open(test_new_out, 'r') as f:
            print(f.read())
        print()


def get_tests(test_path):
    """
    Locates the test inputs and records their names.
    """
    tests = glob(test_path + "/*.in")
    tests = list(map(os.path.splitext, tests))
    return tests


def rm_temp_files(test):
    """
    Attempts to remove temporary files for a specific test, just so
    that the tester isn't confused by old test files lying around.
    """
    new_out_file = f"{test}.out.new"
    if os.path.exists(new_out_file):
        os.unlink(new_out_file)


def init_tests():
    """
    For the moment, this function simply resets the counters, etc.
    Now that I have a batch testing tool that makes use of this module
    I have to provide the facility to initialise all this info before
    each round of tests.
    """
    # FIXME FIXME FIXME
    # We shouldn't need to make use of globals... they're evil!
    global successes, failures, total_failed, total_passed, total_tested
    successes = []
    failures = []
    total_failed = 0
    total_passed = 0
    total_tested = 0


def run_tests(program_path, tests):
    """
    Manages the running of all the tests and the accumulation of both
    output and statistical information.
    """
    global total_tested

    init_tests()
    for test_name, test_ext in tests:
        # Clean up old results
        rm_temp_files(test_name)
        try:
            # Obtain the necessary arguments for this test
            with open(test_name + ".args", 'r') as f:
                args = f.readline()[:-1]
        except Exception:
            # No arguments exist for this test
            args = ""
        # Run the test and store the output (incl. errors)
        os.system(f"{program_path} {args} < {test_name}.in > {test_name}.out.new 2>&1")
    total_tested = len(tests)


def passed(test):
    """
    Handles the passing of a test.
    """
    global successes, total_passed
    successes.append(test)
    total_passed += 1
    # No need for the temporary files
    rm_temp_files(test)


def failed(test):
    """
    Handles the failure of a test.
    """
    global failures, total_failed
    failures.append(test)
    total_failed += 1


def check_tests(tests):
    """
    Checks that output was produced for each of the tests and manages
    the testing of this output.
    """
    global total_passed, total_failed

    for test_name, test_ext in tests:
        old_out = f"{test_name}.out"
        new_out = f"{test_name}.out.new"
        if os.path.exists(new_out):
            if not os.path.exists(old_out):
                # No previous test exists so,
                # by default, the test fails
                print(f"New test output: {new_out}")
                failed(test_name)
            else:
                # A previous test result exists
                # that we must compare against
                if cmp(old_out, new_out):
                    passed(test_name)
                else:
                    failed(test_name)
    return successes, failures


def main():
    # Initialization
    parse_args()
    
    # Get and perform the tests
    tests = get_tests(test_path)
    run_tests(program, tests)
    check_tests(tests)

    # Display the environment and results
    display_environ()
    display_stats()
    if verbose:
        display_failures()


if __name__ == "__main__":
    main()