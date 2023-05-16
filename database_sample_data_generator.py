from faker import Faker
from random import uniform
from sqlalchemy import create_engine
from database_queries import DatabaseQueries
import numpy as np


class DatabaseDataGenerator:
    def __init__(self, query: DatabaseQueries):
        """
        A class for generating sample data for a database.

        :param
            query (DatabaseQueries): An instance of the DatabaseQueries class used to interact with the database.
        """
        self.query: DatabaseQueries = query

    def generate_sample_data(self) -> None:
        """
        Generates sample data for users and reviews.

        :return: None

        Description:
            This method generates sample data by calling the 'generate_users', 'generate_books and 'generate_reviews' methods.
            It specifies the number of users = 3, books = 10 and reviews = 10 to generate.
        """
        self.generate_users(number_of_users=3)
        self.generate_read_books(number_of_read_books=10)
        self.generate_reviews(number_of_reviews=10)

    def generate_users(self, number_of_users: int) -> None:
        """
        Generates new user accounts and adds them to a database.

        :param number_of_users: The number of user accounts to generate.
        :return: None

        Description:
            This function generates new user accounts using the Faker library and adds them to a database
            using the add_new_user_to_database method of the DatabaseQueries class.

            Each new user account is assigned a random username, password, and email address generated by the Faker library.
            The number of user accounts to generate is specified by the number_of_users argument.
        """
        [self.query.add_new_user_to_database(username=Faker().user_name(),
                                             password=Faker().password(length=5),
                                             email=Faker().email()) for _ in range(number_of_users)]

    def generate_read_books(self, number_of_read_books: int) -> None:
        """Generates new records of read books and associates them with random users.

        :param number_of_read_books: The number of read book records to generate.
        :return: None

        Description:
            This method generates new records of read books and associates them with random users
            using the 'add_read_book_to_user_list' method of the 'DatabaseQueries' class.

            The method retrieves a random username and book title using the 'get_random_username'
            and 'get_random_book_title' methods of the 'DatabaseQueries' class.
            It then adds a read book record to the user's list.
        """
        [self.query.add_read_book_to_user_list(self.query.get_random_username(),
                                               self.query.get_random_book_title()) for _ in range(number_of_read_books)]

    def generate_reviews(self, number_of_reviews: int) -> None:
        """
        Generates new reviews and associates them with random users and books.

        :param number_of_reviews: The number of reviews to generate.
        :return: None

        Description:
            This method generates new reviews using the Faker library and associates them with random users and books
            using the 'add_review_to_user_book' method of the 'DatabaseQueries' class.

            Each review is assigned a random rating from the range of 0 to 5 (inclusive) with a step of 0.5,
            and a random comment generated by the Faker library.
            The number of reviews to generate is specified by the 'number_of_reviews' argument.
        """
        for _ in range(number_of_reviews):
            username = self.query.get_random_username()
            book_title = self.query.get_random_book_title()
            self.query.add_read_book_to_user_list(username=username, book_title=book_title)
            self.query.add_review_to_user_book(username=username,
                                               book_title=book_title,
                                               rating=np.random.choice(np.arange(0, 5.5, 0.5)),
                                               comment=Faker().text(max_nb_chars=200))


if __name__ == "__main__":
    db_string = "postgresql://postgres:postgres@localhost:5432/advanced_databases"
    engine = create_engine(db_string)
    DDG = DatabaseDataGenerator(DatabaseQueries(engine))
    DDG.generate_sample_data()
