from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_community.tools import Tool, TavilySearchResults
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os

from outputparser import CustomOutputParser

from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent

import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="urllib3")

# Lade Umgebungsvariablen aus .env Datei
load_dotenv()
memory = MemorySaver()

def create_rag_agent():
    # Initialisiere SQL-Datenbankverbindung
    db = SQLDatabase.from_uri(os.getenv("MYSQL_CONNECTION_STRING"))
    
    # Initialisiere Language Model
    llm = ChatOpenAI(temperature=0)
    
    # Erstelle SQL-Toolkit
    sql_toolkit = SQLDatabaseToolkit(db=db, llm=llm)

    # Definiere SQL-Tool
    sql_tool = Tool(
        name="sql_database",
        func=SQLDatabaseChain.from_llm(llm=llm, db=db, verbose=True).run,
        description="Nützlich für Abfragen der SQL-Datenbank für faktische Informationen."
    )
    
    tav_tool = TavilySearchResults(
    max_results=5,
    search_depth="advanced",
    include_answer=True,
    include_raw_content=True,
    include_images=True,
    # include_domains=[...],
    # exclude_domains=[...],
    name="tavily_search",            # overwrite default tool name
    # description="...",     # overwrite default tool description
    # args_schema=...,       # overwrite default args_schema: BaseModel
)

    # Liste der verfügbaren Tools
    tools = [sql_tool, tav_tool]
    tool_names = [sql_tool.name, tav_tool.name]

    # Definiere Prompt-Template für den Agenten
    prompt = PromptTemplate(
        template="""Du bist ein effizienter SQL-Datenbankexperte. Deine Aufgabe ist es, Fragen über Datenbanken mit minimalem Aufwand und so wenig Iterationen wie möglich zu beantworten. Du hast Zugriff auf folgende Tools:

        {tools}

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
    
    output_parser = CustomOutputParser()

    # Erstelle ReAct-Agenten
    agent = create_openai_tools_agent(
        llm,
        tools,
        prompt,
        # output_parser=output_parser
        )
    
    # Erstelle Agent-Executor
    agent_executor = AgentExecutor.from_agent_and_tools(
        agent=agent, 
        tools=tools, 
        verbose=True, 
        handle_parsing_errors=True,
        # max_iterations=5  # Optional: Begrenzt die maximale Anzahl der Iterationen
    )

    return agent_executor

def query_agent(agent, query: str, callbacks=None):
    try:
        result = agent.invoke(
            {
                "input": query,
                "tools": [tool.name for tool in agent.tools]
            },
            config={"callbacks": callbacks}
        )
        if "tavily_results" in result.get("output", {}):
            print("Tavily-Suchergebnisse:")
            for idx, result in enumerate(result["output"]["tavily_results"], 1):
                print(f"{idx}. {result}")
        return result["output"]
    except Exception as e:
        return f"Ein Fehler ist aufgetreten: {str(e)}"
