# --- Пользовательские исключения ---
class UserAlreadyExistsError(Exception):
    """Исключение: пользователь с данным username уже существует."""
    def __init__(self, username):
        super().__init__(f"Пользователь с именем '{username}' уже существует.")


class UserNotFoundError(Exception):
    """Исключение: пользователь с данным username не найден."""
    def __init__(self, username):
        super().__init__(f"Пользователь с именем '{username}' не найден.")


# --- Класс User ---
class User:
    def __init__(self, username: str, email: str, age: int):
        self.username = username
        self.email = email
        self.age = age

    def __str__(self):
        return f"User(username='{self.username}', email='{self.email}', age={self.age})"


# --- Класс UserManager ---
class UserManager:
    def __init__(self):
        # Словарь: ключ — username, значение — объект User
        self.users: dict[str, User] = {}

    def add_user(self, user: User):
        """
        Добавляет пользователя в словарь.
        Если username уже занят, выбрасывает UserAlreadyExistsError.
        """
        if user.username in self.users:
            raise UserAlreadyExistsError(user.username)
        self.users[user.username] = user

    def remove_user(self, username: str):
        """
        Удаляет пользователя из словаря по его username.
        Если пользователя нет — выбрасывает UserNotFoundError.
        """
        if username not in self.users:
            raise UserNotFoundError(username)
        del self.users[username]

    def find_user(self, username: str) -> User:
        """
        Возвращает объект User по username.
        Если пользователя нет — выбрасывает UserNotFoundError.
        """
        if username not in self.users:
            raise UserNotFoundError(username)
        return self.users[username]


# --- Основная функция для демонстрации работы ---
def main():
    manager = UserManager()

    # --- 1. Добавление пользователей ---
    print("=== Добавление пользователей ===")
    user1 = User("ivan", "ivan@example.com", 30)
    user2 = User("anna", "anna@example.com", 25)
    user3 = User("ivan", "ivan2@example.com", 40)  # Повторяющийся username "ivan"

    try:
        manager.add_user(user1)
        print(f"Добавлен: {user1}")
    except UserAlreadyExistsError as e:
        print(f"Ошибка при добавлении: {e}")

    try:
        manager.add_user(user2)
        print(f"Добавлен: {user2}")
    except UserAlreadyExistsError as e:
        print(f"Ошибка при добавлении: {e}")

    try:
        manager.add_user(user3)
        print(f"Добавлен: {user3}")
    except UserAlreadyExistsError as e:
        print(f"Ошибка при добавлении: {e}")

    # --- 2. Удаление пользователей ---
    print("\n=== Удаление пользователей ===")
    try:
        manager.remove_user("anna")
        print("Пользователь 'anna' успешно удалён.")
    except UserNotFoundError as e:
        print(f"Ошибка при удалении: {e}")

    try:
        manager.remove_user("oleg")
        print("Пользователь 'oleg' успешно удалён.")
    except UserNotFoundError as e:
        print(f"Ошибка при удалении: {e}")

    # --- 3. Поиск пользователей ---
    print("\n=== Поиск пользователей ===")
    try:
        found_user = manager.find_user("ivan")
        print(f"Найден пользователь: {found_user}")
    except UserNotFoundError as e:
        print(f"Ошибка при поиске: {e}")

    try:
        found_user = manager.find_user("maria")
        print(f"Найден пользователь: {found_user}")
    except UserNotFoundError as e:
        print(f"Ошибка при поиске: {e}")


if __name__ == "__main__":
    main()
