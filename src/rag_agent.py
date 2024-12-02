from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_core.tools import Tool
from langchain.agents import initialize_agent, AgentType
from dotenv import load_dotenv
import os

load_dotenv()

def create_rag_agent():
    # SQL-Datenbankverbindung
    db = SQLDatabase.from_uri(os.getenv("MYSQL_CONNECTION_STRING"))

    # LLM-Instanz
    llm = ChatOpenAI(temperature=0)

    # SQL-Toolkit
    sql_toolkit = SQLDatabaseToolkit(db=db, llm=llm)

    # SQL-Tool
    sql_tool = Tool(
        name="SQL Database",
        func=SQLDatabaseChain(llm=llm, database=db, verbose=True).run,
        description="Useful for querying the SQL database for factual information."
    )

    # Hier können Sie in Zukunft weitere Tools hinzufügen
    tools = [sql_tool]

    # Agent erstellen
    agent = initialize_agent(
        tools,
        llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True
    )

    return agent

def query_agent(agent, query: str):
    try:
        response = agent.invoke(query)
        return response
    except Exception as e:
        return f"Ein Fehler ist aufgetreten: {str(e)}"