from typing import Union
from langchain.agents import AgentOutputParser
from langchain.schema import AgentAction, AgentFinish
import re

class CustomOutputParser(AgentOutputParser):
    """
    Ein benutzerdefinierter Parser für die Ausgabe des LLM-Agenten.
    """

    def parse(self, llm_output: str) -> Union[AgentAction, AgentFinish]:
        """
        Parst die Ausgabe des LLM und gibt entweder eine AgentAction oder AgentFinish zurück.

        Args:
            llm_output (str): Die Ausgabe des Language Models.

        Returns:
            Union[AgentAction, AgentFinish]: Entweder eine AgentAction für weitere Schritte
            oder AgentFinish, wenn eine endgültige Antwort gefunden wurde.

        Raises:
            ValueError: Wenn keine Aktion und Aktionseingabe im Output gefunden werden kann.
        """
        # Prüfe, ob eine endgültige Antwort vorhanden ist
        if "Endgültige Antwort:" in llm_output:
            # Extrahiere die endgültige Antwort und gebe AgentFinish zurück
            return AgentFinish(
                return_values={"output": llm_output.split("Endgültige Antwort:")[-1].strip()},
                log=llm_output,
            )
        
        # Suche nach Gedanke, Aktion und Aktionseingabe im Output
        match = re.match(r"Gedanke:(.*?)Aktion:(.*?)Aktionseingabe:(.*)", llm_output, re.DOTALL)
        if not match:
            # Wenn das erwartete Format nicht gefunden wird, wirf einen Fehler
            raise ValueError(f"Konnte keine Aktion und Aktionseingabe finden. Output war: {llm_output}")
        
        # Extrahiere Aktion und Aktionseingabe aus dem Match
        action = match.group(2).strip()
        action_input = match.group(3).strip()
        
        # Gebe eine AgentAction mit den extrahierten Informationen zurück
        return AgentAction(tool=action, tool_input=action_input, log=llm_output)