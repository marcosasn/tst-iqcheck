#!/usr/bin/env python
# Aid tools to identifier quality checker.
# Ichecklib 
# Marcos Nascimento, 2018

import os
import sys
import commands
import json
import nltk
import tstlib
import unidecode
import yaml
import codecs
import ast
import re
import __builtin__
from fileinput import filename

try:
    sys.path.append('/usr/local/bin/nltk/')
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize
except ImportError:
    print("tst quality checker needs nltk to work.")
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

def get_positives(problem_vocabulary, filename):
    student_vocabulary = list(set(get_studentidentifiers(filename)))
    came_fromproblem = []

    for id in student_vocabulary:
        is_fromproblem = False
        
        if has_underscore(id):
            is_fromproblem = check_idwithuderscore(id, problem_vocabulary)
            
        elif has_camelcase(id):
            is_fromproblem = check_idwithcamelcase(id, problem_vocabulary)
               
        elif is_simpleid(id):
            is_fromproblem = id_checking(id.lower(), problem_vocabulary)
        
        if is_fromproblem:
            came_fromproblem.append(id)

    return came_fromproblem

def get_negatives(problem_vocabulary, filename):
    return ichecking(problem_vocabulary, filename)

def get_studentidentifiers(filename):
    program = ast.parse(open(filename).read())  
    names = []
    for node in ast.walk(program):
        if isinstance(node, ast.Name):
            if not is_builtinfunction(node.id):
                names.append(node.id)
        elif isinstance(node, ast.FunctionDef):
            args = node.args.args
            for arg in args:
                if not is_builtinfunction(arg.id):
                    names.append(arg.id)
    return names

def generate_problemvocabulary(problem_file):
    with codecs.open(problem_file, mode='r', encoding='utf-8') as fp:
        problem_file = yaml.load(fp)
    
    problem = problem_file["text"].lower().replace('\n', ' ')
    delimiters = ['r$','%','*','**','$','#','##','_','(',')', '.','-se','`','`','<','>','/']
    
    for delimiter in delimiters:
        if delimiter in ('/','<','>'):
            problem = problem.replace(delimiter, ' ')
        else:
            problem = problem.replace(delimiter, '')
    
    tokens = filter_stopwords(tokenize_text(problem), detect_language(problem))
    tokens_taged = nltk.pos_tag(tokens)
    vocabulary = transform_steams(tokens_taged) 
    return vocabulary

def tokenize_text(problem):
    #Removing pontuaction and numbers
    is_wordwithrepeatedletters = lambda t: not re.compile(r'([a-z])\1+').match(t)
    is_number = lambda t: not re.compile(r'([0-9])').match(t)
    is_wordfollowedbynumbers = lambda t: not re.compile(r'([a-z]+[0-9]+)').match(t)
    is_fileextension = lambda t: not t.endswith('py')
    is_shortword = lambda t: not len(t) <= 2
    is_meaningless = lambda t: not t in ('python','programa','voce','usuario','obs')
    is_htmlformat = lambda t: not re.compile(r'(/[a-z])').match(t)
    
    filters = [is_wordwithrepeatedletters, is_number, is_wordfollowedbynumbers, is_fileextension, is_shortword, is_meaningless, is_htmlformat]

    tokens = word_tokenize(problem)
    tokens = [unidecode.unidecode(token) for token in tokens]
    
    for fun in filters:
        tokens = filter(fun, tokens)

    return list(set(tokens))
    
def filter_stopwords(tokens, language):
    #Code borrowed. (c) 2013 Alejandro Nolla
    stop_words = set(stopwords.words(language))
    tokens_filtered = []
    for t in tokens:
        if t not in stop_words:
            tokens_filtered.append(t)
    return tokens_filtered

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

def detect_language(text):
    #Code borrowed. (c) 2013 Alejandro Nolla
    ratios = calculate_languagesratios(text)
    most_ratedlanguage = max(ratios, key=ratios.get)
    return most_ratedlanguage

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

def check_idwithuderscore(id, problem_vocabulary):
    ids = id.split('_')
    ids = filter_stopwords(ids, LANGUAGE)

    count_idsfromproblem = 0
    for i in ids:
        if id_checking(i.lower(), problem_vocabulary):
            count_idsfromproblem += 1
    if count_idsfromproblem >= 1:
        return True
    return False

def has_underscore(id):
    return "_" in id.lower()

def check_idwithcamelcase(id, problem_vocabulary):
    uppercase_tounderscore = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', id)
    lowercase_tounderscore = re.sub('([a-z0-9])([A-Z])', r'\1_\2',
                                     uppercase_tounderscore)
    return check_idwithuderscore(lowercase_tounderscore, problem_vocabulary)

def has_camelcase(id):
    return (id != id.lower() and id != id.upper())

def is_simpleid(id):
    return id == id.lower() 

def id_checking(id, problem_vocabulary):
    stemmer = nltk.stem.RSLPStemmer()
    
    if id in problem_vocabulary:
        return True
    
    elif stemmer.stem(id) in problem_vocabulary:
        return True
    
    elif id in [stemmer.stem(word) for word in problem_vocabulary]:
        return True
    
    elif stemmer.stem(id) in [stemmer.stem(word) for word in problem_vocabulary]:
        return True 
    
    return False
        
def ichecking(problem_vocabulary, filename):
    student_vocabulary = list(set(get_studentidentifiers(filename)))
    came_notfromproblem = []

    for id in student_vocabulary:
        is_fromproblem = False
        
        if has_underscore(id):
            is_fromproblem = check_idwithuderscore(id, problem_vocabulary)
            
        elif has_camelcase(id):
            is_fromproblem = check_idwithcamelcase(id, problem_vocabulary)
               
        elif is_simpleid(id):
            is_fromproblem = id_checking(id.lower(), problem_vocabulary)
        
        if not is_fromproblem:
            came_notfromproblem.append(id)

    return came_notfromproblem

def icheckscore(problem_vocabulary, filename):
    student_vocabulary = list(set(get_studentidentifiers(filename)))
    come_notproblemvocabulary = ichecking(problem_vocabulary, filename)
    
    return round((len(student_vocabulary)-len(come_notproblemvocabulary))/float(len(student_vocabulary)), 2) 

def save(message):
    url = 'https://us-central1-qichecklog.cloudfunctions.net/logit?accept=%s'
    message = json.dumps(message)
    urlrequest.urlopen(url % message)

    try:
        os.system('tst commit')
    except IOError:
        print("Usage: type tst commit to send your code")
        sys.exit(1)
    
if __name__ == '__main__':
  print("ichecking is a helper module for tst_qcheck commands")
