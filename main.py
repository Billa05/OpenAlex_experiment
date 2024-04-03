import argparse
from OpenAlex import fetch_books
from using_ol_dump.find import find_isbns


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='CLI for fetching books, finding ISBNs, and adding identifiers')
    
    parser.add_argument('--fetch_openalex_books', action='store_true', help='Fetch books from OpenAlex')
    parser.add_argument('--max_records', type=int, default=100000, help='Maximum number of records to fetch')
    
    parser.add_argument('--find_isbns', action='store_true', help='Find ISBNs from OpenAlex data')
    parser.add_argument('--dump_file', type=str, default='using_ol_dump/ol_dump.txt', help='OL dump file to search for ISBNs')
    parser.add_argument('--found_file', type=str, default='using_ol_dump/Hits.jsonl', help='Output file to write found ISBNs')
    parser.add_argument('--not_found_file', type=str, default='using_ol_dump/Not_Found.jsonl', help='File to write ISBNs that were not found')
    
    parser.add_argument('--add_identifier', action='store_true', help='Add OpenAlex identifiers')
    parser.add_argument('--filename', type=str, default='using_ol_dump/Not_Found.jsonl', help='relative path of file with ISBNs and OpenAlex identifiers')
 
    args = parser.parse_args()

    if args.fetch_openalex_books:
        fetch_books(args.max_records)

    if args.find_isbns:
        find_isbns(args.dump_file, args.found_file, args.not_found_file)

    if args.add_identifier:
        from import_and_add import main
        main(args.filename)