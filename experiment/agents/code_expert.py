import json
import time
import asyncio
from typing import List, Dict, Any, Optional, Callable
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import tool
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import httpx


class RetryableLLMError(Exception):
    """Retry edilebilir LLM hatası"""
    pass


class ToolCallingReAct:
    """
    Gerçek ReAct implementasyonu - Tool Calling ile
    
    Özellikler:
    - LangChain tool decorators
    - Retry with exponential backoff
    - Graceful degradation
    - Tool execution tracking
    """
    
    def __init__(self, model_name: str, temperature: float = 0.7, max_iterations: int = 10):
        self.model_name = model_name
        self.temperature = temperature
        self.max_iterations = max_iterations
        
        self.llm = ChatOllama(
            model=model_name,
            temperature=temperature
        )
        
        self.tools = self._create_tools()
        self.llm_with_tools = self.llm.bind_tools(self.tools)
        
    def _create_tools(self) -> List:
        """Tool'ları oluştur"""
        
        @tool
        def search_knowledge(query: str) -> str:
            """Siyasi konularda bilgi aramak için kullanılır."""
            from pathlib import Path
            import faiss
            import numpy as np
            from langchain_ollama import OllamaEmbeddings
            
            # Try to load FAISS index
            index_path = Path("data/faiss_index/politics.index")
            docs_path = Path("data/faiss_index/documents.json")
            
            if not index_path.exists() or not docs_path.exists():
                return f"Knowledge base bulunamadı. Query: {query}"
            
            try:
                embeddings = OllamaEmbeddings(model="nomic-embed-text:latest")
                index = faiss.read_index(str(index_path))
                
                with open(docs_path, "r", encoding="utf-8") as f:
                    documents = json.load(f)
                
                query_vector = embeddings.embed_query(query)
                query_vector = np.array([query_vector]).astype('float32')
                
                distances, indices = index.search(query_vector, 3)
                
                results = []
                for idx in indices[0]:
                    if idx < len(documents):
                        results.append(documents[idx]["content"][:200])
                
                return "\n\n".join(results) if results else "Bilgi bulunamadı"
            except Exception as e:
                return f"Bilgi arama hatası: {str(e)}"
        
        @tool
        def analyze_data(data_type: str, action: str) -> str:
            """Verileri analiz etmek için kullanılır."""
            if "istatistik" in data_type.lower() or "statistic" in data_type.lower():
                return "İstatistik analiz: ANOVA, t-test, correlation mevcut"
            elif "trend" in data_type.lower():
                return "Trend analizi: Zaman serisi verileri değerlendiriliyor"
            else:
                return f"{data_type} için {action} analizi yapılıyor"
        
        @tool
        def calculate_metric(value1: float, value2: float, operation: str) -> str:
            """Basit hesaplamalar yapmak için kullanılır."""
            try:
                if operation == "divide":
                    result = value1 / value2 if value2 != 0 else "Sıfıra bölünemez"
                elif operation == "multiply":
                    result = value1 * value2
                elif operation == "subtract":
                    result = value1 - value2
                elif operation == "add":
                    result = value1 + value2
                elif operation == "percentage":
                    result = (value1 / value2) * 100 if value2 != 0 else "Sıfıra bölünemez"
                else:
                    result = "Bilinmeyen işlem"
                
                return f"Sonuç: {result}"
            except Exception as e:
                return f"Hesaplama hatası: {str(e)}"
        
        @tool
        def generate_report(summary: str, format: str = "markdown") -> str:
            """Rapor oluşturmak için kullanılır."""
            if format == "json":
                return json.dumps({"summary": summary, "generated": True}, indent=2)
            else:
                return f"# Rapor\n\n{summary}\n\n## Sonuç\nBu analiz otomatik olarak oluşturulmuştur."
        
        return [search_knowledge, analyze_data, calculate_metric, generate_report]
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((RetryableLLMError, httpx.ConnectError, httpx.TimeoutException))
    )
    def _call_llm_with_retry(self, messages: List) -> Any:
        """LLM'i retry ile çağır"""
        try:
            response = self.llm_with_tools.invoke(messages)
            return response
        except (httpx.ConnectError, httpx.TimeoutException) as e:
            raise RetryableLLMError(f"Connection error: {e}")
        except Exception as e:
            if "connection" in str(e).lower() or "timeout" in str(e).lower():
                raise RetryableLLMError(f"Retryable error: {e}")
            raise
    
    def run(self, query: str, knowledge: List[Dict] = None) -> Dict[str, Any]:
        """ReAct agent'ı çalıştır"""
        
        system_prompt = """Sen bir araştırma asistanısın. ReAct (Reason + Act) pattern'ini kullan.

Adımlar:
1. Soruyu anla
2. Hangi bilgiye ihtiyacın olduğunu belirle
3. Uygun tool'u kullan
4. Sonuçları değerlendir
5. Cevabı oluştur

Tool'ları kullan:
- search_knowledge: Bilgi tabanında araştırma
- analyze_data: Verileri analiz et
- calculate_metric: Hesaplama yap
- generate_report: Rapor oluştur

Yanıtını JSON formatında ver:
{
    "thought": "düşünce süreci",
    "action": "kullanılan tool ve parametreleri",
    "observation": "tool sonucu",
    "final_answer": "son cevap"
}"""
        
        context = ""
        if knowledge:
            context = "\n\nBilgi Tabani:\n" + "\n".join([
                f"- {k['topic']}: {k['content'][:200]}" for k in knowledge[:5]
            ])
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"Soru: {query}{context}")
        ]
        
        iterations = []
        max_iters = min(self.max_iterations, 5)  # Limit for speed
        
        for i in range(max_iters):
            try:
                response = self._call_llm_with_retry(messages)
                
                # Check if response has tool calls
                if hasattr(response, "tool_calls") and response.tool_calls:
                    for tool_call in response.tool_calls:
                        tool_name = tool_call["name"]
                        tool_args = tool_call["args"]
                        
                        # Execute tool
                        for tool in self.tools:
                            if tool.name == tool_name:
                                try:
                                    result = tool.invoke(tool_args)
                                    iterations.append({
                                        "step": i + 1,
                                        "thought": str(response.content)[:100] if response.content else "",
                                        "action": f"{tool_name}({tool_args})",
                                        "observation": str(result)[:200]
                                    })
                                    
                                    # Add tool result to messages
                                    messages.append(HumanMessage(
                                        content=f"Tool sonucu: {result}"
                                    ))
                                except Exception as e:
                                    iterations.append({
                                        "step": i + 1,
                                        "error": str(e)
                                    })
                                break
                else:
                    # No tool calls, final answer
                    final_answer = response.content if response.content else "Cevap bulunamadı"
                    iterations.append({
                        "step": i + 1,
                        "final_answer": final_answer
                    })
                    break
                    
            except RetryableLLMError as e:
                iterations.append({
                    "step": i + 1,
                    "error": f"Retry hatası: {str(e)}"
                })
                break
            except Exception as e:
                iterations.append({
                    "step": i + 1,
                    "error": str(e)
                })
                break
        
        # Extract final answer
        final = None
        for it in reversed(iterations):
            if "final_answer" in it:
                final = it["final_answer"]
                break
        
        return {
            "orchestration": "ReAct-ToolCalling",
            "iterations": iterations,
            "final_answer": final or "Cevap bulunamadı",
            "model": self.model_name,
            "query": query,
            "knowledge_used": len(knowledge) if knowledge else 0,
            "tool_calls": len([i for i in iterations if "action" in i])
        }


