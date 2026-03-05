import json
from typing import List, Dict, Any
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage


class Reflexion:
    def __init__(self, model_name: str, temperature: float = 0.7, max_reflections: int = 3):
        self.model_name = model_name
        self.temperature = temperature
        self.max_reflections = max_reflections
        self.llm = ChatOllama(
            model=model_name,
            temperature=temperature
        )
        
    def run(self, query: str, knowledge: List[Dict] = None) -> Dict[str, Any]:
        system_prompt = """Sen bir Reflexion agent'sın. Kendini yansıtarak cevap ver.

Adımlar:
1. İlk cevabını oluştur
2. Kendine eleştiri sor: "Bu cevap doğru mu? Eksik bir şey var mı?"
3. Eleştiriye göre cevabını güncelle
4. Son halini kontrol et

JSON formatında cevap ver:
{
    "initial_answer": "ilk cevap",
    "self_criticism": "kendine sorulan eleştiri",
    "revised_answer": "güncellenmiş cevap",
    "final_check": "son kontrol sonucu"
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
                "initial_answer": "JSON parse hatası",
                "self_criticism": "Parse hatası",
                "revised_answer": response.content,
                "final_check": "Başarısız"
            }
        
        return {
            "orchestration": "Reflexion",
            "initial_answer": result.get("initial_answer", ""),
            "self_criticism": result.get("self_criticism", ""),
            "revised_answer": result.get("revised_answer", ""),
            "final_check": result.get("final_check", ""),
            "model": self.model_name,
            "query": query,
            "knowledge_used": len(knowledge) if knowledge else 0
        }
