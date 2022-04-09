import os
import csv


from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


def main():
    f = open("books.csv")
    reader = csv.reader(f)
    for isbn, title, author, publicationYear in reader:
        db.execute("INSERT INTO books (isbn, title, author, publicationYear) VALUES (:isbn, :title, :author, :publicationYear)",
                    {"isbn": isbn, "title": title, "author": author, "publicationYear": publicationYear})
        print(f"Added book with ISBN: {isbn}, title: {title}, author: {author}, publication year: {publicationYear}")
    db.commit()

if __name__ == "__main__":
    main()