class AsyncExperimentRunner:
    """
    Async experiment runner with parallel execution
    """
    
    def __init__(self, config_path: str = "config.yaml"):
        import yaml
        with open(config_path, "r") as f:
            self.config = yaml.safe_load(f)
        
        self.models = self.config["models"]
        
    async def run_single_async(self, query: Dict, model_level: str, 
                               orchestration: str, knowledge_level: str) -> Dict:
        """Single experiment run async"""
        from pathlib import Path
        import json
        
        model = self.models[model_level]
        
        # Load knowledge
        kb_dir = Path(self.config["experiment"]["knowledge_base_dir"])
        kb_file = kb_dir / knowledge_level / "politics.json"
        
        knowledge = []
        if kb_file.exists():
            with open(kb_file, "r", encoding="utf-8") as f:
                knowledge = json.load(f)
        
        # Run orchestration
        orchestrator = ToolCallingReAct(model)
        
        start_time = time.time()
        try:
            result = orchestrator.run(query["query"], knowledge)
            success = True
            error = None
        except Exception as e:
            result = {"error": str(e)}
            success = False
            error = str(e)
        
        elapsed = time.time() - start_time
        
        return {
            "query_id": query["id"],
            "model_level": model_level,
            "orchestration": orchestration,
            "knowledge_level": knowledge_level,
            "success": success,
            "error": error,
            "result": result,
            "elapsed_seconds": round(elapsed, 2)
        }
    
    async def run_batch_async(self, experiments: List[Dict], max_concurrent: int = 3) -> List[Dict]:
        """Run multiple experiments with concurrency limit"""
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def run_with_limit(exp):
            async with semaphore:
                return await self.run_single_async(**exp)
        
        tasks = [run_with_limit(exp) for exp in experiments]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Handle exceptions
        processed = []
        for r in results:
            if isinstance(r, Exception):
                processed.append({"error": str(r), "success": False})
            else:
                processed.append(r)
        
        return processed


class CodeExpert:
    """
    Agent 3: Kod/ML Mimarisi Uzmanı
    
    Görevler:
    - Error handling iyileştirme
    - Async execution
    - Tool calling implementasyonu
    - Performance optimization
    """
    
    def __init__(self):
        self.react = None
        
    def improve_orchestration(self, orchestrator_class, model_name: str):
        """Mevcut orkestrasyonu iyileştir"""
        # Retry decorator ekle
        # Async wrapper ekle
        # Tool calling ekle
        pass
    
    def get_tool_calling_react(self, model_name: str) -> ToolCallingReAct:
        """Tool calling ReAct döndür"""
        return ToolCallingReAct(model_name)
    
    def benchmark_models(self, queries: List[str], models: Dict[str, str]) -> Dict:
        """Model benchmark"""
        import yaml
        with open("config.yaml", "r") as f:
            config = yaml.safe_load(f)
        
        results = {}
        
        for level, model in models.items():
            times = []
            for query in queries[:3]:  # Quick test
                react = ToolCallingReAct(model)
                start = time.time()
                try:
                    react.run(query, [])
                    elapsed = time.time() - start
                    times.append(elapsed)
                except:
                    pass
            
            results[level] = {
                "model": model,
                "avg_time": sum(times) / len(times) if times else None,
                "runs": len(times)
            }
        
        return results


def main():
    # Test tool calling
    react = ToolCallingReAct("phi3:latest", max_iterations=3)
    result = react.run("Türkiye'nin 2024 ekonomik durumu nedir?", [])
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
