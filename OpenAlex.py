import requests
import json
import os
from isbnlib import NotValidISBNError, ISBNLibException
from isbnlib import get_canonical_isbn, to_isbn13
from concurrent.futures import ThreadPoolExecutor

def process_result(result):
    if result.get("doi"):
        try:
            isbn = result["doi"].split("/")[-1]
            canonical_isbn = get_canonical_isbn(isbn)
            if canonical_isbn:
                isbn = to_isbn13(canonical_isbn)
                OpenAlex_ID = result['id']
                return {isbn: OpenAlex_ID}
        except (NotValidISBNError, ISBNLibException) as e:
            print(f"Error processing ISBN: {e}")

def fetch_books(max_records):
    next_cursor = "*"
    record_count = 0
    output_file = 'OpenAlex_isbn1.jsonl'
    print("reached fetch_books")
    with requests.Session() as session, open(output_file, 'w') as f, ThreadPoolExecutor(max_workers=10) as executor:
        while True:
            open_alex = f"https://api.openalex.org/works?filter=type:book&sort=cited_by_count:desc&cursor={next_cursor}"
            try:
                response = session.get(open_alex)
                response.raise_for_status()  # Raises a HTTPError if the response status code is 4xx or 5xx
                data = response.json()
                next_cursor = data["meta"]["next_cursor"]
            except (requests.HTTPError, json.JSONDecodeError) as e:
                print(f"Error fetching or parsing data from OpenAlex: {e}")
                break

            if not data.get("results"):
                break

            results = list(executor.map(process_result, data["results"]))
            for result in results:
                if result is not None:
                    record_count += 1
                    if record_count > max_records:
                        break
                    else:
                        f.write(json.dumps(result) + '\n')

            if record_count > max_records:
                break

    print(f"Output file is saved at: {os.path.relpath(output_file)}")