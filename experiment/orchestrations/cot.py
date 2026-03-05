import json
from typing import List, Dict, Any
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage


class ChainOfThought:
    def __init__(self, model_name: str, temperature: float = 0.7):
        self.model_name = model_name
        self.temperature = temperature
        self.llm = ChatOllama(
            model=model_name,
            temperature=temperature,
            format="json"
        )
        
    def run(self, query: str, knowledge: List[Dict] = None) -> Dict[str, Any]:
        system_prompt = """Sen bir araştırma asistanısın. Verilen soruyu adım adım düşünerek cevapla.

Adımlar:
1. Sorunun ne sorduğunu anla
2. Gerekli bilgi parçalarını belirle
3. Her bilgi parçasını analiz et
4. Sonuçları birleştir
5. Cevabı ver

Cevabını JSON formatında ver:
{
    "reasoning_steps": ["adım1", "adım2", ...],
    "answer": "son cevap",
    "confidence": 0.0-1.0
}"""

        context = ""
        if knowledge:
            context = "\n\nMevcut Bilgi:\n" + "\n".join([f"- {k['topic']}: {k['content']}" for k in knowledge])
        
        user_prompt = f"{query}{context}"
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ]
        
        response = self.llm.invoke(messages)
        
        try:
            result = json.loads(response.content)
        except:
            result = {
                "reasoning_steps": ["JSON parse hatası"],
                "answer": response.content,
                "confidence": 0.0
            }
        
        return {
            "orchestration": "CoT",
            "response": result,
            "model": self.model_name,
            "query": query,
            "knowledge_used": len(knowledge) if knowledge else 0
        }
