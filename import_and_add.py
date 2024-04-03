from olclient.openlibrary import OpenLibrary
import json
from collections import namedtuple

Credentials = namedtuple("Credentials", ["username", "password"])
credentials = Credentials("openlibrary@example.com", "admin123")
ol = OpenLibrary(base_url="http://localhost:8080", credentials=credentials)

def import_isbns(filename):
    with open(filename, "r") as f:
        isbn_dict = {data['ISBN']: data['OpenAlex'].split('/')[-1] for data in map(json.loads, f)}
    return isbn_dict

def add_identifiers(isbn_dict):
    for isbn , id in isbn_dict.items():
        record = ol.session.get(f"http://localhost:8080/isbn/{isbn}.json")
        record = record.json()
        key = record.get("key").split("/")[-1]
        edition = ol.Edition.get(key)
        edition.add_id("OpenAlex",id)
        print(edition.identifiers)
        edition.save("edit adds an OpenAlex identifier.")

def main(filename):
    print("reached main")
    isbn_dict = import_isbns(filename) # Hits.jsonl/Not_Found.jsonl
    add_identifiers(isbn_dict)
