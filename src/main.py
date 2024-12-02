from langchain.callbacks.manager import tracing_v2_enabled
from rag_agent import create_rag_agent, query_agent
from langsmith import Client
from langchain.callbacks.tracers.langchain import LangChainTracer
from dotenv import load_dotenv
import os

load_dotenv()

def main():
    agent = create_rag_agent()

    queries = [
        "Welche Tabellen gibt es in der Datenbank?",
        "Gib die Tabellen und ihre Wert-Spalten an, welche in der Datenbank vorhanden sind."
    ]

    for query in queries:
        print(f"Query: {query}")
        result = query_agent(agent, query)
        print(f"Result: {result}")
        print("---")

if __name__ == "__main__":
    main()