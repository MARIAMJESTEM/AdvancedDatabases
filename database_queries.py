import pandas as pd
from pandas import DataFrame
from typing import List, Dict, Any
from sqlalchemy import MetaData, Table, select, func, desc, update, or_
from sqlalchemy.engine import Engine
from datetime import datetime


class DatabaseQueries:
    def __init__(self, engine: Engine):
        """
        A class for performing database queries.

        :param engine: The SQLAlchemy engine to use for connecting to the database.
        """
        self.engine = engine

        self.user = Table('user', MetaData(), autoload=True, autoload_with=engine)
        self.book = Table('book', MetaData(), autoload=True, autoload_with=engine)
        self.review = Table('review', MetaData(), autoload=True, autoload_with=engine)
        self.book_category = Table('book_category', MetaData(), autoload=True, autoload_with=engine)
        self.readership_status = Table('readership_status', MetaData(), autoload=True, autoload_with=engine)

    def check_user_exists(self, username: str, email: str) -> bool:
        """
        Check if a user with the given username exists in the database.

        :param username: The name of the user to check.
        :param email: The email connected to the username.
        :return: True if the user exists in the database, False otherwise.
        """

        stmt = (
            select([self.user])
            .where(self.user.columns.username == username)
            .where(self.user.columns.email == email)
        )
        return True if self.engine.execute(stmt).fetchall() else False

    def check_book_exists(self, book_title: str) -> bool:
        """
        Check if book with selected title exists in the database.

        :param book_title: The title of the book to check
        :return: True if the book exists in the database, False otherwise.
        """
        stmt = (
            select([self.book])
            .where(func.lower(self.book.columns.title) == book_title.lower())
        )
        return True if self.engine.execute(stmt).fetchall() else False

    def check_is_username_taken(self, username: str) -> bool:
        """
        Check if the given username was taken in the database.

        :param username: The name of the user to check.
        :return: True if the username is taken, False otherwise.
        """

        stmt = (
            select([self.user])
            .where(self.user.columns.username == username)
        )
        return True if self.engine.execute(stmt).fetchall() else False

    def check_is_email_taken(self, email: str) -> bool:
        """
        Check if the given email was taken in the database.

        :param email: The name of the user to check.
        :return: True if the email is taken, False otherwise.
        """

        stmt = (
            select([self.user])
            .where(self.user.columns.email == email)
        )
        return True if self.engine.execute(stmt).fetchall() else False

    def check_user_password(self, username: str, password: str) -> bool:
        """
        Check if the given password matches the password of the specified user in the database.

        :param username: The username of the user to check the password for.
        :param password: The password to check for the specified user.
        :return: True if the given password matches the password of the specified user in the database, False otherwise.
        """

        stmt = (
            select([self.user])
            .where(self.user.columns.username == username)
            .where(self.user.columns.password == password)
        )
        return True if self.engine.execute(stmt).fetchall() else False

    def check_is_title_in_user_database(self, username: str, book_title: str) -> bool:
        """
        Check if the given book title exists in the specified user's database.

        :param username: The username of the user to check the database for.
        :param book_title: The title of the book to check for in the user's database.
        :return: True if the given book title exists in the user's database, False otherwise.
        """

        stmt = (
            select([self.readership_status])
            .select_from(
                self.readership_status
                .join(self.book, self.readership_status.columns.book_id == self.book.columns.id)
            )
            .where(self.readership_status.columns.user_id == self.get_user_id(username))
            .where(self.book.columns.title == book_title)
        )
        return True if self.engine.execute(stmt).fetchall() else False

    def get_top_rated_books(self, number_of_top_rated_books: int) -> DataFrame:
        """
        Returns a pandas DataFrame containing the top-rated books and their total rating.

        :param number_of_top_rated_books: An integer representing the number of selecting top-rated books.
        :return: pd.DataFrame: A pandas DataFrame containing the top-rated books and their total rating.
        """

        stmt = (
            select([
                self.book.columns.title,
                self.book.columns.author,
                self.book_category.columns.name,
                self.review.columns.book_id,
                func.avg(self.review.columns.rating).label('total_rating')
            ])
            .select_from(
                self.book
                .join(self.review, self.book.columns.id == self.review.columns.book_id)
                .join(self.book_category, self.book_category.columns.id == self.book.columns.category_id)
            )
            .group_by(
                self.book.columns.title,
                self.book.columns.author,
                self.book_category.columns.name,
                self.review.columns.book_id
            )
            .order_by(desc('total_rating'))
            .limit(number_of_top_rated_books)
        )
        return pd.DataFrame(self.engine.execute(stmt).fetchall())

    def get_user_read_books(self, username: str) -> List[Dict]:
        """
        Returns a list of dictionaries containing the titles of all books read by the given user.

        :param username: Username of the user whose read books are to be returned.
        :return: List[Dict]: List of dictionaries with titles, author, genre, and release_year of all books read by the given user.
        """

        stmt = (
            select([
                self.book.columns.title,
                self.book.columns.author,
                self.book_category.columns.name.label('genre'),
                self.book.columns.release_year
            ])
            .select_from(
                self.book
                .join(self.readership_status, self.book.columns.id == self.readership_status.columns.book_id)
                .join(self.user, self.readership_status.columns.user_id == self.user.columns.id)
                .join(self.book_category, self.book_category.columns.id == self.book.columns.category_id)
            )
            .where(self.user.columns.username == username)
            .where(
                or_(
                    self.readership_status.columns.status == 'READ',
                    self.readership_status.columns.status == 'REVIEWED'
                )
            )
        )
        return pd.DataFrame(self.engine.execute(stmt).fetchall()).to_dict(orient='records')

    def get_user_reviews(self, username: str) -> List[Dict]:
        """
        Returns a list of dictionaries with reviews for all books read by the given user.

        :param username: Username of the user whose reviewed books are to be returned.
        :return: List[Dict]: List of dictionaries with reviews for all books read by the given user.
        """

        stmt = (
            select([
                self.book.columns.title,
                self.review.columns.rating,
                self.review.columns.comment
            ])
            .select_from(
                self.review
                .join(self.readership_status, self.review.columns.id == self.readership_status.columns.review_id)
                .join(self.user, self.readership_status.columns.user_id == self.user.columns.id)
                .join(self.book, self.readership_status.columns.book_id == self.book.columns.id)
            )
            .where(self.user.columns.username == username)
            .where(self.readership_status.columns.status == 'REVIEWED')
        )
        return pd.DataFrame(self.engine.execute(stmt).fetchall()).to_dict(orient='records')

    def get_book_reviews(self, book_title: str) -> List[Dict]:
        """
        Retrieves reviews for the book with the given title from the database.

        :param book_title: The title of the book to retrieve reviews for.
        :return: A list of dictionaries, where each dictionary contains the following keys:
                 "book_title", "rating", and "comment".
        """
        stmt = (
            select([
                self.book.columns.title,
                self.review.columns.rating,
                self.review.columns.comment
            ])
            .select_from(
                self.book
                .join(self.review, self.book.columns.id == self.review.columns.book_id)
            )
            .where(self.book.columns.title == book_title)
        )

        return pd.DataFrame(self.engine.execute(stmt).fetchall()).to_dict(orient='records')

    def get_search_book_by_title(self, book_title: str) -> List[Any]:
        """
        Searches for books in the database that match the given title.

        :param book_title: The title of the book to search for.
        :return: A list containing information about the matching books, where each item in the list is a tuple with the
                 following fields: (title, author, description, release_year, category_name).
        """

        stmt = (
            select([
                self.book.columns.title,
                self.book.columns.author,
                self.book.columns.description,
                self.book.columns.release_year,
                self.book_category.columns.name
            ])
            .select_from(
                self.book.join(self.book_category, self.book.columns.category_id == self.book_category.columns.id)
            )
            .where(func.lower(self.book.columns.title) == book_title.lower())
        )
        book_information = self.engine.execute(stmt).fetchall()
        if not book_information:
            raise ValueError(f"ERROR: no book with the given title was found: '{book_title}'")
        return list(book_information[0])

    def get_new_user_id(self) -> int:
        """
        Retrieves the new index value for the user table by getting the maximum ID from the table and incrementing it by 1.
        If there are no entries in the table, returns 0.

        :return: The new index value for the user table
        """

        stmt = (
            select(func.max(self.user.columns.id))
        )
        new_id = self.engine.execute(stmt).fetchall()[0][0]
        if new_id is not None:
            return new_id + 1
        return 0

    def get_new_readership_status_id(self) -> int:
        stmt = (
            select(func.max(self.readership_status.columns.id))
        )
        new_id = self.engine.execute(stmt).fetchall()[0][0]
        if new_id is not None:
            return new_id + 1
        return 0

    def get_new_review_id(self) -> int:
        stmt = (
            select(func.max(self.review.columns.id))
        )
        new_id = self.engine.execute(stmt).fetchall()[0][0]
        if new_id is not None:
            return new_id + 1
        return 0

    def get_user_id(self, username: str) -> int:
        stmt = (
            select(self.user.columns.id)
            .where(self.user.columns.username == username)
        )
        return self.engine.execute(stmt).fetchall()[0][0]

    def get_book_id(self, book_title: str) -> int:
        stmt = (
            select(self.book.columns.id)
            .where(self.book.columns.title == book_title)
        )
        return self.engine.execute(stmt).fetchall()[0][0]

    def add_new_user_to_database(self, username: str, password: str, email: str) -> None:
        """
        Add a new user to the database.

        :param username: Username of the new user
        :param password: Password of the new user
        :param email: Email of the new user

        :return: None
        """

        insert_stmt = self.user.insert().values(id=self.get_new_user_id(),
                                                username=username,
                                                password=password,
                                                email=email,
                                                register_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        self.engine.execute(insert_stmt)

    def add_read_book_to_user_list(self, username: str, book_title: str) -> None:
        """
        Adds a book by a user to their list of read books.

        :param username: Username of the user who read the book.
        :param book_title: The title of the book.

        :return: None
        """

        insert_stmt = self.readership_status.insert().values(id=self.get_new_readership_status_id(),
                                                             user_id=self.get_user_id(username),
                                                             book_id=self.get_book_id(book_title),
                                                             review_id=None,
                                                             status='READ')
        self.engine.execute(insert_stmt)

    def add_review_to_user_book(self, username: str, book_title: str, rating: float, comment: str) -> None:
        """
        Add a new review to a book and update the user's reading status.

        :param username: The username of the user who read the book.
        :param book_title: The title of the book.
        :param rating: The rating of the book as a float value from 0 to 5.
        :param comment: The comment about the book.

        :return: None
        """
        if rating < 0 or rating > 5:
            raise ValueError("ERROR: Rating value must be between 0 and 5.")

        new_review_id = self.get_new_review_id()

        self.add_new_review(review_id=new_review_id,
                            user_id=self.get_user_id(username),
                            book_id=self.get_book_id(book_title),
                            rating=rating,
                            comment=comment)

        self.update_readership_status_with_review(user_id=self.get_user_id(username),
                                                  book_id=self.get_book_id(book_title),
                                                  review_id=new_review_id)

    def add_new_review(self, review_id: int, user_id: int, book_id: int, rating: float, comment: str) -> None:
        """
        Add a new review to the 'review' table in the database.

        :param review_id: The unique identifier of the review.
        :param user_id: The unique identifier of the user.
        :param book_id: The unique identifier of the reviewed book.
        :param rating: The rating of the book as a float value from 0 to 5.
        :param comment: The comment about the book.

        :return: None
        """

        insert_stmt = self.review.insert().values(id=review_id,
                                                  user_id=user_id,
                                                  book_id=book_id,
                                                  rating=rating,
                                                  comment=comment,
                                                  added_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        self.engine.execute(insert_stmt)

    def update_readership_status_with_review(self, user_id: int, book_id: int, review_id: int) -> None:
        """
        Update the reading status of a book to 'REVIEWED' and assign a review ID.

        :param user_id: The unique identifier of the user.
        :param book_id: The unique identifier of the reviewed book.
        :param review_id: The unique identifier of the review.

        :return: None
        """

        update_stmt = (
            update(self.readership_status)
            .values(status='REVIEWED', review_id=review_id)
            .where(self.readership_status.columns.book_id == book_id)
            .where(self.readership_status.columns.user_id == user_id)
        )
        self.engine.execute(update_stmt)
