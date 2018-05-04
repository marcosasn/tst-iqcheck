#!/usr/bin/env python
# coding: utf-8
# 
# TST-Online command line quality checker. Based on code metrics used to evaluate software maintainability.
# lloc: Logical Lines of code
# cc: McCabe cyclomatic complexity
# vhalstead: Halstead volume
# pep8: Adherence to Python coding standards (PEP8)
#
# Eliane Araujo, 2016-2017
#

import os
import sys
import json
import codecs
import glob
import argparse

import tstlib
import qchecklib
from fileinput import filename

import nltk
from nltk import wordpunct_tokenize

# Feedback Messages
SHORTHEADER = "Your program header is too short."
HIGHLLOC = "Your program has too many lines of code."
HIGHCC = "Your program has too many decision points."
HIGHVHALSTEAD = "Your program has too many operations (Example: +,-,==, etc)."
NOREFERENCE = "There are no reference values."
NOWARNINGS = "No warnings. Congratulations!"

# Output Settings
COLNUMBERWIDTH = 5
COLTEXTWIDTH = 25
QCHECKFILE = "qcheck.json"
TSTFILE = ".tst/tst.json"
TSTDIR = os.path.expanduser("~/.tst/")
TSTCONFIG = os.path.expanduser(TSTDIR + "config.json")

LBLUE = '\033[1;34m'
LGREEN = '\033[1;32m'
LCYAN = '\033[1;36m'
RESET = '\033[0m'
    
def get_refmetrics(): 
    qcheckjson = read_qcheckjson(exit=True)
    if qcheckjson.get("quality"):
        return qcheckjson.get("quality")[0]
    else:
        return {}
    
def get_quality_metrics( raw_metrics ): 
    ref_metrics = get_refmetrics()
    metrics = {}
    # Ratio metrics
    if ref_metrics:
        metrics["lloc"] = float(raw_metrics.get("lloc")) / float(ref_metrics.get("lloc"))
        # If metric value == 0?
        if int(ref_metrics.get("vhalstead")) != 0:
            metrics["vhalstead"] = float(raw_metrics.get("vhalstead")) / float(ref_metrics.get("vhalstead"))
        elif int(raw_metrics.get("vhalstead")) == 0 and int(ref_metrics.get("vhalstead")) == 0:
            # In this case, users metric and ref_metrics are 0, 
            # Manually set value to 0
            metrics["vhalstead"] = 0.0
        else:
            # In this case, users metric value is greater than 0, must provide fb.
            # Manually set value above threshold
            metrics["vhalstead"] = 1.3
        
        if int(ref_metrics.get("cc")) != 0:
            metrics["cc"] = float(raw_metrics.get("cc")) / float(ref_metrics.get("cc"))
        elif int(raw_metrics.get("vhalstead")) == 0 and int(ref_metrics.get("vhalstead")) == 0:
            # In this case, users metric and ref_metrics are 0, 
            # Manually set value to 0
            metrics["cc"] = 0.0
        else:
            # In this case, users metric value is greater than 0, must provide fb.
            # Manually set value above threshold
            metrics["cc"] = 1.3
    
    return metrics


def check_header( lines ):
    #Ad hoc number of lines to assess header quality
    return True if lines > 2 else False 

def quality_report( raw_metrics ):
    """
    For each rmetric (rlloc, rcc, rh, rpep8) assign a feedback message.
    The threashold to show them is 20%.
    """
    quality_metrics = get_quality_metrics( raw_metrics )    
    report = {}
    if not quality_metrics:
        report["message"] = NOREFERENCE

    #RCC
    report["cc"] = [raw_metrics.get("cc")]
    if quality_metrics.get("cc") > 1.2:
        report["cc"].append( HIGHCC )
    #RLLOC
    report["lloc"] = [raw_metrics.get("lloc")]
    if quality_metrics.get("lloc") > 1.2:
        report["lloc"].append( HIGHLLOC )
    #RH
    report["vhalstead"] = [raw_metrics.get("vhalstead")]
    if quality_metrics.get("vhalstead") > 1.2:
        report["vhalstead"].append( HIGHVHALSTEAD )
    #Rpep8
    if raw_metrics.get("pep8"):
        report["pep8"] = raw_metrics.get("pep8")
    #Header
    report["header"] = [raw_metrics.get("header")]    
    if not check_header(raw_metrics.get("header")):
        report["header"].append( SHORTHEADER )
    return report

