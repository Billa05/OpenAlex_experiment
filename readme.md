# OpenAlex Book Fetching and ISBN Processing

## Fetching Top 100k Books

`OpenAlex.py` script fetches the top 100k books from OpenAlex via their API, processes the results to extract and standardize the ISBNs, and saves the data to a JSONL file. It uses concurrent processing with a `ThreadPoolExecutor` for efficiency.

## ISBN Processing in OpenLibrary Dump

`find.py` script loads ISBNs from "OpenAlex_isbn.jsonl", reads an OpenLibrary dump from "ol_dump.txt" in the "using ol_dump" folder, and checks for matches. Make sure you have the "ol_dump.txt" file in the "using ol_dump" folder. Matches and non-matches are written to "Hits.jsonl" and "Not_Found.jsonl" respectively. ISBN-10s are converted to ISBN-13s for standardization.

## Adding OpenAlex Identifiers and Importing the NotFound Records

The script `import_and_add.py` imports the ISBNs from the "Not_Found.jsonl" file, adds OpenAlex identifiers to the OpenLibrary records, and saves the changes. 

It uses the OpenLibrary client to interact with a local instance of OpenLibrary. Make sure you have the OpenLibrary client installed and a local instance of OpenLibrary running.

The script uses the following process:

1. It loads the ISBNs from the "Not_Found.jsonl" file into a dictionary with the ISBN as the key and the OpenAlex identifier as the value.

2. It iterates over the dictionary. For each ISBN, it fetches the corresponding OpenLibrary record, adds the OpenAlex identifier to the record, and saves the changes.

3. The changes are printed to the console for verification.

To run the script, use the command `python import_and_add.py`.

Note: The script currently stops after processing one record for demonstration purposes. Remove the `break` statement in the `add_identifiers` function to process all records.







