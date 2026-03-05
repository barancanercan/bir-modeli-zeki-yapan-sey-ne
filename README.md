# 🧠 LLM'i Zeki Yapan Şey Ne? 

> Ampirik bir deney: Model mi? Veri mi? Orkestrasyon mu?

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Ollama](https://img.shields.io/badge/Ollama-Local-orange.svg)](https://ollama.ai/)
[![FAISS](https://img.shields.io/badge/FAISS-VectorDB-blue)](https://github.com/facebookresearch/faiss)
[![scipy](https://img.shields.io/badge/scipy-Statistics-green)](https://scipy.org/)

Bu proje, bir LLM sisteminin "zeka" düzeyini belirleyen faktörleri test eden kapsamlı bir ampirik deneydir.

---

## 🎯 Soru

Bir LLM sistemini "zeki" yapan şey tam olarak nedir?

- **Model** mi? (Daha büyük, daha güçlü model)
- **Veri** mi? (Daha fazla bilgi, RAG)
- **Orkestrasyon** mu? (Nasıl düşünüyor, CoT, ReAct, Reflexion)

Bu deney, bu üç faktörün etkileşimini ölçüyor.

---

## 🤖 Agent Swarm Mimarisi

Bu proje **4 uzman agent** ve **1 meta-agent** kullanarak çalışır:

```
┌─────────────────────────────────────────────────────────────────┐
│                    👑 Meta-Agent Swarm                          │
│                 (experiment/swarm.py)                           │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐   │
│  │   Agent 1    │    │   Agent 2    │    │   Agent 3    │   │
│  │ 🇹🇷 Siyaset  │    │  🔬 Bilim    │    │  💻 Kod/ML   │   │
│  │  Uzmanı      │    │  Denetçi     │    │  Mimarisi    │   │
│  └──────────────┘    └──────────────┘    └──────────────┘   │
│         │                    │                    │            │
│         ▼                    ▼                    ▼            │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    │
│  │  + FAISS RAG │    │  + scipy    │    │+ Tool Calling│    │
│  │  + Güncel    │    │  + ANOVA    │    │  + Retry    │    │
│  │    Veri      │    │  + Metrics  │    │  + Async    │    │
│  └──────────────┘    └──────────────┘    └──────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

### Agent 1: 🇹🇷 Türkiye Siyaseti Uzmanı
- **Dosya**: `experiment/agents/politics_expert.py`
- FAISS vector database, semantic search
- 2024-2025 güncel siyasi veriler

### Agent 2: 🔬 Bilimsel Denetim Uzmanı
- **Dosya**: `experiment/agents/science_expert.py`
- scipy, ANOVA, t-test, Cohen's d, confidence intervals

### Agent 3: 💻 Kod/ML Mimarisi Uzmanı
- **Dosya**: `experiment/agents/code_expert.py`
- Real tool calling (LangChain), retry, async execution

### Agent 4: 👑 Meta-Agent Swarm Orchestrator
- **Dosya**: `experiment/swarm.py`
- 5-phase workflow, checkpoint/resume

---

## 📊 Deney Tasarımı

### Test Edilen Faktörler

| Faktör | Değişkenler |
|--------|-------------|
| **Model** | qwen3.5 (6.6GB), qwen2.5:7b (4.7GB), phi3 (2.2GB) |
| **Veri (Knowledge Base)** | Empty, Basic, Comprehensive, FAISS-RAG |
| **Orkestrasyon** | CoT, ReAct (tool calling), ReWOO, Reflexion |

**Toplam Kombinasyon**: 3 × 3 × 4 × 10 = **360 deney**

### Metrikler

| Metrik | Açıklama |
|--------|-----------|
| Task Completion | Görev tamamlandı mı? |
| Latency | Toplam süre (saniye) |
| Token Count | Input/output token sayısı |
| Consistency Score | Aynı soru x3 → varyans |
| User Score | Manuel kalite puanı (1-10) |
| Statistical Sig. | p-value, effect size |

---

## 🚀 Kurulum

```bash
# 1. Bağımlılıkları yükle
pip install -r requirements.txt

# 2. Ollama modellerini kontrol et
ollama list

# 3. Embedding modeli indir (FAISS için)
ollama pull nomic-embed-text

# 4. FAISS index oluştur
python -c "from experiment.agents import PoliticsExpert; p = PoliticsExpert(); p.build_index()"

# 5. Deneyi çalıştır
python -m experiment.swarm
```

---

## 📁 Proje Yapısı

```
├── config.yaml              # Deney konfigürasyonu
├── requirements.txt         # Python bağımlılıkları
├── README.md               # Bu dosya
├── AGENTS.md               # Agent dokümantasyonu
│
├── experiment/
│   ├── swarm.py            # 👑 Meta-Agent Swarm Orchestrator
│   ├── run_experiment.py   # Ana deney koordinatorü
│   ├── score_results.py   # Manuel puanlama aracı
│   │
│   ├── agents/             # 🤖 Uzman Agentlar
│   │   ├── politics_expert.py   # 🇹🇷 Agent 1: FAISS RAG
│   │   ├── science_expert.py    # 🔬 Agent 2: Statistics
│   │   └── code_expert.py       # 💻 Agent 3: Tool Calling
│   │
│   └── orchestrations/     # Orkestrasyon modülleri
│       ├── cot.py          # Chain of Thought
│       ├── react.py        # ReAct
│       ├── rewoo.py        # ReWOO
│       └── reflexion.py    # Reflexion
│
├── data/
│   ├── test_queries.json  # 10 test sorusu
│   ├── knowledge_bases/    # Bilgi tabanları
│   └── faiss_index/       # FAISS vector index
│
└── results/                # Sonuçlar (auto-generated)
    ├── checkpoint.json     # Checkpoint (resume için)
    └── analysis/          # İstatistiksel analiz
```

---

## 📝 Kullanım

### Temel Komutlar

```bash
# Tam deney (360 kombinasyon)
python -m experiment.swarm

# Limitli deney
python -m experiment.swarm --limit 2

# Checkpoint temizle ve baştan başla
python -m experiment.swarm --clear

# Puanlama modu
python -m experiment.swarm --score
```

### Manuel Çalıştırma

```bash
# Sadece deneyi çalıştır
python -m experiment.run_experiment

# Sonuçları puanla
python -m experiment.score_results

# İstatistiksel analiz
python -c "from experiment.agents import ScienceExpert; s = ScienceExpert(); s.save_report(s.load_results())"
```

---

## 🔬 Test Senaryoları

1. Türkiye 2023-2024 ekonomi analizi
2. ABD-Çin ticaret savaşı
3. 2024 AB seçimleri
4. Türkiye erken seçim tartışmaları
5. Rusya-Ukrayna 2. yıl
6. Yeşil enerji ve Türkiye 2053
7. Küresel demokratik gerileme
8. 2024 ABD başkanlık seçimi
9. Orta Doğu su krizi
10. Türkiye NATO-BRICS dengesi

---

## 📈 Örnek Sonuç

```json
{
  "query_id": 1,
  "model_level": "smart",
  "orchestration": "react",
  "knowledge_level": "comprehensive",
  "success": true,
  "elapsed_seconds": 45.2,
  "user_score": 8,
  "metrics": {
    "task_completion": true,
    "latency_seconds": 45.2,
    "input_tokens": 512,
    "output_tokens": 256
  }
}
```

---

## 📊 Örnek Analiz Çıktısı

```python
{
  "summary": {
    "total_experiments": 360,
    "successful": 340,
    "success_rate": 0.94
  },
  "model_analysis": {
    "qwen3.5": {"mean_score": 7.2},
    "qwen2.5:7b": {"mean_score": 6.1},
    "phi3": {"mean_score": 4.8}
  },
  "orchestration_analysis": {
    "ReAct": {"mean_score": 6.8},
    "CoT": {"mean_score": 5.9},
    "Reflexion": {"mean_score": 6.2},
    "ReWOO": {"mean_score": 5.5}
  },
  "statistics": {
    "p_value": 0.023,
    "effect_size": 0.45
  }
}
```

---

## 🔧 Geliştirme

### Yeni Orkestrasyon Ekleme

```python
# experiment/orchestrations/my_orch.py
class MyOrchestration:
    def __init__(self, model_name, temperature=0.7):
        self.llm = ChatOllama(model=model_name, temperature=temperature)
    
    def run(self, query, knowledge=None):
        # Implementasyon
        return {"result": "..."}
```

### Konfigürasyon

`config.yaml` dosyasını düzenleyin:

```yaml
models:
  smart: "qwen3.5:latest"
  medium: "qwen2.5:7b"
  dumb: "phi3:latest"

orchestrations:
  - cot
  - react
  - rewoo
  - reflexion
```

---

## 📝 Lisans

MIT License

---

## 🙏 Teşekkürler

- [Ollama](https://ollama.ai/) - Local LLM inference
- [LangChain](https://langchain.com/) - LLM framework
- [FAISS](https://github.com/facebookresearch/faiss) - Vector similarity search
- [scipy](https://scipy.org/) - Scientific computing
