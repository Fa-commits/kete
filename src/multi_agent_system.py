from langchain_openai import ChatOpenAI

class MultiAgentSystem:
    def __init__(self, agents):
        # Initialisiere das Multi-Agent-System mit einer Liste von Agenten
        self.agents = agents
    
    def run(self, query: str):
        # Führe die Anfrage für jeden Agenten aus
        results = []
        for agent in self.agents:
            # Rufe jeden Agenten mit der Anfrage auf
            result = agent.invoke({"input": query})
            # Extrahiere das Ergebnis und füge es der Liste hinzu
            results.append(result['output'] if isinstance(result, dict) and 'output' in result else str(result))
        
        # Kombiniere die Ergebnisse aller Agenten
        combined_result = self.combine_results(results)
        return combined_result
    
    def combine_results(self, results):
        # Bereite die Ergebnisse für die Zusammenfassung vor
        combined = "\n\n".join([f"Agent {i+1} Ergebnis:\n{result}" for i, result in enumerate(results)])
        
        # Initialisiere das ChatOpenAI-Modell für die Zusammenfassung
        llm = ChatOpenAI(temperature=0)
        
        # Erstelle einen Prompt für die Zusammenfassung und Analyse der Ergebnisse
        prompt = f"""
        Analysiere und fasse die folgenden Ergebnisse der verschiedenen Agenten zusammen:

        {combined}

        Bitte befolge diese Anweisungen:
        1. Gib für jeden Agenten eine kurze Zusammenfassung seiner Ergebnisse.
        2. Hebe wichtige Erkenntnisse oder Schlüsselinformationen aus jedem Agenten hervor.
        3. Vergleiche und kontrastiere die Ergebnisse der verschiedenen Agenten, falls relevant.
        4. Identifiziere eventuelle Widersprüche oder Übereinstimmungen zwischen den Agentenergebnissen.
        5. Ziehe eine Gesamtschlussfolgerung basierend auf allen Agentenergebnissen.
        6. Wenn möglich, gib konkrete Handlungsempfehlungen oder nächste Schritte an.

        Strukturiere deine Antwort klar und übersichtlich, sodass die Beiträge jedes Agenten und die Gesamtanalyse leicht zu verstehen sind.
        """
        
        # Rufe das LLM auf, um die Zusammenfassung zu generieren
        return llm.invoke(prompt)