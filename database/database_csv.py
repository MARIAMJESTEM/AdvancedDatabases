import pandas as pd
import numpy as np
from faker import Faker
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData
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
        category = pd.unique(self.book_df['category_id'])
        map_list = {a: b for a, b in zip(category, range(1, len(category) + 1))}
        self.book_df['category_id'] = self.book_df['category_id'].map(map_list)

        self.book_df.id = self.book_df.id.astype('int64')
        self.book_df.release_year = self.book_df.release_year.astype('int64')
        self.book_df.to_sql('book', con=self.engine, if_exists='append', index=False)

    def upload_category_data(self):
        self.category_df['name'] = self.category_df['name'].apply(lambda x: x[:20])
        self.category_df['description'] = self.category_df['description'].apply(lambda x: x[:200])
        self.category_df.to_sql('book_category', con=self.engine, if_exists='append', index=False)


def fill_database_with_data():
    db_string = "postgresql://postgres:postgres@localhost:5432/advanced_databases"
    engine = create_engine(db_string)
    DU = DatabaseUpload(engine, 'database/data/books_v2.csv', 'database/data/category.csv')
    DU.upload_data()
