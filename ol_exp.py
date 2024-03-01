import requests
from concurrent.futures import ThreadPoolExecutor
from threading import Lock
from isbnlib import get_canonical_isbn, is_isbn10, is_isbn13, canonical


ol_search = "https://openlibrary.org/search.json"
open_alex = "https://api.openalex.org/works?page={}&filter=type:book&sort=cited_by_count:desc"

def process_result(result, record_count,isbn, session, lock):
    try:
        ol_response = session.get(ol_search, params={"isbn": isbn})
        if ol_response.text:  # Check if the response is not empty
            try:
                ol_response_data = ol_response.json()
            except ValueError:
                print(f'title: {result["title"]}, book_no: {record_count},status_code: {ol_response.status_code}')
                return
            if ol_response_data.get('numFound') != 0:
                with lock:
                    with open("isbn_found_in_OL", "a") as file:
                        file.write(f" book_no: {record_count}, Openalex_id: {result['id']}, OL_key: {ol_response_data['docs'][0]['key']}, isbn: {isbn}\n")
            else:
                with lock:
                    with open("isbn_notfound_in_OL", "a") as file:
                            file.write(f" book_no: {record_count}, Openalex_id: {result['id']}, isbn: {isbn}\n")
        else:
            print(f"No response for title: {result['title']}, book_no: {record_count}")
    except Exception as e:
        print(f"Error processing result: {e}, id: {result['id']}")

def main():
    page = 1
    record_count = 0
    lock = Lock()

    with requests.Session() as session:
        while True:
            response = session.get(open_alex.format(page))
            data = response.json()

            if not data["results"]:
                break

            with ThreadPoolExecutor(max_workers=10) as executor:
                for result in data["results"]:
                    record_count += 1
                    if record_count > 200:
                        break
                    else:
                        if result["doi"]:
                            isbn = result["doi"].split("/")[-1]
                            if get_canonical_isbn(isbn):
                                # print("canonical isbn: ", get_canonical_isbn(isbn))
                                isbn = get_canonical_isbn(isbn)
                                with lock:
                                    with open("isbn_of_first200_books", "a") as file:
                                        file.write(f"isbn found: {isbn}\n")
                                executor.submit(process_result, result, record_count,isbn, session, lock)
                            else:
                                with lock:
                                    with open("isbn_of_first200_books", "a") as file:
                                        file.write(f"isbn not found: {isbn}\n")
                                continue
                        else:
                            # print("DOI not found: ", result["title"])
                            continue

            if record_count > 200:
                break

            page += 1

if __name__ == "__main__":
    main()