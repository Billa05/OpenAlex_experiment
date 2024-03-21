# OpenAlex Book Fetching and ISBN Processing

## Fetching Top 100k Books

`OpenAlex.py` script fetches the top 100k books from OpenAlex via their API, processes the results to extract and standardize the ISBNs, and saves the data to a JSONL file. It uses concurrent processing with a `ThreadPoolExecutor` for efficiency.

## ISBN Processing in OpenLibrary Dump

`find.py` script loads ISBNs from "OpenAlex_isbn.jsonl", reads an OpenLibrary dump from "ol_dump.txt" in the "using ol_dump" folder, and checks for matches. Make sure you have the "ol_dump.txt" file in the "using ol_dump" folder. Matches and non-matches are written to "Hits.jsonl" and "Not_Found.jsonl" respectively. ISBN-10s are converted to ISBN-13s for standardization.

## Adding OpenAlex Identifiers to OpenLibrary Records

The script [`add_identifiers.py`](https://github.com/Billa05/openlibrary-client/blob/master/adding%20identifiers/add_identifiers.py) is used to add OpenAlex identifiers to the corresponding editions in OpenLibrary. This script is part of the [`openlibrary-client`](https://github.com/internetarchive/openlibrary-client/blob/master/README.md) repository.

Before running this script, ensure that:

1. The local OpenLibrary development environment is up and running.
2. The records from Hits.jsonl have been copied to the local development environment using the [`copydocs.py`](https://github.com/internetarchive/openlibrary/wiki/Loading-Production-Book-Data) script in the local development environment.

Here is a brief overview of how the `add_identifiers.py` script works:

1. It establishes a connection to the local OpenLibrary instance using the OpenLibrary client.
2. It reads the "Hits.jsonl" file and creates a dictionary mapping OpenAlex identifiers to OpenLibrary edition identifiers. Make sure you have the "Hits.jsonl" file in the correct directory before running the script.
3. For each pair of identifiers, it fetches the corresponding edition from OpenLibrary, adds the OpenAlex identifier to the edition's identifiers, and saves the changes.





