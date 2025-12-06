# library_manager/__init__.py

"""
Library Manager package
Provides Book and LibraryInventory classes.
"""

from .book import Book
from .inventory import LibraryInventory

__all__ = ["Book", "LibraryInventory"]
