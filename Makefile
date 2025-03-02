# Makefile for the ify suite
# Automates testing of all components

PYTHON = python3
TESTIFY = $(PYTHON) testify.py
COMPONENTS = alignify constantify wrapify

.PHONY: all test test-alignify test-constantify test-wrapify clean install uninstall

# Default target runs all tests
all: test

# Run tests for all components
test: $(addprefix test-,$(COMPONENTS))
	@echo "All tests completed."

# Test alignify component
test-alignify:
	@echo "Testing alignify..."
	$(TESTIFY) -p ./alignify.py -t tests/alignify

# Test constantify component
test-constantify:
	@echo "Testing constantify..."
	$(TESTIFY) -p ./constantify.py -t tests/constantify

# Test wrapify component
test-wrapify:
	@echo "Testing wrapify..."
	$(TESTIFY) -p ./wrapify.py -t tests/wrapify

# Run verbose tests for all components
verbose: 
	@echo "Testing alignify with verbose output..."
	$(TESTIFY) -p ./alignify.py -t tests/alignify -V
	@echo "Testing constantify with verbose output..."
	$(TESTIFY) -p ./constantify.py -t tests/constantify -V
	@echo "Testing wrapify with verbose output..."
	$(TESTIFY) -p ./wrapify.py -t tests/wrapify -V

# Clean up any temporary files
clean:
	@echo "Cleaning up temporary files..."
	find . -name "*.out.new" -delete
	find . -name "__pycache__" -type d -exec rm -rf {} +
	find . -name "*.pyc" -delete
	rm -rf build/ dist/ *.egg-info/

# Install the tools using setuptools
install:
	@echo "Installing ify tools..."
	$(PYTHON) -m pip install --user .

# Uninstall the tools
uninstall:
	@echo "Uninstalling ify tools..."
	$(PYTHON) -m pip uninstall -y ify