import abc
import pickle
import os

# Имя файла для хранения данных
DATA_FILE = "library_data.pkl"


class Person(metaclass=abc.ABCMeta):
    def __init__(self, name):
        self.__name = name

    def get_name(self):
        return self.__name

    @abc.abstractmethod
    def get_role(self):
        pass


class Librarian(Person):
    def get_role(self):
        return "Библиотекарь"


class User(Person):
    def __init__(self, name):
        super().__init__(name)
        self.__borrowed_books = []

    def borrow_book(self, book_title):
        self.__borrowed_books.append(book_title)

    def return_book(self, book_title):
        if book_title in self.__borrowed_books:
            self.__borrowed_books.remove(book_title)
            return True
        return False

    def get_borrowed_books(self):
        return self.__borrowed_books.copy()

    def get_role(self):
        return "Пользователь"


class Book:
    def __init__(self, title, author, status="доступна"):
        self.__title = title
        self.__author = author
        self.__status = status

    def get_title(self):
        return self.__title

    def get_author(self):
        return self.__author

    def get_status(self):
        return self.__status

    def set_status(self, new_status):
        if new_status in ["доступна", "выдана"]:
            self.__status = new_status

    def __str__(self):
        return f"«{self.__title}» ({self.__author}) - {self.__status}"


class Library:
    def __init__(self):
        self.__books = []
        self.__users = []
        self.__librarians = []

    def save_data(self):
        """Сохраняет состояние библиотеки в бинарный файл с помощью pickle."""
        try:
            # Собираем данные в словарь для удобства сериализации
            data = {
                'books': self.__books,
                'users': self.__users,
                'librarians': self.__librarians
            }
            with open(DATA_FILE, "wb") as f:
                pickle.dump(data, f)
            print(f"[Система] Данные успешно сохранены в {DATA_FILE}")
        except Exception as e:
            print(f"[Ошибка] Не удалось сохранить данные: {e}")

    def load_data(self):
        """Загружает состояние библиотеки из бинарного файла."""
        if not os.path.exists(DATA_FILE):
            print("[Система] Файл данных не найден. Создается новая библиотека.")
            # Создаем администратора по умолчанию, если база пустая
            self.__librarians.append(Librarian("Администратор"))
            return

        try:
            with open(DATA_FILE, "rb") as f:
                data = pickle.load(f)
                self.__books = data.get('books', [])
                self.__users = data.get('users', [])
                self.__librarians = data.get('librarians', [])

            # Гарантируем наличие хотя бы одного библиотекаря
            if not self.__librarians:
                self.__librarians.append(Librarian("Администратор"))

            print(f"[Система] Данные успешно загружены из {DATA_FILE}")
            print(f"[Система] Найдено книг: {len(self.__books)}, Пользователей: {len(self.__users)}")
        except Exception as e:
            print(f"[Ошибка] Не удалось загрузить данные: {e}")
            print("[Система] Инициализация пустой библиотеки.")
            self.__librarians.append(Librarian("Администратор"))

    def add_book(self, title, author):
        # Проверка на дубликат
        if self.get_book(title):
            return "Такая книга уже существует в каталоге"
        self.__books.append(Book(title, author, "доступна"))
        return "Книга добавлена"

    def remove_book(self, title):
        """
        ИСПРАВЛЕНИЕ БАГА:
        Теперь метод проверяет, не выдана ли книга пользователю, перед удалением.
        """
        book = self.get_book(title)
        if not book:
            return "Книга не найдена"

        if book.get_status() == "выдана":
            return "Ошибка: Нельзя удалить книгу, которая сейчас выдана пользователю!"

        self.__books.remove(book)
        return "Книга удалена"

    def register_user(self, name):
        for user in self.__users:
            if user.get_name().lower() == name.lower():
                return "Пользователь уже существует"
        self.__users.append(User(name))
        return "Пользователь зарегистрирован"

    def list_all_users(self):
        return self.__users

    def list_all_books(self):
        return self.__books

    def get_user(self, name):
        for user in self.__users:
            if user.get_name().lower() == name.lower():
                return user
        return None

    def get_book(self, title):
        for book in self.__books:
            if book.get_title().lower() == title.lower():
                return book
        return None

    def get_available_books(self):
        return [book for book in self.__books if book.get_status() == "доступна"]

    def borrow_book(self, user_name, book_title):
        user = self.get_user(user_name)
        book = self.get_book(book_title)

        if not user:
            return "Пользователь не найден"
        if not book:
            return "Книга не найдена"
        if book.get_status() != "доступна":
            return "Книга уже выдана другому пользователю"

        book.set_status("выдана")
        user.borrow_book(book.get_title())
        return f"Книга «{book.get_title()}» выдана пользователю {user.get_name()}"

    def return_book(self, user_name, book_title):
        user = self.get_user(user_name)
        book = self.get_book(book_title)

        if not user:
            return "Пользователь не найден"
        if not book:
            # Если книги нет в каталоге (например, удалили пока она была на руках - хотя теперь это запрещено)
            return "Книга не найдена в каталоге"

        if book_title not in user.get_borrowed_books():
            return "Этот пользователь не брал данную книгу"

        book.set_status("доступна")
        user.return_book(book.get_title())
        return f"Книга «{book.get_title()}» возвращена в библиотеку"


