# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 19:43:31 2020

@author: LENOVO
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import pandas as pd

books = pd.read_csv('dataset/books.csv', encoding = "ISO-8859-1")
books.head()

books.shape

ratings = pd.read_csv('dataset/ratings.csv', encoding = "ISO-8859-1")
ratings.head()

book_tags = pd.read_csv('dataset/book_tags.csv', encoding = "ISO-8859-1")
book_tags.head()

tags = pd.read_csv('dataset/tags.csv')
tags.tail()

tags_join_DF = pd.merge(book_tags, tags, left_on='tag_id', right_on='tag_id', how='inner')
tags_join_DF.head()

to_read = pd.read_csv('dataset/to_read.csv')
to_read.head()

books_with_tags = pd.merge(books, tags_join_DF, left_on='book_id', right_on='goodreads_book_id', how='inner')

tf1 = TfidfVectorizer(analyzer='word',ngram_range=(1, 2),min_df=0, stop_words='english')
tfidf_matrix1 = tf1.fit_transform(books_with_tags['tag_name'].head(10000))
cosine_sim1 = linear_kernel(tfidf_matrix1, tfidf_matrix1)

titles1 = books['title']
indices1 = pd.Series(books.index, index=books['title'])

# Function that get book recommendations based on the cosine similarity score of books tags
def tags_recommendations(title):
    idx = indices1[title]
    sim_scores = list(enumerate(cosine_sim1[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:21]
    book_indices = [i[0] for i in sim_scores]
    return titles.iloc[book_indices]


