import pandas as pd
import numpy as np
from faker import Faker
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData
import database_architecture
from sqlalchemy.engine import Engine


class DatabaseUpload:
    def __init__(self, engine: Engine, book_data_csv: str, category_data_csv: str):
        self.engine = engine
        self.book_df = pd.read_csv(book_data_csv,
                                   usecols=["id", "category_id", "title", "author", "description", "release_year"])
        self.category_df = pd.read_csv(category_data_csv)

    def upload_data(self):
        self.upload_category_data()
        self.upload_books_data()

    def upload_books_data(self):
        self.book_df.to_sql('book', con=engine, if_exists='append', index=False)

    def upload_category_data(self):
        self.category_df.to_sql('book_category', con=self.engine, if_exists='append', index=False)


if __name__ == "__main__":
    db_string = "postgresql://postgres:postgres@localhost:5432/advanced_databases"
    engine = create_engine(db_string)
    DU = DatabaseUpload(engine, 'data/books_v2.csv', 'data/category.csv')
    DU.upload_data()
