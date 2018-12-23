#!/usr/bin/env python
# Aid tools to identifiers quality checker.
# Iqchecklib 
# Marcos Nascimento, 2018

import os
import sys
import commands
import json
import nltk
import tstlib
import yaml
import codecs
import ast
import re
import __builtin__
import time
import datetime
from fileinput import filename

try:
    import unidecode
except ImportError:
    print("tst identifiers quality checker needs unidecode to work.")
    sys.exit(1)

try:
    sys.path.append('/usr/local/bin/nltk/')
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize
except ImportError:
    print("tst identifiers quality checker needs nltk to work.")
    sys.exit(1)

try:
   import urllib.request as urlrequest
except ImportError:
   import urllib as urlrequest

#Settings
LANGUAGE = 'portuguese'

def is_builtinfunction(name):
    try:
        getattr(__builtin__, name)
    except AttributeError:
        if AttributeError:
            return False
    return True

def get_identifiers(filename):
    program = ast.parse(open(filename).read())  
    identifiers = []
    for node in ast.walk(program):
        if isinstance(node, ast.Name):
            if not is_builtinfunction(node.id):
                identifiers.append(node.id)
        elif isinstance(node, ast.FunctionDef):
            args = node.args.args
            for arg in args:
                if not is_builtinfunction(arg.id):
                    identifiers.append(arg.id)
    return list(set(identifiers))

def get_positiveidentifiers(reference_words, program_identifiers):
    positiveidentifiers = []

    for id in program_identifiers:
        is_positive = False
        
        if has_underscore(id):
            is_positive = check_idwithuderscore(id, reference_words)
            
        elif has_camelcase(id):
            is_positive = check_idwithcamelcase(id, reference_words)
               
        elif is_simple(id):
            is_positive = idqcheck(id.lower(), reference_words)
        
        if is_positive:
            positiveidentifiers.append(id)

    return positiveidentifiers

def get_negativeidentifiers(reference_words, program_identifiers):
    return iqcheck(reference_words, program_identifiers)

def extract_problemvocabulary(problemtext_filename):
    with codecs.open(problemtext_filename, mode='r', encoding='utf-8') as fp:
        problemtext_file = yaml.load(fp)
    
    problemtext = problemtext_file["text"].lower().replace('\n', ' ')
    delimiters = ['r$','%','*','**','$','#','##','_','(',')', '.','-se','`','`','<','>','/']
    
    for delimiter in delimiters:
        if delimiter in ('/','<','>'):
            problemtext = problemtext.replace(delimiter, ' ')
        else:
            problemtext = problemtext.replace(delimiter, '')
    
    tokens = filter_stopwords(tokenize_text(problemtext), detect_language(problemtext))
    tokens_taged = nltk.pos_tag(tokens)
    vocabulary = transform_steams(tokens_taged) 
    return vocabulary

def filter_stopwords(tokens, language):
    #Code borrowed. (c) 2013 Alejandro Nolla
    stop_words = set(stopwords.words(language))
    tokens_filtered = []
    for t in tokens:
        if t not in stop_words:
            tokens_filtered.append(t)
    return tokens_filtered

def tokenize_text(problemtext):
    #Removing pontuaction and numbers
    is_wordwithrepeatedletters = lambda t: not re.compile(r'([a-z])\1+').match(t)
    is_number = lambda t: not re.compile(r'([0-9])').match(t)
    is_wordfollowedbynumbers = lambda t: not re.compile(r'([a-z]+[0-9]+)').match(t)
    is_fileextension = lambda t: not t.endswith('py')
    is_shortword = lambda t: not len(t) <= 2
    is_meaningless = lambda t: not t in ('python','programa','voce','usuario','obs')
    is_htmlformat = lambda t: not re.compile(r'(/[a-z])').match(t)
    
    filters = [is_wordwithrepeatedletters, is_number, is_wordfollowedbynumbers, is_fileextension, is_shortword, is_meaningless, is_htmlformat]

    tokens = word_tokenize(problemtext)
    tokens = [unidecode.unidecode(token) for token in tokens]
    
    for fun in filters:
        tokens = filter(fun, tokens)

    return list(set(tokens))

def detect_language(text):
    #Code borrowed. (c) 2013 Alejandro Nolla
    ratios = calculate_languagesratios(text)
    most_ratedlanguage = max(ratios, key=ratios.get)
    return most_ratedlanguage

def calculate_languagesratios(text):
    #Code borrowed. (c) 2013 Alejandro Nolla
    languages_ratios = {}
    words = tokenize_text(text)
    
    for language in stopwords.fileids():
        stopwords_set = set(stopwords.words(language))
        words_set = set(words)
        common_elements = words_set.intersection(stopwords_set)
        languages_ratios[language] = len(common_elements) # language "score"
    return languages_ratios

def transform_steams(tokens_taged):
    stemmer = nltk.stem.RSLPStemmer()
    is_not_noun = lambda pos: pos[:2] not in ('NNP','NN') #('VB','VBP','VBG','VBD','VBZ')
    is_noun = lambda pos: pos[:2] in ('NNP','NN')
    vocabulary = []
    
    for (word, pos) in tokens_taged:
        if is_not_noun(pos):
            #Strip affixes from the token and return the stem.
            vocabulary.append(stemmer.stem(word))
        elif is_noun(pos):
            vocabulary.append(word)
    return list(set(vocabulary))

def has_underscore(id):
    return "_" in id.lower()

def check_idwithuderscore(idwithuderscore, reference_words):
    terms = idwithuderscore.split('_')
    terms = filter_stopwords(terms, LANGUAGE)

    positiveterms = 0
    for term in terms:
        if idqcheck(term.lower(), reference_words):
            positiveterms += 1
    if positiveterms >= 1:
        return True
    return False

def has_camelcase(id):
    return (id != id.lower() and id != id.upper())
    
def check_idwithcamelcase(id, reference_words):
    uppercase_tounderscore = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', id)
    lowercase_tounderscore = re.sub('([a-z0-9])([A-Z])', r'\1_\2',
                                     uppercase_tounderscore)
    return check_idwithuderscore(lowercase_tounderscore, reference_words)

def is_simple(id):
    return id == id.lower() 

def idqcheck(id, reference_words):
    stemmer = nltk.stem.RSLPStemmer()
    
    if id in reference_words:
        return True
    
    elif stemmer.stem(id) in reference_words:
        return True
    
    elif id in [stemmer.stem(word) for word in reference_words]:
        return True
    
    elif stemmer.stem(id) in [stemmer.stem(word) for word in reference_words]:
        return True 
    
    return False

def iqcheck(reference_words, program_identifiers):
    negativeidentifiers = []

    for id in program_identifiers:
        is_positive = False
        
        if has_underscore(id):
            is_positive = check_idwithuderscore(id, reference_words)
            
        elif has_camelcase(id):
            is_positive = check_idwithcamelcase(id, reference_words)
               
        elif is_simple(id):
            is_positive = idqcheck(id.lower(), reference_words)
        
        if not is_positive:
            negativeidentifiers.append(id)
            
    return negativeidentifiers
 
def iqcheckscore(reference_words, program_identifiers):
    negativeidentifiers = iqcheck(reference_words, program_identifiers)    
    return round((len(program_identifiers)-len(negativeidentifiers))/float(len(program_identifiers)), 2)

def save(message):
    url = 'https://us-central1-qichecklog.cloudfunctions.net/logit?accept=%s'
    message["timestamp"] = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    message = json.dumps(tstlib.data2json(message))
    urlrequest.urlopen(url % message)

if __name__ == '__main__':
  print("iqchecklib is a helper module for tst_iqcheck commands")