from langchain.callbacks.manager import tracing_v2_enabled
from rag_agent import create_rag_agent, query_agent
from dotenv import load_dotenv
import os

from langsmith import Client
from langchain.callbacks.tracers.langchain import LangChainTracer

# Lade Umgebungsvariablen aus der .env Datei
load_dotenv()

def main():
    client = Client()
    tracer = LangChainTracer(project_name=os.getenv("LANGCHAIN_PROJECT"))
    
    # Erstelle den RAG-Agenten
    agent = create_rag_agent()
    
    # Liste von Abfragen, die an den Agenten gesendet werden sollen
    queries = [
        "Welche Tabellen gibt es in der Datenbank?",
        "Wie zufrieden sind die Mitarbeitenden?"
        # Weitere Abfragen können hier hinzugefügt werden
        # "Gib die Tabellen und ihre Wert-Spalten an, welche in der Datenbank vorhanden sind."
    ]

    # Iteriere über jede Abfrage und führe sie aus
    for query in queries:
        print(f"Query: {query}")
        
        # Führe die Abfrage mit dem Agenten aus und speichere das Ergebnis
        result = query_agent(agent, query, callbacks=[tracer])
        
        # Gib das Ergebnis der Abfrage aus
        print(f"Result: {result}")
        print("---")

# Der Einstiegspunkt des Skripts
if __name__ == "__main__":
    main()