# Importiere notwendige Module und Klassen
from rag_agent import create_rag_agent, query_agent
from multi_agent_system import MultiAgentSystem
from langchain_openai import ChatOpenAI
from langchain.tools import StructuredTool
from langchain_experimental.sql import SQLDatabaseChain
from langchain_community.tools import TavilySearchResults
from langchain_community.utilities import SQLDatabase
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
from langsmith import Client
from langchain.callbacks.tracers.langchain import LangChainTracer
from langchain_core.tracers.context import tracing_v2_enabled

import os

# Lade Umgebungsvariablen aus .env Datei
load_dotenv()

def main():
    # Initialisiere Language Model und Datenbank
    llm = ChatOpenAI(temperature=0)
    db = SQLDatabase.from_uri(os.getenv("MYSQL_CONNECTION_STRING"))
    
    # Initialisiere LangSmith Client und Tracer
    client = Client()
    tracer = LangChainTracer(project_name=os.getenv("LANGCHAIN_PROJECT"))
    
    # Definiere SQL-Tool
    sql_tool = StructuredTool.from_function(
        func=lambda input: SQLDatabaseChain.from_llm(llm=llm, db=db, verbose=True).invoke(query),
        name="sql_database",
        description="Nützlich für Abfragen der SQL-Datenbank für faktische Informationen.",
        return_direct=False,
        coroutine=None,
        args_schema=None,
        infer_schema=True,
        metadata={
            "type": "database",
            "keywords": ["sql", "datenbank", "tabelle", "abfrage", "daten"]
        }
    )

    # Definiere Tavily-Suchtool
    tav_tool = StructuredTool.from_function(
        func=TavilySearchResults(
            max_results=5,
            search_depth="advanced",
            include_answer=True,
            include_raw_content=True,
            include_images=True,
        ).run,
        name="tavily_search",
        description="Nützlich für Internetsuchen und Recherche aktueller Informationen.",
        return_direct=False,
        coroutine=None,
        args_schema=None,
        infer_schema=True,
        metadata={
            "type": "search",
            "keywords": ["internet", "suche", "aktuell", "recherche", "vergleich"]
        }
    )
    
    # Kombiniere Tools
    tools = [sql_tool, tav_tool]
    
    # Definiere Prompt-Template für den Agenten
    prompt = PromptTemplate(
        template="""Du bist ein effizienter SQL-Datenbankexperte. Deine Aufgabe ist es, Fragen über Datenbanken mit minimalem Aufwand und so wenig Iterationen wie möglich zu beantworten. Du hast Zugriff auf folgende Tools:

        

        Befolge dieses Format STRIKT:

        Frage: die zu beantwortende Eingabefrage
        Gedanke: Analysiere die Frage sorgfältig. Plane deine Aktionen, um die Antwort mit minimalen Iterationen zu finden.
        Aktion: Wähle die effizienteste Aktion aus und kombiniere alle Tools
        Aktionseingabe: Präzise Eingabe für die gewählte Aktion
        Beobachtung: Ergebnis der Aktion
        ... (Wiederhole Gedanke/Aktion/Aktionseingabe/Beobachtung NUR wenn unbedingt nötig)
        Gedanke: Fasse die gewonnenen Informationen zusammen und formuliere die endgültige Antwort.
        Endgültige Antwort: Prägnante und vollständige Antwort auf die ursprüngliche Frage.

        Beginne nun:

        Frage: {input}
        Zwischenschritte: {intermediate_steps}
        Gedanke: {agent_scratchpad}""",
        input_variables=["input", "intermediate_steps", "agent_scratchpad", "tools"]
    )
    
    # Erstelle Agenten
    sql_agent, sql_adaptive_selector, sql_learning_system, sql_user_profile = create_rag_agent(llm, [sql_tool], prompt)
    search_agent, search_adaptive_selector, search_learning_system, search_user_profile = create_rag_agent(llm, [tav_tool], prompt)
    
    # Erstelle Multi-Agent-System
    multi_agent_system = MultiAgentSystem([sql_agent, search_agent])
    
    # Hauptschleife für Benutzerabfragen
    while True:
        query = input("Bitte geben Sie Ihre Frage ein (oder 'exit' zum Beenden): ")
        if query.lower() == 'exit':
            break
        
        # Verwende Multi-Agent-System zur Beantwortung der Frage
        result = multi_agent_system.run(query)
        print(result)
        
        # Alternative: Verwende einzelne Agenten (auskommentiert)
        # sql_result = query_agent(sql_agent, query, sql_adaptive_selector, sql_learning_system, sql_user_profile)
        # search_result = query_agent(search_agent, query, search_adaptive_selector, search_learning_system, search_user_profile)
        # print("SQL Agent:", sql_result)
        # print("Search Agent:", search_result)

# Führe das Hauptprogramm aus, wenn das Skript direkt ausgeführt wird
if __name__ == "__main__":
    main()