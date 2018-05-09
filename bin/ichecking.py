#!/usr/bin/env python
# Aid tools to identifier quality checker.
# Qchecklib 
# Marcos Nascimento, 2018

import os
import sys
import commands
import json
import nltk

from nltk import wordpunct_tokenize

try:
    sys.path.append('/usr/local/bin/radon/')
except ImportError:
    print("tst quality checker needs radon to work.")
    sys.exit(1)

def vocabulary(filename):
    with io.open(filename, encoding='utf-8') as f:
        tst_json = json.load(f)
    problem = tst_json["files"]["linger.yaml"]["data"]
    problem = problem.replace('\n', '')
    return tokenize_text(problem)

def tokenize_text(text):
    tokens = nltk.word_tokenize(text)
    words = [word.lower() for word in tokens]
    return words

def get_vocabulary(filenames):
    return vocabulary(filenames)

def save(message):
    type_ = 'accept'
    urlrequest.urlopen(url + type_, data=message)
    
if __name__ == '__main__':
  print("ichecking is a helper module for tst_qcheck commands")
