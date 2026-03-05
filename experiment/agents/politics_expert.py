import json
import os
from pathlib import Path
from typing import List, Dict, Any, Optional
import numpy as np
import faiss
from langchain_ollama import ChatOllama
from langchain_ollama import OllamaEmbeddings


class PoliticsExpert:
    """
    Agent 1: Türkiye Siyaseti Uzmanı
    
    Görevler:
    - Knowledge Base'i güncel verilerle genişletme
    - FAISS vector database kurulumu
    - Semantic search implementasyonu
    - RAG sistemi oluşturma
    """
    
    def __init__(self, embedding_model: str = "nomic-embed-text:latest"):
        self.embedding_model = embedding_model
        self.embeddings = OllamaEmbeddings(model=embedding_model)
        self.index: Optional[faiss.IndexFlatL2] = None
        self.documents: List[Dict] = []
        self.metadata: List[Dict] = []
        self.data_dir = Path("data/knowledge_bases")
        
    def load_base_knowledge(self) -> List[Dict]:
        """Mevcut knowledge base'leri yükle"""
        all_docs = []
        
        for level in ["empty", "basic", "comprehensive"]:
            file_path = self.data_dir / level / "politics.json"
            if file_path.exists():
                with open(file_path, "r", encoding="utf-8") as f:
                    docs = json.load(f)
                    for doc in docs:
                        doc["knowledge_level"] = level
                    all_docs.extend(docs)
        
        return all_docs
    
    def add_g2024_data(self) -> List[Dict]:
        """2024-2025 güncel siyasi verileri ekle"""
        current_docs = [
            {
                "id": "tr_ekonomi_2025_q1",
                "topic": "Türkiye Ekonomisi 2025 Q1",
                "content": """2025 Q1'de Türkiye ekonomisi yıllık bazda %2.1 büyüme kaydetti. 
Enflasyon Ocak 2025'te %39.5 seviyesinde gerçekleşti. Merkez Bankası politika faizi %45'te sabit kaldı.
İşsizlik oranı %9.2'ye yükseldi. Cari açık 2024 yılında 52 milyar dolar oldu.
ABD ile F-16 tedarik anlaşması onaylandı. S-400 krizi devam ediyor.""",
                "source": "TCMB, TÜİK 2025",
                "date": "2025-01"
            },
            {
                "id": "abd_secim_2025",
                "topic": "Trump 2. Dönem Politikaları 2025",
                "content": """Trump Ocak 2025'te göreve başladı. İlk 100 gün:
- Göç politikası: Sınır duvarı genişletildi, iltica başvuruları kısıtlandı
- Ticaret: Çin'e %60 tariffeler, AB'ye %20 tariffeler
- Enerji: Petrol üretimini artırma kararı, LNG ihracatı hedefleri
- NATO: Mütteşiklerin savunma harcamalarını artırması baskısı
- Ukrayna: Yardımlara koşul bağlama, müzakere çağrısı""",
                "source": "AP, Reuters 2025",
                "date": "2025-01"
            },
            {
                "id": "ab_buyume_2025",
                "topic": "AB Ekonomisi 2025",
                "content": """AB 2025'te %1.1 büyüme bekliyor. Almanya ekonomisi durgun.
Fransa'da emeklilik reformu protestoları sürüyor. Ursula von der Leyen ikinci döneminde
yeşil dönüşüm ve dijital tek pazar öncelikleriyle devam ediyor.
Göç paketi kabul edildi. Rusya yaptırımları 15. pakete ulaştı.""",
                "source": "Eurostat 2025",
                "date": "2025-01"
            },
            {
                "id": "rusya_ukrayna_2025",
                "topic": "Rusya-Ukrayna Savaşı 2025 Durumu",
                "content": """Savaş 3. yılına girdi. Müzakezme umutları artıyor.
ABD'nin arabuluculuğunda ateşkes görüşmeleri başladı.
Ukrayna AB üyelik müzakereleri resmen açıldı. NATO desteği sürüyor.
Rusya ekonomisi yaptırımlara rağmen %2.8 büyüdü.""",
                "source": "ISW, Economist 2025",
                "date": "2025-02"
            },
            {
                "id": "dogu_akdeniz_2025",
                "topic": "Doğu Akdeniz Enerji 2025",
                "content": """Türkiye-Kıbrıs barış görüşmeleri yeniden başladı.
Doğu Akdeniz'de yeni gaz keşifleri: Afrodit (Kıbrıs) + Akkuyu (Türkiye) = bölgesel işbirliği potansiyeli.
Mısır ile enerji işbirliği anlaşması imzalandı.
Yunanistan ile Ege sorunları çözüme kavuşturulamadı.""",
                "source": "Enerji Bakanlığı 2025",
                "date": "2025-01"
            },
            {
                "id": "nato_2025",
                "topic": "NATO 2025 Durumu",
                "content": """NATO 32 üyeye ulaştı. Finlandiya ve İsveç tam üye.
Türkiye'nin İsveç üyelik onayı 2024'te çıktı.
NATO'nun 75. yılı: Yeni stratejik konsept kabul edildi.
Rusya tehdidi vurgusu arttı. Pasifik vurgusu yok.""",
                "source": "NATO 2025",
                "date": "2025-01"
            }
        ]
        return current_docs
    
    def add_expected_answers(self, docs: List[Dict]) -> List[Dict]:
        """Her soru için beklenen cevapları ekle"""
        expected = {
            1: {
                "expected_metrics": ["GSYİH büyümesi ~%3", "Enflasyon ~%45", "İşsizlik ~%10"],
                "reasoning_steps": ["Verileri topla", "Trend analiz et", "Karşılaştır"]
            },
            2: {
                "expected_metrics": ["Tarife %25", "İhracat $500B", "Tedarik zinciri yeniden yapılanma"],
                "reasoning_steps": ["Tarihsel bak", "Etki analizi yap", "Sonuç çıkar"]
            },
            3: {
                "expected_metrics": ["Aşırı sağ güçlendi", "Yeşiller kaybetti", "Von der Leyen seçildi"],
                "reasoning_steps": ["Sonuçları analiz et", "Siyasi dengeyi değerlendir"]
            }
        }
        
        for doc in docs:
            query_id = int(doc.get("id", "").split("_")[-1]) if doc.get("id", "").split("_")[-1].isdigit() else None
            if query_id and query_id in expected:
                doc["expected"] = expected[query_id]
        
        return docs
    
    def build_index(self, force_rebuild: bool = False) -> faiss.IndexFlatL2:
        """FAISS index oluştur"""
        output_dir = Path("data/faiss_index")
        output_dir.mkdir(exist_ok=True)
        
        index_path = output_dir / "politics.index"
        docs_path = output_dir / "documents.json"
        
        if index_path.exists() and not force_rebuild:
            self.index = faiss.read_index(str(index_path))
            with open(docs_path, "r", encoding="utf-8") as f:
                self.documents = json.load(f)
            print(f"Mevcut index yüklendi: {len(self.documents)} doküman")
            return self.index
        
        # Tüm dokümanları topla
        self.documents = self.load_base_knowledge()
        self.documents.extend(self.add_g2024_data())
        self.documents = self.add_expected_answers(self.documents)
        
        # Embeddings oluştur
        texts = [doc["content"] for doc in self.documents]
        vectors = self.embeddings.embed_documents(texts)
        vectors = np.array(vectors).astype('float32')
        
        # FAISS index oluştur
        dimension = vectors.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(vectors)
        
        # Kaydet
        faiss.write_index(self.index, str(index_path))
        with open(docs_path, "w", encoding="utf-8") as f:
            json.dump(self.documents, f, ensure_ascii=False, indent=2)
        
        print(f"Yeni index oluşturuldu: {len(self.documents)} doküman, {dimension} boyut")
        return self.index
    
    def search(self, query: str, k: int = 5) -> List[Dict]:
        """Semantic search yap"""
        if self.index is None:
            self.build_index()
        
        query_vector = self.embeddings.embed_query(query)
        query_vector = np.array([query_vector]).astype('float32')
        
        distances, indices = self.index.search(query_vector, k)
        
        results = []
        for idx, distance in zip(indices[0], distances[0]):
            if idx < len(self.documents):
                doc = self.documents[idx].copy()
                doc["score"] = float(distance)
                results.append(doc)
        
        return results
    
    def get_context_for_query(self, query: str, max_docs: int = 5) -> str:
        """Soru için bağlam oluştur"""
        results = self.search(query, max_docs)
        
        context_parts = []
        for i, doc in enumerate(results, 1):
            context_parts.append(
                f"[{i}] {doc['topic']}: {doc['content'][:300]}..."
            )
        
        return "\n\n".join(context_parts)


def main():
    expert = PoliticsExpert()
    expert.build_index()
    
    # Test sorusu
    query = "Türkiye'nin 2024 ekonomik durumu nedir?"
    results = expert.search(query)
    
    print(f"\nSorgu: {query}")
    print(f"Sonuç sayısı: {len(results)}")
    for r in results:
        print(f"  - {r['topic']} (score: {r.get('score', 'N/A'):.2f})")


if __name__ == "__main__":
    main()
