from langchain import OpenAI, SQLDatabase, SQLDatabaseChain
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from langchain.llms.openai import OpenAI
from langchain.agents import AgentExecutor
from dotenv import load_dotenv
import os

load_dotenv()

def create_rag_agent():
    db = SQLDatabase.from_uri(os.getenv("MYSQL_CONNECTION_STRING"))
    llm = OpenAI(temperature=0)
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)

    agent_executor = create_sql_agent(
        llm=llm,
        toolkit=toolkit,
        verbose=True,
        agent_type="zero-shot-react-description",
    )

    return agent_executor

def query_agent(agent, query):
    return agent.run(query)