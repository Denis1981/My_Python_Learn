from .utils.data_validation import validate_book_data
from .utils.formatting import format_book_data

class Library:
    def __init__(self):
        self.books = []

    def add_book(self, book_data: dict):
        if validate_book_data(book_data):
            self.books.append(book_data)
        else:
            raise ValueError("Invalid book data")

    def remove_book(self, title: str):
        self.books = [book for book in self.books if book["title"] != title]

    def find_by_title(self, title: str):
        return [book for book in self.books if book["title"] == title]

    def find_by_author(self, author: str):
        return [book for book in self.books if book["author"] == author]

    def find_by_genre(self, genre: str):
        return [book for book in self.books if book["genre"] == genre]

    def view_all_books(self):
        return self.books
