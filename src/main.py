from langchain.callbacks.manager import tracing_v2_enabled
from rag_agent import create_rag_agent, query_agent
from langsmith import Client
from langchain.callbacks.tracers.langchain import LangChainTracer
from dotenv import load_dotenv
import os

load_dotenv()

def main():
    # Initialize LangSmith client
    client = Client()

    # Create RAG agent
    agent = create_rag_agent()

    # Example query
# Liste von Abfragen für Batch-Verarbeitung
    queries = [
        "How many datapoints are in the database?",
        "What is the average value of column X?",
        "List the top 5 entries by column 1."
    ]
    
    # Batch-Verarbeitung mit Tracing
    results = [query_agent(agent, query) for query in queries]
    
    # Ausgabe der Ergebnisse
    for query, result in zip(queries, results):
        print(f"Query: {query}")
        print(f"Result: {result}")
        print("---")

if __name__ == "__main__":
    main()