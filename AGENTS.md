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
```

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
