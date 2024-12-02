from langchain_openai import ChatOpenAI, OpenAI
from langchain_community.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from dotenv import load_dotenv
import os

load_dotenv()

def create_rag_agent():
    db = SQLDatabase.from_uri(os.getenv("MYSQL_CONNECTION_STRING"))
    llm = ChatOpenAI(temperature=0)
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)

    agent_executor = create_sql_agent(
        llm=llm,
        toolkit=toolkit,
        verbose=True,
        agent_type="zero-shot-react-description",
    )

    
    
    return agent_executor

def query_agent(agent, query):
    return agent.invoke(query)