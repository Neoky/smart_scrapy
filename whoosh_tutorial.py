# Tutorial/Code from https://annamarbut.blogspot.com/2018/08/whoosh-pandas-and-redshift-implementing.html


import os
from whoosh.fields import Schema, TEXT, KEYWORD, ID, STORED
from whoosh.analysis import StemmingAnalyzer
from whoosh import index
from whoosh.qparser import QueryParser
import pandas as pd
from whoosh import sorting
from whoosh import qparser
from pprint import pprint

df = pd.read_csv("processed.csv")

schema = Schema(summary=TEXT(stored=True, analyzer=StemmingAnalyzer()),
                content=TEXT(stored=True, analyzer=StemmingAnalyzer()),
                topic_keywords=TEXT(stored=True, field_boost=4.0),
                url=TEXT(stored=True),
                tags=KEYWORD)


# create and populate index
def populate_index(dirname, dataframe, sch):
    # Checks for existing index path and creates one if not present
    if not os.path.exists(dirname):
        os.mkdir(dirname)
    print("Creating the Index")
    ix = index.create_in(dirname, sch)
    with ix.writer() as writer:
        # Imports stories from pandas df
        print("Populating the Index")
        for i in dataframe.index:
            add_stories(i, dataframe, writer)


def add_stories(i, dataframe, writer):
    writer.update_document(summary=str(dataframe.loc[i, "summary"]),
                           content=str(dataframe.loc[i, "content"]),
                           topic_keywords=str(dataframe.loc[i, "Topic_Keywords"]),
                           url=str(dataframe.loc[i, "url"]))


populate_index("index", df, schema)


def index_search(dirname, search_fields, search_query):
    ix = index.open_dir(dirname)
    sch = ix.schema
    # Create query parser that looks through designated fields in index
    og = qparser.OrGroup.factory(0.9)
    mp = qparser.MultifieldParser(search_fields, sch, group=og)

    # This is the user query
    q = mp.parse(search_query)

    # Actual searcher, prints top 10 hits
    with ix.searcher() as s:
        results = s.search(q, limit=10)
        print("Search Results: ")
        pprint(results[0:10])

index_search("index", ['content', 'topic_keywords'], u"search term")