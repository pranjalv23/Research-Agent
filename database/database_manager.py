import arxiv
from langchain_neo4j import Neo4jGraph
from langchain_neo4j.vectorstores.neo4j_vector import Neo4jVector


class DB(object):
    db_name = "newsscraper"

    news_col_name = "newsarticles_dev"

    summarizer_db = mongo_client[db_name]

    summarizer_col = summarizer_db[news_col_name]


def doc_from_attachements():
    pass


def load_documents():
    pass
