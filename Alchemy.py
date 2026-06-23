from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, func
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine("sqlite:///library.db", echo=True)
print(engine)

Base = declarative_base()


class Author(Base):
    __tablename__ = "authors"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    birth_year = Column(Integer)


class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    year = Column(Integer)
    author_id = Column(Integer, ForeignKey("authors.id"))


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

author1 = Author(name="Автор", birth_year=1888)
author2 = Author(name="Тоже автор", birth_year=1887)
author3 = Author(name="Ещё автор", birth_year=1886)

session.add_all([author1, author2, author3])
session.commit()

book1 = Book(title="Книга", year=1889, author_id=author1.id)
book2 = Book(title="Другая книга", year=1888, author_id=author1.id)
book3 = Book(title="Совсем другая книга", year=1898, author_id=author2.id)
book4 = Book(title="Почти такая же книга", year=1988, author_id=author2.id)
book5 = Book(title="Несовсем книга", year=1887, author_id=author3.id)

session.add_all([book1, book2, book3, book4, book5])
session.commit()

print("\nВсе авторы:")
authors = session.query(Author).all()
for author in authors:
    print(author.name)

author_to_update = session.query(Author).filter(Author.name == "Автор").first()
author_to_update.name = "АВТОР"
session.commit()

print("\nАвтор после изменения:")
print(f"{author_to_update.id}. {author_to_update.name} - {author_to_update.birth_year}")

book_to_delete = session.query(Book).filter(Book.title == "Несовсем книга").first()
session.delete(book_to_delete)
session.commit()

print("\nВсе книги, отсортированные по году (от новых к старым):")
books_sorted = session.query(Book).order_by(Book.year.desc()).all()
for book in books_sorted:
    print(f"{book.title} - {book.year} - author_id: {book.author_id}")

print("\nКниги, изданные после 1950 года:")
books_after_1950 = session.query(Book).filter(Book.year > 1950).all()
for book in books_after_1950:
    print(f"{book.title} - {book.year} - author_id: {book.author_id}")

print("\nАвтор по конкретному имени:")
author_by_name = session.query(Author).filter(Author.name == "Тоже автор").first()
print(f"{author_by_name.name} - {author_by_name.birth_year}")

books_count = session.query(func.count(Book.id)).scalar()
print(f"\nКоличество книг: {books_count}")

print("\nПервые 3 книги в алфавитном порядке:")
first_3_books = session.query(Book).order_by(Book.title).limit(3).all()
for book in first_3_books:
    print(f"{book.title} - {book.year} - author_id: {book.author_id}")

session.close()
