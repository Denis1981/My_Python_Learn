from .utils.formatting import format_book_data

def generate_report(library):
    report_lines = []
    for book in library.view_all_books():
        report_lines.append(format_book_data(book))
    return "\n".join(report_lines)
