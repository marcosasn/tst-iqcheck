# IQCHECK

IQCHECK is a tst custom command to check student's solution code identifiers quality to a given problem. 

It is based on a well-known gold standard recommended in a book and also adopted by some software engineering literature initiatives towards improving the identifiers quality. Also, it is based on a previously developed tool: qcheck.

## License

This software is licensed under the terms of the AGPL 3.0 license. Please read the LICENSE file.

## Documentation

### Usage 

```
tst qcheck [-h] [-m METRICS] [-f FEEDBACK] [-p PROF]
           [-o {human,json}]
           [filename]

Check program identifiers quality written Python through static code analysis.

positional arguments:
  filename

optional arguments:
  -h, --help,        show this help message and exit
  -m METRICS,        get values of cc, header, lloc, pep8, vhalstead and icheckscore
  -f FEEDBACK,       present warning messages referring to identifiers
  -p PROF,           get values of cc, header, lloc, pep8, vhalstead and icheckscore referring to a given pattern or file(s)
  -s SET,            set reference code
  -o {human,json},   set output format
```

### Messages

IQCHECK produces warning messages that give hints about **program identifiers** (programming solution identifiers). These warning messages are based on the similarity between the identifiers obtained from student program and the words extracted from problem specification text.

### Example
```
$ tst qcheck code.py
# code.py

**2 Warning(s)** 

### Identifiers names
- *x* Does not appear to be a suitable name. You should use words from the programming assignment description.
- *y* Does not appear to be a suitable name. You should use words from the programming assignment description.
```
In this sample execution, there are two identifiers name warnings. 

The identifiers name warnings suggest renaming the identifiers "x" and "y" because they appear not to be suitable names.

## Dependencies

This script is used as a TST custom command. TST must be installed in order to IQCHECK work properly. 
IQCHECK also depends on:
 - radon
 - NLTK
 - cc
 - pycodestyle
  
Radon (https://pypi.python.org/pypi/radon) and NLTK (https://pypi.python.org/pypi/nltk) must be installed in your environment. Cc and Pycodestyle will be downloaded from public repositories during IQCHECK installation.

## Installation

IQCHECK must be installed using the command below. It uses an existing TST configured environment.  

### Latest release

To install the latest stable release, run the following command.

$ bash -c "$(curl -q -sSL http://bit.ly/tst-iqcheck-install)"

### Development pre-release
