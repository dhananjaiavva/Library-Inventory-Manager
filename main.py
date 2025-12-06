# cli/main.py

"""
Main CLI for Library Inventory Manager.
Provides menu options to interact with the inventory.
"""

import logging
from pathlib import Path

from library_manager import Book, LibraryInventory


def setup_logging():
    """
    Configure logging to write to a file named library.log.
    """
    logging.basicConfig(
        filename="library.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )


def print_menu():
    print("\n=== Library Inventory Manager ===")
    print("1. Add Book")
    print("2. Issue Book")
    print("3. Return Book")
    print("4. View All Books")
    print("5. Search Books")
    print("6. Exit")


def get_choice():
    """
    Safely get a menu choice from the user.
    """
    try:
        choice = int(input("Enter your choice (1-6): ").strip())
        if choice not in range(1, 7):
            raise ValueError
        return choice
    except ValueError:
        print("Invalid input. Please enter a number between 1 and 6.")
        return None


def handle_add_book(inventory: LibraryInventory, catalog_path: Path):
    title = input("Enter book title: ").strip()
    author = input("Enter book author: ").strip()
    isbn = input("Enter book ISBN: ").strip()

    if not title or not author or not isbn:
        print("All fields are required.")
        return

    try:
        book = Book(title=title, author=author, isbn=isbn)
        inventory.add_book(book)
        inventory.save_to_file(catalog_path)
        print("Book added successfully.")
    except ValueError as e:
        print("Error:", e)


def handle_issue_book(inventory: LibraryInventory, catalog_path: Path):
    isbn = input("Enter ISBN of the book to issue: ").strip()
    book = inventory.search_by_isbn(isbn)
    if not book:
        print("Book not found.")
        return
    try:
        book.issue()
        inventory.save_to_file(catalog_path)
        print("Book issued successfully.")
    except ValueError as e:
        print("Error:", e)


def handle_return_book(inventory: LibraryInventory, catalog_path: Path):
    isbn = input("Enter ISBN of the book to return: ").strip()
    book = inventory.search_by_isbn(isbn)
    if not book:
        print("Book not found.")
        return
    try:
        book.return_book()
        inventory.save_to_file(catalog_path)
        print("Book returned successfully.")
    except ValueError as e:
        print("Error:", e)


def handle_view_all(inventory: LibraryInventory):
    books_list = inventory.display_all()
    if not books_list:
        print("No books in the catalog.")
        return
    print("\n--- All Books ---")
    for line in books_list:
        print(line)


def handle_search(inventory: LibraryInventory):
    print("Search by:")
    print("1. Title")
    print("2. ISBN")

    try:
        sub_choice = int(input("Enter your choice (1-2): ").strip())
    except ValueError:
        print("Invalid choice.")
        return

    if sub_choice == 1:
        title = input("Enter part or full title: ").strip()
        results = inventory.search_by_title(title)
        if not results:
            print("No books found with that title.")
        else:
            print("\nSearch results:")
            for book in results:
                print(book)
    elif sub_choice == 2:
        isbn = input("Enter ISBN: ").strip()
        book = inventory.search_by_isbn(isbn)
        if not book:
            print("No book found with that ISBN.")
        else:
            print("Book found:")
            print(book)
    else:
        print("Invalid choice.")


def main():
    setup_logging()

    catalog_path = Path("catalog.json")
    inventory = LibraryInventory()

    # Load existing data with exception handling
    inventory.load_from_file(catalog_path)

    while True:
        print_menu()
        choice = get_choice()
        if choice is None:
            continue

        if choice == 1:
            handle_add_book(inventory, catalog_path)
        elif choice == 2:
            handle_issue_book(inventory, catalog_path)
        elif choice == 3:
            handle_return_book(inventory, catalog_path)
        elif choice == 4:
            handle_view_all(inventory)
        elif choice == 5:
            handle_search(inventory)
        elif choice == 6:
            # Save before exit (safety)
            try:
                inventory.save_to_file(catalog_path)
            finally:
                print("Exiting... Goodbye!")
                break


if __name__ == "__main__":
    main()
