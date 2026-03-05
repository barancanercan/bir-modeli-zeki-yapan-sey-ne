# 🧠 LLM'i Zeki Yapan Şey Ne? 

> Ampirik bir deney: Model mi? Veri mi? Orkestrasyon mu?

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Ollama](https://img.shields.io/badge/Ollama-Local-orange.svg)](https://ollama.ai/)

Bu proje, bir LLM sisteminin "zeka" düzeyini belirleyen faktörleri test eden kapsamlı bir deneydir.

## 📊 Deney Tasarımı

### Test Edilen Faktörler

| Faktör | Değişkenler |
|--------|-------------|
| **Model** | qwen3.5 (6.6GB), qwen2.5:7b (4.7GB), phi3 (2.2GB) |
| **Veri (Knowledge Base)** | Empty, Basic, Comprehensive |
| **Orkestrasyon** | CoT, ReAct, ReWOO, Reflexion |

### Metrikler
- ✅ Task Completion (Otomatik)
- ⏱️ Latency (Otomatik)
- 📝 Kullanıcı Kalite Puanı (Manuel: 1-10)

## 🚀 Kurulum

```bash
# 1. Bağımlılıkları yükle
pip install -r requirements.txt

# 2. Ollama modellerini kontrol et
ollama list

# 3. Deneyi çalıştır
python -m experiment.run_experiment
```

## 📁 Proje Yapısı

```
├── config.yaml              # Deney konfigürasyonu
├── requirements.txt         # Python bağımlılıkları
├── experiment/
│   ├── run_experiment.py   # Ana deney koordinatorü
│   ├── score_results.py    # Manuel puanlama aracı
│   └── orchestrations/     # Orkestrasyon modülleri
│       ├── cot.py          # Chain of Thought
│       ├── react.py        # ReAct (Reason + Act)
│       ├── rewoo.py        # ReWOO
│       └── reflexion.py    # Reflexion
├── data/
│   ├── test_queries.json   # 10 test sorusu
│   └── knowledge_bases/    # Bilgi tabanları
│       ├── empty/
│       ├── basic/
│       └── comprehensive/
└── results/                # Sonuçlar (auto-generated)
```

## 🎯 Kullanım

### 1. Deneyi Çalıştır
```bash
python -m experiment.run_experiment
```

### 2. Sonuçları Puanla
```bash
python -m experiment.score_results
```

### 3. Sonuçları İncele
```bash
# CSV olarak dışa aktar
python -c "from experiment import ExperimentRunner; r = ExperimentRunner(); r.export_csv()"
```

## 🔬 Senaryo

**Multi-step Research Agent**: Siyaset konulu araştırma sorularına yanıt üreten bir agent.

10 test sorusu:
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

## 📝 Lisans

MIT License
