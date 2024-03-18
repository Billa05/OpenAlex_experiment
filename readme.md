# OpenAlex Book Fetching and ISBN Processing

## Fetching Top 100k Books

`OpenAlex.py` script fetches the top 100k books from OpenAlex via their API, processes the results to extract and standardize the ISBNs, and saves the data to a JSONL file. It uses concurrent processing with a `ThreadPoolExecutor` for efficiency.

## ISBN Processing in OpenLibrary Dump

`new.py` script loads ISBNs from "OpenAlex_isbn.jsonl", reads an OpenLibrary dump from "ol_dump.txt" in the "using ol_dump" folder, and checks for matches. Make sure you have the "ol_dump.txt" file in the "using ol_dump" folder. Matches and non-matches are written to "Hits.jsonl" and "Not_Found.jsonl" respectively. ISBN-10s are converted to ISBN-13s for standardization.