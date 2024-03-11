import json
import requests
from isbnlib import to_isbn10
from concurrent.futures import ThreadPoolExecutor
from retry import retry

ol_search = "https://openlibrary.org/search.json"

@retry(tries=5, delay=2, backoff=2)
def make_request(url, params):
    response = requests.get(url, params=params)
    if response.status_code != 200:
        print(f"Error: HTTP status code {response.status_code}", params)
        with open("error.jsonl", "a") as error_file:
            error_file.write(json.dumps({params['isbn']: response.status_code}) + "\n")
        raise Exception("HTTP error")
    return response.json()

def worker(key, value):
    try:
        ol_response_data = make_request(ol_search, {"isbn": key})
    except Exception as e:
        print(f"Error occurred while making a request: {e}")
        with open("error.jsonl", "a") as error_file:
            error_file.write(json.dumps({key: str(e)}) + "\n")
        return

    if ol_response_data.get('numFound') == 0:
        try:
            ol_response_data = make_request(ol_search, {"isbn": to_isbn10(key)})
        except Exception as e:
            print(f"Error occurred while making a request: {e}")
            with open("error.jsonl", "a") as error_file:
                error_file.write(json.dumps({key: str(e)}) + "\n")
            return

        if ol_response_data.get('numFound') == 0:
            print(f"Neither ISBN-13 nor ISBN-10 found for {key}")
            try:
                with open("Not_Found.jsonl", "a") as not_found_file:
                    not_found_file.write(json.dumps({"ISBN_13": key, "OpenAlex": value}) + "\n")
            except IOError as e:
                print(f"Error occurred while writing to file: {e}")
        else:
            print(f"ISBN-10 found for {to_isbn10(key)}")
            try:
                with open("Hits.jsonl", "a") as details_file:
                    details_file.write(json.dumps({"OpenAlex": value, "ISBN_10": to_isbn10(key), "edition": ol_response_data['docs'][0]['key']}) + "\n")
            except IOError as e:
                print(f"Error occurred while writing to file: {e}")
    else:
        print(f"ISBN-13 found for {key}")
        try:
            with open("Hits.jsonl", "a") as details_file:
                details_file.write(json.dumps({"OpenAlex": value, "ISBN_13": key, "edition": ol_response_data['docs'][0]['key']}) + "\n")
        except IOError as e:
            print(f"Error occurred while writing to file: {e}")

try:
    with open("OpenAlex_isbn.jsonl", "r") as f:
        isbn_dict = {list(json.loads(line).keys())[0]: list(json.loads(line).values())[0] for line in f}
        with ThreadPoolExecutor() as executor:
            for key, value in isbn_dict.items():
                executor.submit(worker, key, value)
except IOError as e:
    print(f"Error occurred while opening the file: {e}")