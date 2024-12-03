from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_core.tools import Tool
from langchain.agents import AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os

from outputparser import CustomOutputParser

# Lade Umgebungsvariablen aus .env Datei
load_dotenv()

def create_rag_agent():
    # Initialisiere SQL-Datenbankverbindung
    db = SQLDatabase.from_uri(os.getenv("MYSQL_CONNECTION_STRING"))
    
    # Initialisiere Language Model
    llm = ChatOpenAI(temperature=0)
    
    # Erstelle SQL-Toolkit
    sql_toolkit = SQLDatabaseToolkit(db=db, llm=llm)

    # Definiere SQL-Tool
    sql_tool = Tool(
        name="SQL Database",
        func=SQLDatabaseChain.from_llm(llm=llm, db=db, verbose=True).run,
        description="Nützlich für Abfragen der SQL-Datenbank für faktische Informationen."
    )

    # Liste der verfügbaren Tools
    tools = [sql_tool]

    # Definiere Prompt-Template für den Agenten
    prompt = PromptTemplate.from_template(
        """Du bist ein effizienter SQL-Datenbankexperte. Deine Aufgabe ist es, Fragen über die Datenbank mit minimalem Aufwand und so wenig Iterationen wie möglich zu beantworten. Du hast Zugriff auf folgende Tools:

        {tools}

        Befolge dieses Format STRIKT:

        Frage: die zu beantwortende Eingabefrage
        Gedanke: Analysiere die Frage sorgfältig. Plane deine Aktionen, um die Antwort mit minimalen Datenbankabfragen zu finden.
        Aktion: Wähle die effizienteste Aktion aus [{tool_names}]
        Aktionseingabe: Präzise Eingabe für die gewählte Aktion
        Beobachtung: Ergebnis der Aktion
        ... (Wiederhole Gedanke/Aktion/Aktionseingabe/Beobachtung NUR wenn unbedingt nötig)
        Gedanke: Fasse die gewonnenen Informationen zusammen und formuliere die endgültige Antwort.
        Endgültige Antwort: Prägnante und vollständige Antwort auf die ursprüngliche Frage.

        Beginne nun:

        Frage: {input}
        Gedanke: {agent_scratchpad}"""
    )
    
    output_parser = CustomOutputParser()

    # Erstelle ReAct-Agenten
    agent = create_react_agent(
        llm,
        tools,
        prompt,
        output_parser=output_parser)
    
    # Erstelle Agent-Executor
    agent_executor = AgentExecutor(
        agent=agent, 
        tools=tools, 
        verbose=True, 
        handle_parsing_errors=True
    )

    return agent_executor

def query_agent(agent, query: str):
    """
    Führt eine Abfrage mit dem Agenten aus und behandelt mögliche Fehler.
    """
    try:
        return agent.invoke({"input": query})
    except Exception as e:
        return f"Ein Fehler ist aufgetreten: {str(e)}"
    