def get_metrics(filename):
    results = {
        "lloc": qchecklib.lloc(filename),
        "cc": qchecklib.cc(filename),
        "vhalstead": qchecklib.vhalstead(filename),
        "pep8": qchecklib.pep8(filename),
        "header": qchecklib.header_lines(filename)
    }
    return results

def get_rawmetrics(filename):
    results = {
        "lloc": qchecklib.lloc(filename),
        "cc": qchecklib.cc(filename),
        "vhalstead": qchecklib.vhalstead(filename),
        "pep8": qchecklib.pep8count(filename),
        "header": qchecklib.header_lines(filename)
    }  
    return results

import io
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

import json
def get_vocabulary(filenames):
    return vocabulary(filenames)

def get_username():
    configjson = read_tstconfig(exit=True)
    if configjson.get("user"):
        return configjson.get("user")
    else:
        return ''

def get_activityid():
    tstjson = read_tstjson(exit=True)
    if tstjson.get("iid"):
        return tstjson.get("iid")
    else:
        return '0'
    
def get_logdata(filenames, output):
    content = { "filename": filenames, "report": output }
    content["iid"] = get_activityid()
    content["user"] = get_username()
    return tstlib.data2json(content)
    
def pack_logfeedback(results):
    style, code = 0, 0
    codemetrics = ["cc", "header", "lloc", "vhalstead"]
    for metric, message in results.items():
        if len(message) > 1:
            if metric in codemetrics:
                code += 1
            else:
                style += message[0]    
    report = { "stylewarning": style, "codewarning": code,  "feedback": results }
    
    return report

def pack_markdownfeedback(filename, results):
    codeline = "### Code\n"
    styleline = "### Style\n"
    codewarnings, stylewarnings = 0, 0
    
    if not results:
        return ""
    
    #Header
    if results.get("header") and len(results.get("header")) > 1:
        codeline+= "- %s\n" % results.get("header")[1]
        codewarnings += 1
    #RCC
    if results.get("cc") and len(results.get("cc")) > 1:
        codeline+= "- %s\n" % results.get("cc")[1]
        codewarnings += 1
    #LLOC
    if results.get("lloc") and len(results.get("lloc")) > 1:
        codeline+=  "- %s\n" % results.get("lloc")[1]
        codewarnings += 1
    #RVHALSTEAD
    if results.get("vhalstead") and len(results.get("vhalstead")) > 1:
        codeline+=  "- %s\n" % results.get("vhalstead")[1]
        codewarnings += 1
    #RPEP8
    if results.get("pep8") and len(results.get("pep8")) > 1:
        for i in range(1, len(results.get("pep8"))):
            styleline+=  "- %s\n" % results.get("pep8")[i]
            stylewarnings += 1
    
    if stylewarnings or codewarnings:
        header = LBLUE + "# %s\n\n" % filename
        report = LCYAN + "**%d Warning(s)** \n\n" % (stylewarnings + codewarnings) + RESET
        messages = codeline if codewarnings else ""
        messages += styleline if stylewarnings else ""
        text = header + report + messages[:-1]
    else:
        text = LCYAN + "** %s **" % NOWARNINGS + RESET
    
    return text

def pack_readablefeedback(results):
    line = ""
    if not results:
        return line
    #Message
    if results.get("message") and len(results.get("message")) > 1:
        line+= "%s\n" % results.get("message")
    #Header
    if results.get("header") and len(results.get("header")) > 1:
        line+= "%s\n" % results.get("header")[1]
    #RCC
    if results.get("cc") and len(results.get("cc")) > 1:
        line+= "%s\n" % results.get("cc")[1]
    #LLOC
    if results.get("lloc") and len(results.get("lloc")) > 1:
        line+=  "%s\n" % results.get("lloc")[1]
    #RVHALSTEAD
    if results.get("vhalstead") and len(results.get("vhalstead")) > 1:
        line+=  "%s\n" % results.get("vhalstead")[1]
    #RPEP8
    if results.get("pep8") and len(results.get("pep8")) > 1:
        for i in range(1, len(results.get("pep8"))):
            line+=  "%s\n" % results.get("pep8")[i]
    
    return line[:-1]

