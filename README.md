# QCHECK

QCHECK is a tst custom command to check student's solution code quality to a given problem. 

It is based on well-known static metrics that help to evaluate software maintainability.
 - lloc: Logical lines of code
 - cc: McCabe cyclomatic complexity
 - vhalstead: Halstead volume
 - pep8: Adherence to Python coding standards (PEP8)


## License

This software is licensed under the terms of the AGPL 3.0
license. Please read the LICENSE file.


## Documentation

### Usage 

```
tst qcheck [-h] [-m METRICS] [-f FEEDBACK] [-p PROF]
           [-o {human,json}]
           [filename]

Check python code static quality metrics.

positional arguments:
  filename

optional arguments:
  -h, --help,        show this help message and exit
  -m METRICS,        get values of cc, header, lloc, pep8, vhalstead
  -f FEEDBACK,       present warning messages referring to static quality metrics
  -p PROF,           get values of cc, header, lloc, pep8, vhalstead referring to a given pattern or file(s)
  -s SET,            set reference code
  -o {human,json},   set output format
```

### Messages

QCHECK produces warning messages that give hints about **code** (programming solution to the problem) and **style** (Python coding standards).

Warning messages about code quality are based on well-known quality software metrics and other requirements. Style hints are based on PEP8 - Python community canonical style guide.

### Example
```
$ tst qcheck code.py
# code.py

**2 Warning(s)** 

### Code
- There are few lines on program header.
### Style
- 2:1: E265 block comment should start with '# '
```
In this sample execution there is a code warning and a style warning. 

The code warning suggests to add more lines to the program's header. 

The style warning points a problem in line 2, column 1 (*[line]:[column]*).

## Dependencies

This script is used as a TST custom command. TST must be installed in order to QCHECK work properly. 
QCHECK also depends on:
 - radon
 - cc
 - pycodestyle
  
Radon must be installed in your environment (https://pypi.python.org/pypi/radon). Cc and Pycodestyle will be downloaded from public repositories during QCHECK installation.


## Installation

QCHECK must be installed using the command below. It uses an existing TST configured environment.  

### Latest release

To install the latest stable release, run the following command.

$ bash -c "$(curl -q -sSL http://bit.ly/qcheck-install)"


### Development pre-release
