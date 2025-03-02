```
$Id: README 998 2003-04-28 15:51:03Z david $
```

# ify 1.0

A collection of text processing utilities for code formatting and management.

## Utilities included

- **alignify**: Aligns text around a given alignment indicator (like = or :)
- **constantify**: Converts variables and strings into constant assignments
- **wrapify**: Wraps text at a given margin without breaking words
- **testify**: A regression testing tool used for the suite itself

## Installation

Install the commands to your user directory:

```
make install
```

Or install directly with pip:

```
python3 -m pip install --user .
```

## Usage examples

Align equals signs right-aligned:
```
alignify -r < code.py > aligned_code.py
```

Align 'and' keywords:
```
alignify -i and < code.py > aligned_code.py
```

Convert variable names to constants:
```
constantify < variables.txt > constants.py
```

Wrap text at 80 characters:
```
wrapify < longlines.txt > wrapped.txt
```

Wrap text at custom width (60 characters):
```
wrapify 60 < longlines.txt > wrapped.txt
```

## License

Copyright 2003 by David Taylor.  This software is published under the
GNU public licence version 2.0 or later.  Please read the file "LICENCE"
for more information.

David Taylor
david@cloudartisan.com