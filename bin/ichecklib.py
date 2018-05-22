#!/usr/bin/env python
# Aid tools to identifier quality checker.
# Ichecklib 
# Marcos Nascimento, 2018

import os
import sys
import commands
import json
import nltk
import unidecode
import yaml
import codecs
import ast
import re
from fileinput import filename

try:
    sys.path.append('/usr/local/bin/nltk/')
    from nltk.corpus import stopwords
    from nltk import RegexpTokenizer
except ImportError:
    print("tst quality checker needs nltk to work.")
    sys.exit(1)

# Settings
LANGUAGE = 'portuguese'

def get_studentidentifiers(filename):
    program = ast.parse(open(filename).read())  
    names = []
    for node in ast.walk(program):
        if isinstance(node, ast.Name) and not isinstance(node.ctx, ast.Load):
            names.append(node.id)
    return list(set(names))

def generate_problemvocabulary(problem_file):
    with codecs.open(problem_file, mode='r', encoding='utf-8') as fp:
        problem_file = yaml.load(fp)
    
    problem = problem_file["text"].lower()
    delimiters = ['\n', '_', '**', '$', '#', '##']
    
    for delimiter in delimiters:
        problem = problem.replace(delimiter, '')
    
    tokens = filter_stopwords(tokenize_text(problem), detect_language(problem))
    tokens_taged = nltk.pos_tag(tokens)
    vocabulary = transform_steams(tokens_taged)    
    return [unidecode.unidecode(word) for word in vocabulary]

def tokenize_text(problem):
    #Removing pontuaction and numbers
    is_wordwithrepeatedletters = lambda t: not re.compile(r'([a-z])\1+').match(t)
    is_fileextension = lambda t: not t.endswith('py')
    
    tokens = RegexpTokenizer(r'[a-zA-Z]\w+').tokenize(problem)
    tokens = filter(is_wordwithrepeatedletters, tokens)
    tokens = filter(is_fileextension, tokens)
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
    return vocabulary

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
    student_vocabulary = get_studentidentifiers(filename)
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
    student_vocabulary = get_studentidentifiers(filename)
    come_notproblemvocabulary = ichecking(problem_vocabulary, filename)
    return (len(student_vocabulary)-len(come_notproblemvocabulary))/float(len(student_vocabulary))

def save(message):
    type_ = 'accept'
    urlrequest.urlopen(url + type_, data=message)
    
if __name__ == '__main__':
  print("ichecking is a helper module for tst_qcheck commands")
