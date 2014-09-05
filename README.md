search-and-count
================

Reads a list of search terms and an input CSV. Outputs a CSV showing how many rows each search term appears in.

usage: search-and-count.py [-h] [-m] [-n] [-c] [-f FUZZY] terms documents

Search for strings within a CSV, using a word-by-word match

positional arguments:
  terms                 file with phrases to match, one per line
  documents             CSV file of text to match against

optional arguments:
  -h, --help            show this help message and exit
  -m, --matches         count total number of matches instead of number of
                        matching rows
  -n, --normalizespaces
                        treat newlines, tabs, multiple spaces etc. as single
                        spaces
  -c, --casesenstive    case-senstive match
  -f FUZZY, --fuzzy FUZZY
                        use fuzzy string matching with specified edit distance

Terms.csv should be one search term/phrase per row, without a header row. Documents.csv should have one document per row, with a header row with one column named "text" indicating which column to search (this is the export format for an Overview document set.) Phrases will be matched at the word level, where words are considered to by anything separated by whitespace. 

Matches are case insensitive by default, use -c for a case sensitive search. Each word must match exactly, use -f [distance] to specify a maximum edit distance (applied to each individual word for search terms that are phrases.) Outputs the number of documents containing each term, use -m to output total number of matches (counting multiple matches per document.)

Example terms.csv:

    help
    strange folk

Example documents.csv:

    text
    I was feeling helpful (no match on partial word)
    I can help tomorrow (match)
    These folks are strange (no match)
    These strange folk are improving my day (match)
    These strange folks are improving my day (no match on partial word)
    "These strange
    folk are using newlines (match across newline)"

Example run on this data

    > python search-and-count.py terms.csv text.csv 
    help,1
    strange folk,2`
