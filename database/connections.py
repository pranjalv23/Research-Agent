import os

from dotenv import load_dotenv
from langchain_neo4j import Neo4jGraph

load_dotenv()

neo4j_uri = os.getenv('NEO4J_URI')
neo4j_password = os.getenv('NEO4J_PASSWORD')
neo4j_username = os.getenv('NEO4J_USERNAME')
aura_instanceid = os.getenv('AURA_INSTANCEID')
aura_instancename = os.getenv('AURA_INSTANCENAME')
llama_parse_api_key = os.getenv('LLAMA_CLOUD_API_KEY')

graph = Neo4jGraph(username=neo4j_username, password=neo4j_password)
