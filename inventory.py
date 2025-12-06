# library_manager/inventory.py
"""
Inventory module
Contains the LibraryInventory class which manages a collection of books.
"""

import json
import logging
from pathlib import Path

from .book import Book


class LibraryInventory:
    def __init__(self):
        """
        Initialize an empty inventory of books.
        """
        self.books = []

    # ---------- Book management methods ----------

    def add_book(self, book: Book) -> None:
        """
        Add a new book to the inventory.
        Avoid duplicate ISBNs.
        """
        if self.search_by_isbn(book.isbn):
            raise ValueError(f"A book with ISBN {book.isbn} already exists.")
        self.books.append(book)
        logging.info("Book added: %s", book)

    def search_by_title(self, title: str):
        """
        Search for books by (partial) title, case-insensitive.
        Returns a list of Book objects.
        """
        title = title.lower()
        return [book for book in self.books if title in book.title.lower()]

    def search_by_isbn(self, isbn: str):
        """
        Search for a book by ISBN.
        Returns a Book object or None.
        """
        for book in self.books:
            if book.isbn == isbn:
                return book
        return None

    def display_all(self):
        """
        Return a list of string representations of all books.
        (Printing will be handled in CLI.)
        """
        return [str(book) for book in self.books]

    # ---------- File handling methods (JSON) ----------

    def load_from_file(self, file_path: Path) -> None:
        """
        Load book data from a JSON file.
        If file does not exist or is corrupted, start with an empty inventory.
        """
        try:
            if not file_path.exists():
                logging.info("Catalog file does not exist yet: %s", file_path)
                self.books = []
                return

            with file_path.open("r", encoding="utf-8") as f:
                data = json.load(f)

            self.books = [Book.from_dict(item) for item in data]
            logging.info("Loaded %d books from %s", len(self.books), file_path)

        except json.JSONDecodeError as e:
            logging.error("JSON file is corrupted: %s", e)
            print("Warning: catalog file is corrupted. Starting with an empty inventory.")
            self.books = []

        except Exception as e:
            logging.error("Error loading file: %s", e)
            print("Error loading catalog file. Starting with an empty inventory.")
            self.books = []

    def save_to_file(self, file_path: Path) -> None:
        """
        Save book data to a JSON file.
        """
        try:
            data = [book.to_dict() for book in self.books]
            with file_path.open("w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            logging.info("Saved %d books to %s", len(self.books), file_path)
        except Exception as e:
            logging.error("Error saving file: %s", e)
            print("Error: Could not save catalog to file.")
