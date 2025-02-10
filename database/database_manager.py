from langchain_core.tools import create_retriever_tool
from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_neo4j.vectorstores.neo4j_vector import Neo4jVector
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from database.connections import graph, neo4j_username, neo4j_password


async def create_graph(documents):
    llm_graph = ChatOpenAI(model="gpt-4o")
    llm_transformer = LLMGraphTransformer(
        llm=llm_graph,
        node_properties=True,
        relationship_properties=True,
        strict_mode=False
    )

    graph_documents = await llm_transformer.aconvert_to_graph_documents(documents)
    graph.add_graph_documents(
        graph_documents,
        baseEntityLabel=True,
        include_source=True
    )

    graph.refresh_schema()

    return True


def create_retriever():
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
    vector_index = Neo4jVector.from_existing_graph(
        embeddings,
        username=neo4j_username,
        password=neo4j_password,
        search_type="hybrid",
        node_label="Document",
        text_node_properties=["text"],
        embedding_node_property="embedding"
    )

    retriever = vector_index.as_retriever()
    retriever_tool = create_retriever_tool(
        retriever,
        name="Professor X",
        description="This will retrieve the information about the research paper"
    )

    return retriever_tool