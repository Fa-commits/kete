from typing import Union
from langchain.agents import AgentOutputParser
from langchain.schema import AgentAction, AgentFinish
import re

class CustomOutputParser(AgentOutputParser):
    def parse(self, llm_output: str) -> Union[AgentAction, AgentFinish]:
        if "Endgültige Antwort:" in llm_output:
            answer = llm_output.split("Endgültige Antwort:")[-1].strip()
            # Extrahiere Tavily-Suchergebnisse, falls vorhanden
            tavily_results = re.findall(r"Tavily-Suchergebnis: (.*?)(?:\n|$)", llm_output, re.DOTALL)
            return AgentFinish(
                return_values={"output": answer, "tavily_results": tavily_results},
                log=llm_output,
            )
        
        match = re.match(r"Gedanke:(.*?)Aktion:(.*?)Aktionseingabe:(.*)", llm_output, re.DOTALL)
        if not match:
            raise ValueError(f"Konnte keine Aktion und Aktionseingabe finden. Output war: {llm_output}")
        
        action = match.group(2).strip()
        action_input = match.group(3).strip()
        
        return AgentAction(tool=action, tool_input=action_input, log=llm_output)