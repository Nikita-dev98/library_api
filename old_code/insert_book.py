from sqlalchemy.orm import Session
from datetime import date

from database import engine, localSession
import models

models.Base.metadata.create_all(bind=engine)

db: Session = localSession()

books = [
    models.Book(title="The Pragmatic Programmer", author="Andrew Hunt", isbn="978-0201616224", published_date=date(1999, 10, 20)),
    models.Book(title="Clean Code", author="Robert C. Martin", isbn="978-0132350884", published_date=date(2008, 8, 1)),
    models.Book(title="Design Patterns", author="Erich Gamma", isbn="978-0201633610", published_date=date(1994, 10, 21)),
    models.Book(title="Refactoring", author="Martin Fowler", isbn="978-0201485677", published_date=date(1999, 7, 8)),
    models.Book(title="Working Effectively with Legacy Code", author="Michael Feathers", isbn="978-0131177055", published_date=date(2004, 9, 30)),
    models.Book(title="Code Complete", author="Steve McConnell", isbn="978-0735619678", published_date=date(2004, 6, 9)),
    models.Book(title="Domain-Driven Design", author="Eric Evans", isbn="978-0321125217", published_date=date(2003, 8, 30)),
    models.Book(title="Test Driven Development: By Example", author="Kent Beck", isbn="978-0321146533", published_date=date(2002, 11, 8)),
    models.Book(title="Patterns of Enterprise Application Architecture", author="Martin Fowler", isbn="978-0321127426", published_date=date(2002, 11, 15)),
    models.Book(title="Head First Design Patterns", author="Eric Freeman", isbn="978-0596007126", published_date=date(2004, 10, 25)),
    models.Book(title="Continuous Delivery", author="Jez Humble", isbn="978-0321601919", published_date=date(2010, 7, 27)),
    models.Book(title="You Don’t Know JS", author="Kyle Simpson", isbn="978-1491904244", published_date=date(2014, 12, 27)),
    models.Book(title="Cracking the Coding Interview", author="Gayle Laakmann McDowell", isbn="978-0984782857", published_date=date(2015, 7, 1)),
    models.Book(title="Introduction to Algorithms", author="Thomas H. Cormen", isbn="978-0262033848", published_date=date(2009, 7, 31)),
    models.Book(title="Structure and Interpretation of Computer Programs", author="Harold Abelson", isbn="978-0262510875", published_date=date(1996, 7, 25)),
]

db.add_all(books)
db.commit()

db.close()