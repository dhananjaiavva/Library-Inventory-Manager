# tests/test_inventory.py

import unittest
from library_manager import Book, LibraryInventory


class TestLibraryInventory(unittest.TestCase):
    def test_add_and_search_book(self):
        inventory = LibraryInventory()
        book = Book("Test Title", "Test Author", "12345")
        inventory.add_book(book)

        found = inventory.search_by_isbn("12345")
        self.assertIsNotNone(found)
        self.assertEqual(found.title, "Test Title")

    def test_issue_and_return(self):
        book = Book("Test", "Author", "111")
        self.assertTrue(book.is_available())

        book.issue()
        self.assertFalse(book.is_available())

        book.return_book()
        self.assertTrue(book.is_available())


if __name__ == "__main__":
    unittest.main()
