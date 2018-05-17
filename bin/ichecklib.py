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
    from nltk import wordpunct_tokenize
    from nltk.corpus import wordnet
    from nltk.corpus import stopwords
    from nltk.stem.lancaster import LancasterStemmer
    from nltk import RegexpTokenizer
except ImportError:
    print("tst quality checker needs nltk to work.")
    sys.exit(1)

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
    cont_ids = 0
    cont_idsfromspec = 0
    for i in ids:
        if(len(i) > 1):
            cont_ids += 1
            if i.lower() in problem_vocabulary:
                cont_idsfromspec += 1
    if cont_ids == cont_idsfromspec:
        return True
    return False

def is_idwithuderscore(id):
    return "_" in id.lower()

def check_idwithcamelcase(id, problem_vocabulary):
    #print id
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', id)
    s1 = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
    return check_idwithuderscore(s1, problem_vocabulary)

def is_idwithcamelcase(id):
    return (id != id.lower() and id != id.upper())

def check_idwithprep(id, problem_vocabulary):
    if '_of_' in id.lower():
        ids = id.lower().split('_of_')
        return check_idwithuderscore('_'.join(ids),problem_vocabulary)
    elif '_de_' in id.lower():
        ids = id.lower().split('_de_')
        return check_idwithuderscore('_'.join(ids),problem_vocabulary)
    return False

def is_idwithprep(id):
    return '_of_' in id.lower() or '_de_' in id.lower()
        
def ichecking(problem_vocabulary, filename):
    student_vocabulary = get_studentidentifiers(filename)
    come_notproblemvocabulary = []

    #https://stackoverflow.com/questions/3788870/how-to-check-if-a-word-is-an-english-word-with-python
    for id in student_vocabulary:
        is_fromproblem = False
        
        if id.lower() in problem_vocabulary:
            is_fromproblem = True
        elif is_idwithuderscore(id):
            is_fromproblem = check_idwithuderscore(id, problem_vocabulary)
        elif is_idwithcamelcase(id):
            is_fromproblem = check_idwithcamelcase(id, problem_vocabulary)
        elif is_idwithprep(id):
            is_fromproblem = check_idwithprep(id, problem_vocabulary)
        if not is_fromproblem:
            come_notproblemvocabulary.append(id)
    return come_notproblemvocabulary

def icheckscore(problem_vocabulary, filename):
    student_vocabulary = get_studentidentifiers(filename)
    come_notproblemvocabulary = ichecking(problem_vocabulary, filename)
    return (len(student_vocabulary)-len(come_notproblemvocabulary))/float(len(student_vocabulary))

def save(message):
    type_ = 'accept'
    urlrequest.urlopen(url + type_, data=message)
    
if __name__ == '__main__':
  print("ichecking is a helper module for tst_qcheck commands")
