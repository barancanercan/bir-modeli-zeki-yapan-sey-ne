# AGENTS.md - Proje Çalıştırma Rehberi

## Kurulum

### 1. Ollama Kurulumu
```bash
# Ollama'yı indir ve kur
# https://ollama.ai

# Modelleri kontrol et
ollama list
```

### 2. Python Bağımlılıkları
```bash
# Virtual environment oluştur
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# veya
.venv\Scripts\activate  # Windows

# Bağımlılıkları yükle
pip install -r requirements.txt
```

---

## 🤖 Agent Swarm Kullanımı

### Meta-Agent Swarm (Önerilen)
```bash
# Tam deneyi agent swarm ile çalıştır
python -m experiment.swarm

# Limitli çalıştır
python -m experiment.swarm --limit 2

# Puanlama modu
python -m experiment.swarm --score
```

---

## 👑 Agent Yapısı

### Agent 1: 🇹🇷 Türkiye Siyaseti Uzmanı
**Dosya**: `experiment/agents/politics_expert.py`

```python
from experiment.agents import PoliticsExpert

expert = PoliticsExpert()

# FAISS index oluştur
expert.build_index()

# Semantic search
results = expert.search("Türkiye ekonomi 2024")

# Bağlam oluştur
context = expert.get_context_for_query("Soru?", max_docs=5)
```

### Agent 2: 🔬 Bilimsel Denetim Uzmanı
**Dosya**: `experiment/agents/science_expert.py`

```python
from experiment.agents import ScienceExpert

expert = ScienceExpert()

# Sonuçları yükle
results = expert.load_results()

# Analiz raporu oluştur
report = expert.generate_report(results)

# Kaydet
expert.save_report(results, "analysis.json")
```

**İstatistiksel Testler**:
- ANOVA (f_oneway)
- t-test (ttest_ind)
- Effect Size (Cohen's d)
- Confidence Intervals
- Correlation (Pearson, Spearman)

### Agent 3: 💻 Kod/ML Mimarisi Uzmanı
**Dosya**: `experiment/agents/code_expert.py`

```python
from experiment.agents import ToolCallingReAct

# Tool calling ile ReAct
react = ToolCallingReAct("phi3:latest", max_iterations=5)
result = react.run("Soru", knowledge_list)
```

**Özellikler**:
- Gerçek tool calling (LangChain tools)
- Retry with exponential backoff
- Graceful degradation

---

## Deneyi Çalıştırma

### Tam Deney (Tüm Kombinasyonlar)
```bash
python -m experiment.run_experiment
```

Bu komut:
- 10 test sorusu × 3 model × 4 orkestrasyon × 3 bilgi seviyesi = 360 deney çalıştırır
- Sonuçları `results/` klasörüne JSON olarak kaydeder

### Hızlı Test (Sınırlı)
```bash
# Sadece 2 soru ve comprehensive bilgi ile dene
python -c "
from experiment import ExperimentRunner
r = ExperimentRunner()
r.run_all(limit_queries=2, limit_combinations=True)
"
```

## Puanlama

Deney tamamlandıktan sonra:

```bash
python -m experiment.score_results
```

Bu komut:
- Her sonuç için cevabı gösterir
- 1-10 arası puan ister
- Puanları sonuç dosyasına kaydeder

## Sonuçları İnceleme

### CSV İndir
```bash
python -c "
from experiment import ExperimentRunner
r = ExperimentRunner()
r.export_csv('analysis.csv')
"
```

### Özet Tablo
```python
from experiment import ExperimentRunner
r = ExperimentRunner()
print(r.get_summary_table())
```

### İstatistiksel Analiz
```python
from experiment.agents import ScienceExpert

expert = ScienceExpert()
results = expert.load_results()

# Model bazlı analiz
model_analysis = expert.analyze_by_model(results)

# Orkestrasyon analizi
orch_analysis = expert.analyze_by_orchestration(results)

# Tutarlılık skoru
consistency = expert.calculate_consistency(results)
```

## Konfigürasyon

`config.yaml` dosyasını düzenleyebilirsiniz:

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

knowledge_levels:
  - empty
  - basic
  - comprehensive
```

---

## Yeni Orkestrasyon Ekleme

1. `experiment/orchestrations/` klasörüne yeni Python dosyası oluştur
2. `run` metodu olan bir class yaz
3. `config.yaml`'da listeye ekle

Örnek:
```python
# my_orch.py
class MyOrchestration:
    def __init__(self, model_name, temperature=0.7):
        self.llm = ChatOllama(model=model_name, temperature=temperature)
    
    def run(self, query, knowledge=None):
        # Implementasyon
        return {"result": "..."}
```
