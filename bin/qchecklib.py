#!/usr/bin/env python
# Aid tools to quality checker.
# Qchecklib 
# Eliane Araujo, 2016

import os
import sys
import commands
import json

try:
    from cc import measure_complexity
except ImportError:
    print("tst quality checker needs cc.py to work.")
    sys.exit(1)

try:
    sys.path.append('/usr/local/bin/radon/')
    from radon.raw import *
    from radon.complexity import *
    from radon.metrics import *
except ImportError:
    print("tst quality checker needs radon to work.")
    sys.exit(1)

try:
   import urllib.request as urlrequest
except ImportError:
   import urllib as urlrequest

url = 'http://qchecklog.appspot.com/api/action/'

def four_metrics(program_name):    
    return "%s %s %s %s" % ( lloc(program_name), cc(program_name), vhalstead(program_name), pep8(program_name)["count"])

def pep8count(program):
    return int(pep8(program)[0])

def pep8(program):
    result = []
    cmd = 'pycodestyle.py --select=E --count ' + program
    try:
        pep_errors = commands.getoutput(cmd)
    except ImportError:
        print("tst quality checker needs pycodestyle.py to work.")
        sys.exit(1)
        
    if pep_errors:
        for error in pep_errors.splitlines():
            if error.isdigit():
                result.insert(0, int(error))
                break
            #remove filename from message.
            #Example:
            #reference.py:15:16: E225 missing whitespace around operator
            result.append( error[error.find(":") + 1:] )
    else:
        result = [0]    
    return result

def header_lines(filename):
    # Count header's lines   
    # Consider "coding" and "env" as header
    program = open(filename, 'r')
    code = program.read()
 
    counter = 0
    codelines = code.split("\n")
    while codelines[counter].startswith("#"):
        counter += 1

    program.close()
    return counter

def vhalstead(filename):  
    return halstead_metrics("vol", filename)
    
def halstead_metrics(options, filename):  
    #It may be used another options
    program = open(filename, 'r')
    code = program.read()

    if options == 'vol':
        h = h_visit(code).volume
    else:
        h = h_visit(code)
    
    program.close()
    return round(h, 2)

def cc(filename):    
    # Radon complexity method only applies to programs containing classes or functions.
    # Using another API to other cases.
    program = open(filename, 'r')
    code = program.read()
    try:
        # Use radon
        visitor = cc_visit(code)
        if len(visitor) <= 0:
            # Doesn't have functions or classes. 
            # Use cc.py
            stats = measure_complexity(code)
            cc = stats.complexity
        else:
            cc = 0
            for i in range( len(visitor) ):
                cc += visitor[i].complexity
        
    except Exception as e:
        # Failed
        print("qcheck: unable to get cc")
        cc = 0
    program.close()
    return cc

def lloc(filename):
    program = open(filename, 'r')
    code = program.read()
    lines = raw_metrics(code)[1]
    program.close()
    return lines
    
def raw_metrics(code):
    return analyze(code)

def save(message):
    type_ = 'accept'
    urlrequest.urlopen(url + type_, data=message)
    
    
if __name__ == '__main__':
  print("qchecklib is a helper module for tst_qcheck commands")
