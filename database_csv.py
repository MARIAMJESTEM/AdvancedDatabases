import pandas as pd
import numpy as np
from faker import Faker
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData
import database_architecture

db_string = "postgresql://postgres:postgres@localhost:5433/advanced_databases"
engine = create_engine(db_string)

usecols = ["id","category_id","title", "author", "description", "release_year"]
df = pd.read_csv('books_v2.csv', usecols=usecols)
category = pd.unique(df['category_id'])
map_list = {a : b for a,b in zip(category,range(1,len(category) + 1))} # map category
df['category_id'] = df['category_id'].map(map_list)
# print(df.info())

df2 = pd.read_csv('category.csv')

df.id = df.id.astype('int64')
df.release_year = df.release_year.astype('int64')
df.to_sql('book', con = engine, if_exists='append', index=False)
df2.to_sql('book_category', con = engine, if_exists='append', index=False)






