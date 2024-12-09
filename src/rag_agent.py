from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.agents import Tool, AgentExecutor, LLMSingleActionAgent
from langchain.prompts import StringPromptTemplate
from langchain_openai import ChatOpenAI
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import numpy as np
from langchain.agents import AgentExecutor, create_openai_tools_agent

class AdaptiveToolSelector:
    def __init__(self, all_tools):
        self.all_tools = all_tools
        self.tool_performance = {tool.name: 1.0 for tool in all_tools}
        self.embeddings = OpenAIEmbeddings()
    
    def select_tools(self, query, user_profile=None):
        # Berechne Embedding für die Anfrage
        query_embedding = self.embeddings.embed_query(query)
        # Erstelle Embeddings für alle Tools
        tool_texts = [f"{tool.name}: {tool.description}" for tool in self.all_tools]
        tool_embeddings = self.embeddings.embed_documents(tool_texts)
        
        # Berechne Ähnlichkeitsscores
        similarity_scores = np.dot(tool_embeddings, query_embedding)
        
        # Berücksichtige Benutzerprofile, falls vorhanden
        if user_profile:
            history_weight = 0.2
            history_scores = np.array([user_profile.tool_preferences.get(tool.name, 0) for tool in self.all_tools])
            history_scores = history_scores / np.max(history_scores) if np.max(history_scores) > 0 else history_scores
            similarity_scores = (1 - history_weight) * similarity_scores + history_weight * history_scores
        
        # Berücksichtige Tool-Performance
        performance_scores = np.array([self.tool_performance[tool.name] for tool in self.all_tools])
        final_scores = similarity_scores * performance_scores
        
        # Wähle die besten Tools aus
        sorted_indices = np.argsort(final_scores)[::-1]
        selected_tools = [self.all_tools[i] for i in sorted_indices[:2]]
        return selected_tools
    
    def update_performance(self, tool_name, success_score):
        # Aktualisiere die Performance-Bewertung eines Tools
        self.tool_performance[tool_name] = 0.9 * self.tool_performance[tool_name] + 0.1 * success_score

class UserProfile:
    def __init__(self):
        self.query_history = []
        self.tool_preferences = {}
    
    def update(self, query, used_tools):
        # Aktualisiere das Benutzerprofil mit neuen Informationen
        self.query_history.append(query)
        for tool in used_tools:
            self.tool_preferences[tool.name] = self.tool_preferences.get(tool.name, 0) + 1

class ContinuousLearningSystem:
    def __init__(self, all_tools):
        self.all_tools = all_tools
        self.vectorizer = TfidfVectorizer()
        self.classifier = MultinomialNB()
        self.X = []
        self.y = []
    
    def update(self, query, used_tool):
        # Füge neue Daten zum Lernsystem hinzu
        self.X.append(query)
        self.y.append(used_tool.name)
        
        # Trainiere das Modell neu, wenn genügend Daten vorhanden sind
        if len(self.X) > 100:
            X_vectorized = self.vectorizer.fit_transform(self.X)
            self.classifier.fit(X_vectorized, self.y)
    
    def predict_tool(self, query, adaptive_selector, user_profile):
        # Verwende den adaptiven Selektor, wenn nicht genügend Daten vorhanden sind
        if len(self.X) < 10:
            return adaptive_selector.select_tools(query, user_profile)
        
        # Andernfalls verwende das trainierte Modell zur Vorhersage
        query_vectorized = self.vectorizer.transform([query])
        predicted_tool_name = self.classifier.predict(query_vectorized)[0]
        predicted_tool = next(tool for tool in self.all_tools if tool.name == predicted_tool_name)
        return [predicted_tool] + adaptive_selector.select_tools(query, user_profile)[:1]

def create_rag_agent(llm, tools, prompt):
    # Erstelle die notwendigen Komponenten für den Agenten
    adaptive_selector = AdaptiveToolSelector(tools)
    learning_system = ContinuousLearningSystem(tools)
    user_profile = UserProfile()

    def get_tools(query):
        # Wähle Tools basierend auf der Anfrage und dem Lernstand aus
        selected_tools = learning_system.predict_tool(query, adaptive_selector, user_profile)
        user_profile.update(query, selected_tools)
        return selected_tools

    # Erstelle den OpenAI-Tools-Agenten
    agent = create_openai_tools_agent(llm, tools, prompt)

    # Erstelle den Agent-Executor mit den ausgewählten Tools
    agent_executor = AgentExecutor.from_agent_and_tools(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True,
        tool_retriever=get_tools
    )

    return agent_executor, adaptive_selector, learning_system, user_profile

def query_agent(agent_executor, query: str, adaptive_selector, learning_system, user_profile, callbacks=None):
    try:
        # Wähle Tools für die aktuelle Anfrage aus
        selected_tools = learning_system.predict_tool(query, adaptive_selector, user_profile)
        # Führe die Anfrage mit dem Agent-Executor aus
        result = agent_executor.invoke(
            {
                "input": query,
                "tools": [tool.name for tool in selected_tools]
            },
            config={"callbacks": callbacks}
        )
        
        # Aktualisiere die Performance-Bewertungen und das Lernsystem
        for tool in selected_tools:
            success_score = 1.0 if tool.name in str(result) else 0.5
            adaptive_selector.update_performance(tool.name, success_score)
            learning_system.update(query, tool)
        
        # Gib das Ergebnis zurück
        return result['output'] if isinstance(result, dict) and 'output' in result else str(result)
    except Exception as e:
        return f"Ein Fehler ist aufgetreten: {str(e)}"