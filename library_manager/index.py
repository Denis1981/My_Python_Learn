import sys
sys.path.append("./")

from library_manager import Library, generate_report


lib = Library()


lib.add_book({"title": "1984", "author": "George Orwell", "genre": "Dystopia"})
lib.add_book({"title": "Python 101", "author": "John Smith", "genre": "Programming"})
lib.add_book({"title": "Harry Potter", "author": "J.K. Rowling", "genre": "Fantasy"})


print("Все книги в библиотеке:")
for book in lib.view_all_books():
    print(book)


print("\nПоиск по автору 'George Orwell':")
print(lib.find_by_author("George Orwell"))

print("\nПоиск по жанру 'Fantasy':")
print(lib.find_by_genre("Fantasy"))


lib.remove_book("1984")
print("\nКниги после удаления '1984':")
for book in lib.view_all_books():
    print(book)


print("\nОтчет по библиотеке:")
print(generate_report(lib))
