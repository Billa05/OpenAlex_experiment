import json
from isbnlib import to_isbn13, NotValidISBNError
from concurrent.futures import ThreadPoolExecutor

def process_line(line):
    try:
        json_str = line.split("\t")[-1]
        json_data = json.loads(json_str)
    except json.JSONDecodeError:
        print(f"Error decoding JSON on line {count}: {line}")
        return None

    try:
        if not json_data.get("isbn_13"):
            if json_data.get("isbn_10"):
                isbn = to_isbn13(json_data.get("isbn_10")[0])
        else:
            isbn = json_data.get("isbn_13")[0]
    except (KeyError, NotValidISBNError) as e:
        print(f"Error getting ISBN on line {count}: {e}")
        return None

    if isbn in isbn_dict:
        json_data['output_value'] = isbn_dict[isbn]
        not_found_isbn_dict.pop(isbn, None)
        return {"OpenAlex": isbn_dict[isbn], "ISBN_13": isbn, "edition": json_data["key"]}

count = 0
# Read all ISBNs and their values from output.jsonl into a dictionary
try:
    with open("OpenAlex_isbn.jsonl", "r") as f:
        isbn_dict = {list(json.loads(line).keys())[0]: list(json.loads(line).values())[0] for line in f}
except (FileNotFoundError, PermissionError) as e:
    print(f"Error accessing output.jsonl: {e}")
    isbn_dict = {}
except MemoryError:
    print("Error: Not enough memory to load output.jsonl")
    isbn_dict = {}

# Create a copy of isbn_dict to store the ISBNs that are not found in ol_dump.txt
not_found_isbn_dict = isbn_dict.copy()

# Open the new file to write the details
try:
    with open("Hits.jsonl", "w") as details_file, open("ol_dump.txt", "r") as file, ThreadPoolExecutor(max_workers=10) as executor:
        lines = file.readlines()
        results = list(executor.map(process_line, lines))
        for result in results:
            if result is not None:
                details_file.write(json.dumps(result) + "\n")
                print(count)
                count += 1
except (FileNotFoundError, PermissionError) as e:
    print(f"Error accessing ol_dump.txt or Hits.jsonl: {e}")
except MemoryError:
    print("Error: Not enough memory to process ol_dump.txt")

# Write the details of the ISBNs that were not found in ol_dump.txt to a new file
try:
    with open("Not_Found.jsonl", "w") as not_found_file:
        for isbn, value in not_found_isbn_dict.items():
            not_found_file.write(json.dumps({"ISBN_13": isbn, "OpenAlex": value}) + "\n")
except (FileNotFoundError, PermissionError) as e:
    print(f"Error accessing Not_Found.jsonl: {e}")