def pack_readablemetrics(results):
    
    line = ""
    if not results:
        return line
    #RCC
    if results.get("cc") is not None:
        line += '{0:>{width}}'.format(results.get("cc"), width = COLNUMBERWIDTH)
    #Header
    if results.get("header") is not None:
        line += '{0:>{width}}'.format(results.get("header"), width = COLNUMBERWIDTH)
    #LLOC
    if results.get("lloc") is not None:
        line += '{0:>{width}}'.format(results.get("lloc"), width = COLNUMBERWIDTH)
    #RPEP8
    if results.get("pep8") is not None:
        line += '{0:>{width}}'.format(results.get("pep8"), width = COLNUMBERWIDTH)
    #RVHALSTEAD
    if results.get("vhalstead") is not None:
        line += '{0:>{width}.{precision}f}'.format(results.get("vhalstead"), \
                                                   width = COLNUMBERWIDTH + 3, precision = 2)
    
    return line

def pack_profresults(results):
    
    line = ""
    ref_metrics = pack_readablemetrics(get_refmetrics())
    if ref_metrics:
        line += '{0:{width}.{width}} {1}\n'.format("REFERENCE", ref_metrics, width = COLTEXTWIDTH)
    else:
        line += NOREFERENCE + '\n'
        
    for t in results:
        line += '{0:{width}.{width}} {1}\n'.format(t[0], pack_readablemetrics(t[1]), width = COLTEXTWIDTH)
        
    return line[:-1]

def pack_results(results):    
    return tstlib.data2json(results)

def write_results(results, QCHECKFILE):
    content = { "quality" : [results] }
    with open(QCHECKFILE, 'w') as fp:
        json.dump(content, fp, indent = 2, separators=(',', ': '), ensure_ascii=False)
    
    fp.close()
    
def read_tstconfig(exit=False, quit_on_fail=False):
#Code borrowed from tstlib.py (c) 2011-2014 Dalton Serey, UFCG
    if not os.path.exists(TSTCONFIG):
        if quit_on_fail:
            msg = "qcheck: config.json file not found"
            print msg
            #sys.exit(1)
        return {}
    try:
        with codecs.open(TSTCONFIG, mode='r', encoding='utf-8') as f:
            configjson = json.loads(tstlib.to_unicode(f.read()))
    except ValueError:
        msg = "qcheck: %s is corrupted" % TSTCONFIG
        if exit_on_fail:
            print msg
            #sys.exit()
        raise CorruptedFile(msg)
        

    return configjson


def read_tstjson(exit=False, quit_on_fail=False):
#Code borrowed from tstlib.py (c) 2011-2014 Dalton Serey, UFCG
    if not os.path.exists(TSTFILE):
        if quit_on_fail:
            msg = "qcheck: tst.json file not found"
            print msg
            #sys.exit(1)
        return {}
    try:
        with codecs.open(TSTFILE, mode='r', encoding='utf-8') as f:
            tstjson = json.loads(tstlib.to_unicode(f.read()))
        f.close()

    except ValueError:
        msg = "qcheck: %s is corrupted" % TSTFILE
        if exit or quit_on_fail:
            print msg
            #sys.exit(1)
        raise CorruptedConfigFile(msg)
    
    return tstjson

def read_qcheckjson(exit=False, quit_on_fail=False):
#Code borrowed from tstlib.py (c) 2011-2014 Dalton Serey, UFCG
    
    if not os.path.exists(QCHECKFILE):
        if quit_on_fail:
            msg = "qcheck: file not found"
            print msg
            sys.exit(1)
        return {}
    try:
        with codecs.open(QCHECKFILE, mode='r', encoding='utf-8') as f:
            qcheckjson = json.loads(tstlib.to_unicode(f.read()))
        f.close()

    except ValueError:
        msg = "qcheck: %s is corrupted" % QCHECKFILE
        if exit or quit_on_fail:
            print msg
            sys.exit(1)
        raise CorruptedConfigFile(msg)
    
    return qcheckjson

