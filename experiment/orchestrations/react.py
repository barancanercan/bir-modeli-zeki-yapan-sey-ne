import json
from typing import List, Dict, Any
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage


class ReAct:
    def __init__(self, model_name: str, temperature: float = 0.7, max_iterations: int = 10):
        self.model_name = model_name
        self.temperature = temperature
        self.max_iterations = max_iterations
        self.llm = ChatOllama(
            model=model_name,
            temperature=temperature
        )
        
    def run(self, query: str, knowledge: List[Dict] = None) -> Dict[str, Any]:
        system_prompt = """Sen bir ReAct (Reason + Act) agent'sın. Verilen soruyu düşünerek ve gözlem yaparak çöz.

Format:
Thought: [neyi düşünüyorum]
Action: [hangi bilgiye ihtiyacım var]
Observation: [bilgi buraya]

En sonunda:
Final Answer: [kesin cevap]

Bilgi tabanından bilgi almak için "search_knowledge" actionunu kullan.
Bilgi yetmezse kendi bilginden yararlan."""

        context = ""
        if knowledge:
            context = "\n\nBilgi Tabani:\n" + "\n".join([f"[{i}] {k['topic']}: {k['content']}" for i, k in enumerate(knowledge)])
        
        conversation = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"Soru: {query}\n{context}\n\nBaşla:")
        ]
        
        iterations = []
        final_answer = None
        
        for i in range(self.max_iterations):
            response = self.llm.invoke(conversation)
            content = response.content
            iterations.append({"step": i + 1, "output": content})
            
            if "Final Answer:" in content:
                final_answer = content.split("Final Answer:")[-1].strip()
                break
            
            observation = "\n[Gözlem: Devam ediyorum...]"
            conversation.append(HumanMessage(content=observation))
        
        return {
            "orchestration": "ReAct",
            "iterations": iterations,
            "final_answer": final_answer or "Cevap bulunamadı",
            "model": self.model_name,
            "query": query,
            "knowledge_used": len(knowledge) if knowledge else 0,
            "steps": len(iterations)
        }
