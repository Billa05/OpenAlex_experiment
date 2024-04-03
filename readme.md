# OpenAlex Book Fetching and ISBN Processing

This project provides a command-line interface (CLI) for fetching books from OpenAlex, finding ISBNs in an OpenLibrary dump, and adding OpenAlex identifiers to OpenLibrary records.

## Command Line Interface (CLI) Usage

### Fetching Books from OpenAlex

To fetch books from OpenAlex, use the `--fetch_openalex_books` flag. The script fetches the top 100k books by default. You can specify a different number with the `--max_records` option. For example:

```bash
python main.py --fetch_openalex_books --max_records 50000
```
### Finding ISBNs in OpenLibrary Dump

To find ISBNs from the fetched OpenAlex data in an OpenLibrary dump, use the --find_isbns flag. The script reads the dump from `using_ol_dump/ol_dump.txt` by default. You can specify your dump file path with the --dump_file option. The script writes found ISBNs to `using_ol_dump/Hits.jsonl` and ISBNs that were not found to `using_ol_dump/Not_Found.jsonl` by default. You can specify different output files with the --found_file and --not_found_file options. For example:

```bash
python main.py --find_isbns --dump_file path/to/your/dump.txt --found_file path/to/your/found.jsonl --not_found_file path/to/your/not_found.jsonl
```

### Adding OpenAlex Identifiers

To add OpenAlex identifiers to OpenLibrary records, use the --add_identifier flag. The script reads ISBNs and OpenAlex identifiers from `using_ol_dump/Not_Found.jsonl` by default. You can specify a different file with the --filename option. For example:

```bash
python main.py --add_identifier --filename path/to/your/file.jsonl
```
This script will add OpenAlex identifiers to the OpenLibrary records corresponding to the ISBNs in the specified file.

## Scripts Logic

### Fetching Top 100k Books

The OpenAlex.py script fetches the top 100k books from OpenAlex via their API, processes the results to extract and standardize the ISBNs, and saves the data to a JSONL file. It uses concurrent processing with a ThreadPoolExecutor for efficiency.

### ISBN Processing in OpenLibrary Dump

The find.py script loads ISBNs from `OpenAlex_isbn.jsonl`, reads an OpenLibrary dump from `ol_dump.txt` in the `using ol_dump` folder, and checks for matches. Make sure you have the `ol_dump.txt` file in the `using ol_dump` folder. Matches and non-matches are written to `Hits.jsonl` and `Not_Found.jsonl` respectively. ISBN-10s are converted to ISBN-13s for standardization.

### Adding OpenAlex Identifiers and Importing the NotFound Records

The import_and_add.py script reads ISBNs from a given file (default is `Not_Found.jsonl`). If an ISBN doesn't exist in the database, it imports and appends the corresponding OpenAlex identifiers to the OpenLibrary records. If the ISBN already exists, it simply adds the OpenAlex identifier. All changes are saved.

It uses the OpenLibrary client to interact with a local instance of OpenLibrary. Make sure you have the OpenLibrary client installed and a local instance of OpenLibrary running.

The script uses the following process:

    1. It loads the ISBNs from the specified file into a dictionary with the ISBN as the key and the OpenAlex identifier as the value. This is done in the import_isbns function.

    2. It iterates over the dictionary. For each ISBN, it fetches the corresponding OpenLibrary record, adds the OpenAlex identifier to the record, and saves the changes. This is done in the add_identifiers function.

Note: The script processes all records in the specified file. If you want to add identifiers to the records in a different file, change the filename in the main function call to the desired file (e.g., `Hits.jsonl`).