def get_filestocheck(pattern):
     #Code borrowed from tst_test.py (c) 2011-2014 Dalton Serey, UFCG
    
     # Obtain filenames
    if len(pattern) == 1 and os.path.exists(pattern[0]):
        filenames = [pattern[0]]
    elif len(pattern) == 1:
        fn_pattern = "*%s*.py" % pattern[0]
        filenames = glob.glob(fn_pattern)
    #All .py files
    elif len(pattern) == 0:
        fn_pattern = "*.py"
        filenames = glob.glob(fn_pattern)
    else:
        filenames = pattern

    # remove files
    files_to_ignore = ['tst.json']
    filenames = list(set(filenames) - set(files_to_ignore))
    
    return filenames

def parse_arguments():
    from argparse import RawTextHelpFormatter

    parser = argparse.ArgumentParser(description='Check python code static quality metrics.', formatter_class=RawTextHelpFormatter)
    parser.add_argument("-m", "--metrics", nargs = 1, help="get values of cc, header, lloc, pep8, vhalstead")
    parser.add_argument("-f", "-fb", "--feedback", nargs = 1, help="present warning messages referring to static quality metrics")
    parser.add_argument("-p","-prof", "--prof", nargs = "*", help="get values of cc, header, lloc, pep8, vhalstead referring to a given pattern or file(s)")
    parser.add_argument("-s","--set", nargs = 1, help="set reference solution")
    #mudei aqui
    parser.add_argument("-sps","--problemspec", nargs = 1, help="set problem specification")
    parser.add_argument("-o", "--outputformat", type=str, default="human", choices=["human","json"], help="set output format")
    
    parser.add_argument("filename", nargs="*", default = [""])
    
    args = parser.parse_args()
    if args.metrics:
        filenames = args.metrics[0]
        function = "metrics"
    elif args.set:
        filenames = args.set[0]
        function = "set"
    # mudei aqui
    elif args.problemspec:
        filenames = args.problemspec[0]
        function = "problemspec"
    elif args.feedback:
        filenames = args.feedback[0]
        function = "feedback"
    elif args.prof is not None:
        filenames = args.prof
        function = "prof"
    elif args.filename:
        filenames = args.filename[0]
        function = "feedback"
    
    return filenames, function, args.outputformat

def main():
    
    filenames, function, outputformat = parse_arguments()
    logit = ""
    try:
        if function in ('metrics') :
            # metrics output human-readable format
            results = get_rawmetrics(filenames)
            report = pack_results(results) if outputformat == 'json' else pack_readablemetrics(results)
            
        elif function in ('set'): 
            # set reference solution file
            results = get_rawmetrics(filenames)
            write_results(results, QCHECKFILE)
            report = QCHECKFILE + " was created."
        
        elif function in ('problemspec'):
            report = "problem specification was setted."
            vocabulary = get_vocabulary(filenames)
            #write_results(vocabulary, QCHECKFILE)
            report = QCHECKFILE + " was created."

        elif function in ('feedback'): 
            # feedback output human-readable format
            if not get_refmetrics():
                report = NOREFERENCE
            else:
                results = quality_report( get_metrics(filenames) )
                report = pack_results(results) if outputformat == 'json' else pack_markdownfeedback(filenames, results)
                logit = get_logdata(filenames, pack_logfeedback(results))
                
        elif function in ('prof'):
            setofcode = sorted(get_filestocheck(filenames))
            if not setofcode:
                print( "qcheck: nothing to check.")
                sys.exit()
            results = []
            for code in setofcode:
                results.append((code, get_rawmetrics(code)))
            report = pack_profresults(results)
            
        print report
        ### Is log active?
        if logit:
            qchecklib.save(logit)
            
    except IOError:
        print("Usage: tst qcheck [options] code.py")
        sys.exit(1)
    
if __name__ == "__main__":
    
    if len(sys.argv) < 2:
        print("Usage: tst qcheck [options] code.py")
        sys.exit()
     
    if len(sys.argv) > 1 and sys.argv[1] == '--one-line-help':
        print("check code quality")
        sys.exit()
    
    main()
