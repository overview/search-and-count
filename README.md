search-and-count
================

Reads a list of search terms and an input CSV. Outputs a CSV showing how many rows each search term appears in.

Usage: search-and-count <terms.csv> <documents.csv>

Terms.csv should not have a header. Documents.csv should have a header row with one column named "text" which is the column that will be searched (this is the export format for an Overview document set.) Phrases will be matched at the word level, where words are considered to by anything separated by whitespace. All matches are case insensitive.

Outputs a list of term,occurences pairs to the console, with no header. Each term can match each document only once, even if it appears multiple times in that document.

