from rag_agent import create_rag_agent, query_agent
from langsmith import Client
from dotenv import load_dotenv
import os

load_dotenv()

def main():
    # Initialize LangSmith client
    client = Client()

    # Create RAG agent
    agent = create_rag_agent()

    # Example query
    query = "How many users are in the database?"

    # Use LangSmith to trace the execution
    with client.tracing_v2_enabled():
        result = query_agent(agent, query)

    print(f"Query: {query}")
    print(f"Result: {result}")

if __name__ == "__main__":
    main()