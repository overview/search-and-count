#!/usr/bin/python

# Read a list of search terms/phrases, one per line, and an input CSV
# Output to console: how many rows each term appears in
# Usage:
#   search-and-count terms.csv documents.csv 

import sys
import csv


# What kind of match are we looking for? 
def termInString(term, str):
	return term.upper() in str.upper()  # case-insensitive exact substring match
	

# given a dictionary of terms->counts and a string, increment the counts for every term found in the string
# Increments by one, no matter how many times the string appears
def updateCounts(termcounts, str):
	for term in termcounts:
		if termInString(term, str):
			termcounts[term] += 1



# --- main ----

if len(sys.argv) < 3:
	print "Usage: search-and-count <terms.csv> <documents.csv>"
	sys.exit()
termfile = sys.argv[1]	
datafile = sys.argv[2]

# read list of terms, one per line
with open(termfile) as f:
    terms = f.readlines()

# create a dictionary of terms, with all counts initially 0
termcounts = {term.strip():0 for term in terms}

# check for matches against each row 
with open(datafile, 'rb') as f:
    reader = csv.reader(f)

    # Get index of text column
    headers = reader.next()
    try:
    	textCol = headers.index("text")
    except ValueError:
    	print "Count not find 'text' column in documents file -- check CSV headers?"
    	sys.exit(0)

    for row in reader:
        updateCounts(termcounts, row[textCol])


# output terms and document counts to stdout
for term in termcounts:
	print term + "," + str(termcounts[term])