def main():
    library = Library()
    library.load_data()

    print("=" * 50)
    print("Добро пожаловать в систему управления библиотекой!")
    print("=" * 50)

    while True:
        role = input("\nВыберите роль (библиотекарь/пользователь/выход): ").strip().lower()

        if role == "выход":
            library.save_data()
            print("Данные сохранены. До свидания!")
            break

        elif role == "библиотекарь":
            print("\nРежим библиотекаря (доступны все функции)")

            while True:
                print("\nМеню библиотекаря:")
                print("1. Добавить книгу")
                print("2. Удалить книгу")
                print("3. Зарегистрировать пользователя")
                print("4. Показать всех пользователей")
                print("5. Показать все книги")
                print("0. Выйти в главное меню")

                choice = input("Ваш выбор: ").strip()

                if choice == "1":
                    title = input("Название книги: ").strip()
                    author = input("Автор: ").strip()
                    print(library.add_book(title, author))

                elif choice == "2":
                    title = input("Название книги для удаления: ").strip()
                    print(library.remove_book(title))

                elif choice == "3":
                    name = input("Имя нового пользователя: ").strip()
                    print(library.register_user(name))

                elif choice == "4":
                    users = library.list_all_users()
                    if not users:
                        print("Нет зарегистрированных пользователей")
                    else:
                        print("\nСписок пользователей:")
                        for i, user in enumerate(users, 1):
                            books = ", ".join(user.get_borrowed_books()) if user.get_borrowed_books() else "нет"
                            print(f"{i}. {user.get_name()} (взял книги: {books})")

                elif choice == "5":
                    books = library.list_all_books()
                    if not books:
                        print("Нет книг в библиотеке")
                    else:
                        print("\nСписок всех книг:")
                        for i, book in enumerate(books, 1):
                            print(f"{i}. {book}")

                elif choice == "0":
                    break

                else:
                    print("Неверный выбор. Попробуйте снова.")

        elif role == "пользователь":
            name = input("Введите ваше имя: ").strip()
            user = library.get_user(name)

            if not user:
                print("Пользователь не найден. Обратитесь к библиотекарю для регистрации.")
                continue

            print(f"\nЗдравствуйте, {user.get_name()}! Режим пользователя.")

            while True:
                print("\nМеню пользователя:")
                print("1. Показать доступные книги")
                print("2. Взять книгу")
                print("3. Вернуть книгу")
                print("4. Мои книги")
                print("0. Выйти в главное меню")

                choice = input("Ваш выбор: ").strip()

                if choice == "1":
                    books = library.get_available_books()
                    if not books:
                        print("Нет доступных книг")
                    else:
                        print("\nДоступные книги:")
                        for i, book in enumerate(books, 1):
                            print(f"{i}. {book}")

                elif choice == "2":
                    title = input("Название книги для взятия: ").strip()
                    print(library.borrow_book(name, title))

                elif choice == "3":
                    title = input("Название книги для возврата: ").strip()
                    print(library.return_book(name, title))

                elif choice == "4":
                    books = user.get_borrowed_books()
                    if not books:
                        print("У вас нет взятых книг")
                    else:
                        print("\nВаши книги:")
                        for i, book_title in enumerate(books, 1):
                            print(f"{i}. {book_title}")

                elif choice == "0":
                    break

                else:
                    print("Неверный выбор. Попробуйте снова.")

        else:
            print("Неверная роль. Выберите 'библиотекарь', 'пользователь' или 'выход'.")


if __name__ == "__main__":
    main()