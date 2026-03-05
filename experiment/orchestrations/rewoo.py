import json
from typing import List, Dict, Any
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage


class ReWOO:
    def __init__(self, model_name: str, temperature: float = 0.7):
        self.model_name = model_name
        self.temperature = temperature
        self.llm = ChatOllama(
            model=model_name,
            temperature=temperature
        )
        
    def run(self, query: str, knowledge: List[Dict] = None) -> Dict[str, Any]:
        system_prompt = """Sen bir ReWOO (Reasoning Without Observation) agent'sın. Önce plan yap, sonra paralel olarak bilgileri al, en son cevapla.

Adımlar:
1. PLAN: Soruyu çözmek için hangi bilgilere ihtiyacın olduğunu listele
2. GATHER: Tüm bilgileri topla (paralel)
3. SOLVE: Topladığın bilgilerle cevabı oluştur

JSON formatında cevap ver:
{
    "plan": ["bilgi1", "bilgi2", ...],
    "gathered_info": {"bilgi1": "...", "bilgi2": "..."},
    "final_answer": "..."
}"""

        context = ""
        if knowledge:
            context = "\n\nBilgi Tabani:\n" + "\n".join([f"- {k['topic']}: {k['content']}" for k in knowledge])
        
        user_prompt = f"Soru: {query}{context}"
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ]
        
        response = self.llm.invoke(messages)
        
        try:
            result = json.loads(response.content)
        except:
            result = {
                "plan": ["JSON parse hatası"],
                "gathered_info": {},
                "final_answer": response.content
            }
        
        return {
            "orchestration": "ReWOO",
            "plan": result.get("plan", []),
            "gathered_info": result.get("gathered_info", {}),
            "final_answer": result.get("final_answer", "Cevap bulunamadı"),
            "model": self.model_name,
            "query": query,
            "knowledge_used": len(knowledge) if knowledge else 0
        }
