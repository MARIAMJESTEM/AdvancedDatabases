import pandas as pd
import numpy as np
from faker import Faker


def make_book_and_category_database(data):
    usecols = ["categories", "title", "authors", "description", "published_year"]
    df = pd.read_csv(data, usecols=usecols, sep=';')
    df.rename(columns={"categories": "category_id", "authors": "author", "published_year": "release_year"},
              inplace=True)
    # drop all nan
    df.dropna(inplace=True, ignore_index=True)

    drop_list = []
    for i in range(len(df)):
        if len(df['title'][i]) > 30 or len(df['author'][i]) > 30 or len(df['description'][i]) > 400:
            drop_list.append(i)

    df.drop(drop_list, axis=0, inplace=True)
    df = df.reset_index(drop=True)

    category = pd.unique(df['category_id'])
    map_list = {a: b for a, b in zip(category, range(1, len(category) + 1))}  # map category
    df['category_id'] = df['category_id'].map(map_list)
    df.insert(0, "id", np.linspace(1, len(df), num=len(df)))
    df = df[['id', 'category_id', 'title', 'author', 'description', 'release_year']]

    df.id = df.id.astype('int64')
    df.release_year = df.release_year.astype('int64')
    df.to_csv('data/books_v2.csv', index=False)

    df2 = pd.DataFrame()
    df2['id'] = map_list
    df2['name'] = category
    df2['description'] = Faker().text(100)
    df2.to_csv('data/category.csv', index=False)


def make_category_database(data):
    print(make_book_database(data).category)


if __name__ == "__main__":
    make_book_and_category_database('data/books.csv')
