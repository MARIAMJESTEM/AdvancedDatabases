import pandas as pd
import numpy as np
from sqlalchemy import create_engine,MetaData, Table
import database_architecture

db_string = "postgresql://postgres:postgres@localhost:5432/advanced_databases"
engine = create_engine(db_string)

usecols = ["id","category_id","title", "author", "description", "release_year"]
df = pd.read_csv('books_v2.csv', usecols=usecols)
category = pd.unique(df['category_id'])
map_list = {a : b for a,b in zip(category,range(1,len(category)))} # map category
df['category_id'] = df['category_id'].map(map_list)

df.to_sql('book', con = engine, if_exists='replace', index=False)


# df.to_sql(name = df, con = engine, if_exists = 'replace', index = False)






