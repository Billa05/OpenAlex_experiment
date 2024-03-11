import requests
import json
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

next_cursor = "*"
record_count = 0

with requests.Session() as session, open('output2.jsonl', 'w') as f, ThreadPoolExecutor(max_workers=10) as executor:
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
                if record_count > 100000:
                    break
                else:
                    f.write(json.dumps(result) + '\n')

        if record_count > 100000:
            break