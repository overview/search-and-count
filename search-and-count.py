#!/usr/bin/python

# Read a list of search terms/phrases, one per line, and an input CSV
# Output to console: how many rows each term appears in
# Usage:
#   search-and-count terms.csv documents.csv 

import sys
import csv
import re
import argparse


# Collapse all runs of space characters (including newlines etc.) into a single space. Also trims
def normalizeSpaces(str):
    rex = re.compile(r'\W+')
    return rex.sub(' ', str).strip()


# from http://rosettacode.org/wiki/Levenshtein_distance#Python
def levenshteinDistance(s1,s2):
    if len(s1) > len(s2):
        s1,s2 = s2,s1
    distances = range(len(s1) + 1)
    for index2,char2 in enumerate(s2):
        newDistances = [index2+1]
        for index1,char1 in enumerate(s1):
            if char1 == char2:
                newDistances.append(distances[index1])
            else:
                newDistances.append(1 + min((distances[index1],
                                             distances[index1+1],
                                             newDistances[-1])))
        distances = newDistances
    return distances[-1]

# Do all strings within two lists match to within a specific edit distance?
def fuzzyListEq(a, b, dist):
    return all(list(levenshteinDistance(a[i], b[i])<=dist for i in range(len(a))))

# based on http://stackoverflow.com/questions/3313590/check-for-presence-of-a-sublist-in-python
def sublistMatches(lst, sublst, fuzzy):
    n = len(sublst)
    if fuzzy==0:
        return sum((sublst == lst[i:i+n]) for i in xrange(len(lst)-n+1))
    else:
        return sum(fuzzyListEq(sublst, lst[i:i+n], fuzzy) for i in xrange(len(lst)-n+1))

# Return number of occurences of term in string.
def termInString(term, text, fuzzy):
    termWords = term.split()
    textWords = text.split()
    return sublistMatches(textWords, termWords, fuzzy)
	

# given a dictionary of terms->counts and a string, increment the counts for every term found in the string
# Increments by one, no matter how many times the string appears
def updateCounts(termcounts, text, count_matches, case_senstive, normalizespaces, fuzzy):
    if normalizespaces:
        text = normalizeSpaces(text)
    if not case_senstive:
        text = text.upper()

    for term in termcounts:
        term2 = term if case_sensitive else term.upper()  # can't modify term here as we're iterating over dict

        hits = termInString(term2, text, fuzzy)
        if (hits) > 0:
            if count_matches:
                termcounts[term] += hits
            else:
                termcounts[term] += 1



# --- main ----

parser = argparse.ArgumentParser(description='Search for strings within a CSV, using a word-by-word match')
parser.add_argument('terms', help='file with phrases to match, one per line')
parser.add_argument('documents', help='CSV file of text to match against')
parser.add_argument('-m', '--matches', action="store_true", help='count total number of matches instead of number of matching rows')
parser.add_argument('-n', '--normalizespaces', action="store_true", help='treat newlines, tabs, multiple spaces etc. as single spaces')
parser.add_argument('-c', '--casesenstive', action="store_true", help='case-senstive match')
parser.add_argument('-f', '--fuzzy', nargs=1, type=int, help='use fuzzy string matching with specified edit distance')
args = parser.parse_args()

termfile = args.terms
datafile = args.documents
count_matches = args.matches
case_sensitive = args.casesenstive
normalize_spaces = args.normalizespaces
if args.fuzzy != None:
    fuzzy = args.fuzzy[0]
else:
    fuzzy = 0

# read list of terms, one per line
# Assumes no header row, reads terms from first column
terms = []
with open(termfile, 'rU') as f:
    reader = csv.reader(f)
    for row in reader:
    	term = row[0].strip()				# first column, strip leading and trailing whitespace
    	if len(term)>2 and term[0]=='"' and term[-1]=='"':	# strip quotes if quoted
    		term = term[1:-1]
        if normalize_spaces:
            term = normalizeSpaces(term)
    	if term != "":
        	terms.append(term) 


# create a dictionary of terms, with all counts initially 0
termcounts = {term:0 for term in terms}

# check for matches against each row 
with open(datafile, 'rU') as f:
    reader = csv.reader(f)

    # Get index of text column
    headers = reader.next()
    try:
    	textCol = headers.index("text")
    except ValueError:
    	print "Count not find 'text' column in documents file -- check CSV headers?"
    	sys.exit(0)

    for row in reader:
        updateCounts(termcounts, row[textCol], count_matches, case_sensitive, normalize_spaces, fuzzy)


# output terms and document counts to stdout, sorted case insensitive
for termcount in sorted(termcounts.items(), key=lambda s: s[0].lower()):
	print termcount[0] + "," + str(termcount[1])


