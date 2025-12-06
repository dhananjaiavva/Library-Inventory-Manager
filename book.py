# library_manager/book.py
"""
Book module
Contains the Book class used in the library inventory system.
"""

class Book:
    def __init__(self, title: str, author: str, isbn: str, status: str = "available"):
        """
        Initialize a Book object.

        :param title: Title of the book
        :param author: Author of the book
        :param isbn: Unique ISBN number
        :param status: "available" or "issued"
        """
        self.title = title
        self.author = author
        self.isbn = isbn
        # normalize status
        self.status = status.lower() if status else "available"

    def __str__(self) -> str:
        """Return a user-friendly string representation of the book."""
        return f"{self.title} by {self.author} (ISBN: {self.isbn}) - {self.status.upper()}"

    def to_dict(self) -> dict:
        """
        Convert Book object to a dictionary (for JSON saving).
        """
        return {
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "status": self.status
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Book":
        """
        Create a Book object from a dictionary (for JSON loading).
        """
        return cls(
            title=data.get("title", ""),
            author=data.get("author", ""),
            isbn=data.get("isbn", ""),
            status=data.get("status", "available")
        )

    # --- Required methods ---

    def issue(self):
        """Mark the book as issued if it is available."""
        if self.is_available():
            self.status = "issued"
        else:
            raise ValueError("Book is already issued.")

    def return_book(self):
        """Mark the book as available if it is issued."""
        if not self.is_available():
            self.status = "available"
        else:
            raise ValueError("Book is already available.")

    def is_available(self) -> bool:
        """Check if the book is available."""
        return self.status == "available"
