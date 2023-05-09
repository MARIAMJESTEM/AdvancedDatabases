from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey


db_string = "postgresql://postgres:postgres@localhost:5432/advanced_databases"
engine = create_engine(db_string)

Base = declarative_base()


class Customer(Base):
    __tablename__ = 'customer'
    id = Column(Integer, primary_key=True)
    username = Column(String(20))
    password = Column(String(20))
    email = Column(String(30))
    register_date = Column(Date)

    def __repr__(self):
        return "<Customer(id={0}, username={1}, password={2}, email={3}, register_date={4})>".format(self.id, self.username, self.password, self.email, self.register_date)


class BookCategory(Base):
    __tablename__ = 'book_category'
    id = Column(Integer, primary_key=True)
    name = Column(String(20))
    description = Column(String(200))

    def __repr__(self):
        return "<Book Category(id={0}, name={1}, description={2})>".format(self.id, self.name, self.description)


class Book(Base):
    __tablename__ = 'book'
    id = Column(Integer, primary_key=True)
    category_id = Column(Integer, ForeignKey('book_category.id'))
    title = Column(String(40))
    description = Column(String(400))
    release_year = Column(Date)

    def __repr__(self):
        return "<Book(id={0}, category_id={1}, title={2}, description={3}, release_year={4})>".format(self.id, self.category_id, self.title, self.description, self.release_year)


class Review(Base):
    __tablename__ = 'review'
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customer.id'))
    book_id = Column(Integer, ForeignKey('book.id'))
    rating = Column(Float)
    comment = Column(String(400))
    added_date = Column(Date)

    def __repr__(self):
        return "<Review(id={0}, customer_id={1}, book_id={2}, rating={3}, comment={4}, added_date={5})>".format(self.id, self.customer_id, self.book_id, self.rating, self.comment, self.added_date)


Base.metadata.create_all(engine)
