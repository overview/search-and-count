search-and-count
================

Reads a list of search terms and an input CSV. Outputs a CSV showing how many rows each search term appears in.

Usage: `python search-and-count.py <terms.csv> <documents.csv>`

Terms.csv should be one search term/phrase per row, without a header row. Documents.csv should have one document per row, with a header row with one column named "text" indicating which column to search (this is the export format for an Overview document set.) Phrases will be matched at the word level, where words are considered to by anything separated by whitespace. All matches are case insensitive.

Outputs a list of term,occurences pairs to the console, with no header. Each term can match each document only once, even if it appears multiple times in that document.

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
    folk are using newlines (phrase match across newline)"`

Example run on this data

    > python search-and-count.py terms.csv text.csv 
    help,1
    strange folk,2`
