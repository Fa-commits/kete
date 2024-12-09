from langchain.callbacks.manager import tracing_v2_enabled
from rag_agent import create_rag_agent, query_agent
from dotenv import load_dotenv
import os

from langsmith import Client
from langchain.callbacks.tracers.langchain import LangChainTracer

import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="urllib3")

# Lade Umgebungsvariablen aus der .env Datei
load_dotenv()

def main():
    client = Client()
    tracer = LangChainTracer(project_name=os.getenv("LANGCHAIN_PROJECT"))
    
    # Erstelle den RAG-Agenten
    agent = create_rag_agent()
    
    # Liste von Abfragen, die an den Agenten gesendet werden sollen
    queries = [
        # "Ist die Tabellenstruktur so in Ordnung? Was kann gem. Internet verbessert werden? Wenn ja, gib explizite Vorschläge."
        # "Welche Tabellen gibt es in der Datenbank? Welche Felder gibt es in den jeweiligen Tabellen? Was sind die 3 häufigsten Mitarbeiternamen?",
        # "Wie zufrieden sind die Mitarbeitenden (Tabelle Mitarbeiter)? Ist dieser Wert normal im Vergleich mit anderen Unternehmen?"
        # "Gib die Tabellen und ihre Wert-Spalten an, welche in der Datenbank vorhanden sind."
        "Was würde passieren, wenn wir den Mitarbeitenden Homeoffice verbieten würde? Gib mir die Konkreten konsequenzen auf Mitarbeiterzufriedenheit und Kündigungen. Was kann dagegen gemacht werden? Beziehe die Datenbankdaten (nur agregierte Daten nutzen und nicht die Rohdaten!) und auch die Erkenntnisse aus dem Internet mit ein."
    ]

    # Iteriere über jede Abfrage und führe sie aus
    for query in queries:
        print(f"Query: {query}")
        
        # Führe die Abfrage mit dem Agenten aus und speichere das Ergebnis
        result = query_agent(agent,
                             query, 
                             callbacks=[tracer]
                             )
        
        # Gib das Ergebnis der Abfrage aus
        print(f"Result: {result}")
        print("---")

# Der Einstiegspunkt des Skripts
if __name__ == "__main__":
    main()