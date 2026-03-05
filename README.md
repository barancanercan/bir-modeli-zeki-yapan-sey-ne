# 🧠 LLM'i Zeki Yapan Şey Ne? 

> Ampirik bir deney: Model mi? Veri mi? Orkestrasyon mu?

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Ollama](https://img.shields.io/badge/Ollama-Local-orange.svg)](https://ollama.ai/)
[![FAISS](https://img.shields.io/badge/FAISS-VectorDB-blue)](https://github.com/facebookresearch/faiss)
[![scipy](https://img.shields.io/badge/scipy-Statistics-green)](https://scipy.org/)

Bu proje, bir LLM sisteminin "zeka" düzeyini belirleyen faktörleri test eden kapsamlı bir deneydir.

---

## 🤖 Agent Swarm Mimarisi

Bu proje **4 uzman agent** ve **1 meta-agent** kullanarak çalışır:

```
┌─────────────────────────────────────────────────────────────────┐
│                    👑 Meta-Agent Swarm                          │
│                 (experiment/swarm.py)                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    │
│  │   Agent 1    │    │   Agent 2    │    │   Agent 3    │    │
│  │ 🇹🇷 Siyaset  │    │  🔬 Bilim    │    │  💻 Kod/ML   │    │
│  │  Uzmanı      │    │  Denetçi     │    │  Mimarisi    │    │
│  └──────────────┘    └──────────────┘    └──────────────┘    │
│         │                    │                    │            │
│         ▼                    ▼                    ▼            │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    │
│  │  + FAISS RAG │    │  + scipy     │    │+ Tool Calling│    │
│  │  + Güncel    │    │  + ANOVA     │    │  + Retry     │    │
│  │    Veri      │    │  + Metrics   │    │  + Async     │    │
│  └──────────────┘    └──────────────┘    └──────────────┘    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Agent 1: 🇹🇷 Türkiye Siyaseti Uzmanı
- **Dosya**: `experiment/agents/politics_expert.py`
- **Görev**: Knowledge Base genişletme, RAG sistemi kurulumu
- **Teknoloji**: FAISS vector database, semantic search

### Agent 2: 🔬 Bilimsel Denetim Uzmanı
- **Dosya**: `experiment/agents/science_expert.py`
- **Görev**: Deney tasarımı, istatistiksel analiz
- **Teknoloji**: scipy, ANOVA, t-test, effect size, confidence intervals

### Agent 3: 💻 Kod/ML Mimarisi Uzmanı
- **Dosya**: `experiment/agents/code_expert.py`
- **Görev**: Kod iyileştirme, tool calling, error handling
- **Teknoloji**: Real ReAct with tools, retry logic, async execution

### Agent 4: 👑 Meta-Agent Swarm Orchestrator
- **Dosya**: `experiment/swarm.py`
- **Görev**: Tüm agentları koordinasyon, workflow yönetimi

---

## 📊 Deney Tasarımı

### Test Edilen Faktörler

| Faktör | Değişkenler |
|--------|-------------|
| **Model** | qwen3.5 (6.6GB), qwen2.5:7b (4.7GB), phi3 (2.2GB) |
| **Veri (Knowledge Base)** | Empty, Basic, Comprehensive, FAISS-RAG |
| **Orkestrasyon** | CoT, ReAct (tool calling), ReWOO, Reflexion |

### Metrikler (Gelişmiş)

| Metrik | Açıklama |
|--------|-----------|
| Task Completion | Görev tamamlandı mı? |
| Latency | Toplam süre (saniye) |
| First Token Time | İlk token süresi |
| Token Count | Input/output token sayısı |
| Consistency Score | Aynı soru 3 kez → varyans |
| User Score | Manuel kalite puanı (1-10) |
| Statistical Sig. | p-value, effect size |

---

## 🚀 Kurulum

```bash
# 1. Bağımlılıkları yükle
pip install -r requirements.txt

# 2. Ollama modellerini kontrol et
ollama list

# 3. FAISS index oluştur (Agent 1)
python -c "from experiment.agents.politics_expert import PoliticsExpert; p = PoliticsExpert(); p.build_index()"

# 4. Meta-agent ile deneyi çalıştır
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
│   ├── score_results.py    # Manuel puanlama aracı
│   │
│   ├── agents/             # 🤖 Uzman Agentlar
│   │   ├── __init__.py
│   │   ├── politics_expert.py   # 🇹🇷 Agent 1: RAG + FAISS
│   │   ├── science_expert.py    # 🔬 Agent 2: Statistics
│   │   └── code_expert.py       # 💻 Agent 3: Tool Calling
│   │
│   ├── orchestrations/     # Orkestrasyon modülleri
│   │   ├── cot.py          # Chain of Thought
│   │   ├── react.py        # ReAct (gerçek tool calling)
│   │   ├── rewoo.py        # ReWOO
│   │   └── reflexion.py    # Reflexion
│   │
│   └── metrics/            # Metrik sistemi
│       ├── __init__.py
│       ├── statistics.py   # scipy tabanlı istatistik
│       └── evaluation.py   # LLM-as-Judge
│
├── data/
│   ├── test_queries.json   # 10 test sorusu
│   ├── knowledge_bases/    # Bilgi tabanları
│   │   ├── empty/
│   │   ├── basic/
│   │   └── comprehensive/
│   └── raw/               # Ham veriler (Agent 1 tarafından işlenir)
│
└── results/               # Sonuçlar (auto-generated)
    ├── experiments/
    └── analysis/
```

---

## 🎯 Kullanım

### Meta-Agent Swarm (Önerilen)
```bash
python -m experiment.swarm
```

### Manuel Çalıştırma
```bash
# Sadece deneyi çalıştır
python -m experiment.run_experiment

# Sonuçları puanla
python -m experiment.score_results

# İstatistiksel analiz yap
python -c "from experiment.metrics.statistics import StatisticalAnalyzer; s = StatisticalAnalyzer(); s.analyze()"
```

### FAISS Knowledge Base Oluştur
```bash
python -c "from experiment.agents.politics_expert import PoliticsExpert; p = PoliticsExpert(); p.build_index()"
```

---

## 🔬 Senaryo

**Multi-step Research Agent**: Siyaset konulu araştırma sorularına yanıt üreten bir agent.

### Test Soruları
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

## 📈 Örnek Çıktı

```json
{
  "experiment_id": "exp_001",
  "timestamp": "2025-03-05T12:00:00",
  "model": "qwen3.5:latest",
  "orchestration": "react",
  "knowledge_level": "faiss_rag",
  "metrics": {
    "task_completion": true,
    "latency_seconds": 4.2,
    "first_token_time": 0.3,
    "input_tokens": 512,
    "output_tokens": 256,
    "consistency_score": 0.85,
    "user_score": 8
  },
  "statistics": {
    "p_value": 0.023,
    "effect_size": 0.45,
    "confidence_interval": [0.72, 0.98]
  }
}
```

---

## 📝 Lisans

MIT License
