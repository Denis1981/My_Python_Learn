def validate_book_data(data: dict) -> bool:
    required_fields = {"title", "author", "genre"}
    return all(field in data and isinstance(data[field], str) and data[field] for field in required_fields)
