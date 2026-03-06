# LLM'i Zeki Yapan Şey Ne?

## Ampirik Bir Deney: Model mi? Veri mi? Orkestrasyon mu?

---

### Soru

*"Bir LLM sistemini zeki yapan şey tam olarak nedir?"*

Bu soru kafamda uzun zamandır dönüyordu. Üç ana faktör var:

1. **Model** — Hangi LLM'i kullanıyorsun?
2. **Veri** — Ne kadar bilgi tabanına erişiyor?
3. **Orkestrasyon** — Nasıl düşünüyor (CoT, ReAct, Reflexion...)?

Cevabı tahmin etmek yerine, **deney yaptım**.

---

## 🧪 Deney Tasarımı

### Setup
- **Senaryo**: Multi-step siyasi araştırma agent'ı
- **10 test sorusu**: Türkiye ekonomisi, ABD-Çin, AB seçimleri, Rusya-Ukrayna...
- **Platform**: Ollama (local inference)
- **Embedding**: FAISS vector database

### Değişkenler

| Faktör | Seçenekler |
|---------|------------|
| **Model** | qwen3.5 (smart), qwen2.5:7b (medium), phi3 (dumb) |
| **Veri** | Empty, Basic, Comprehensive + FAISS-RAG |
| **Orkestrasyon** | CoT, ReAct, ReWOO, Reflexion |

**Toplam**: 3 × 3 × 4 × 10 = **360 kombinasyon**

---

## 🎯 Nihai Sonuçlar

### 1. Model En Kritik Faktör

| Model | Kalite | Süre |
|-------|--------|------|
| **qwen2.5:7b (medium)** | **6.5/10** ⭐ | 18s |
| qwen3.5 (smart) | 5.0/10 | 109s |
| phi3 (dumb) | **0.0/10** ❌ | 0.02s |

**🤯 ŞOK SONUC**: En büyük model en iyi DEĞİL! Orta boy model en başarılı!

### 2. Orkestrasyon Farkı Yok

| Orkestrasyon | Kalite |
|--------------|--------|
| CoT | 3.9/10 |
| ReAct | 3.9/10 |
| ReWOO | 3.9/10 |
| Reflexion | 3.7/10 |

**🤯 Tüm orkestrasyonlar neredeyse aynı!** "İleri teknikler" fark yaratmıyor.

### 3. Bilgi (RAG) Etkisi Zayıf

| Bilgi Seviyesi | Kalite |
|-----------------|--------|
| Empty (RAG yok) | 4.2/10 |
| Comprehensive | 4.0/10 |
| Basic | 3.3/10 |

**🤯 Daha fazla bilgi = daha iyi sonuç DEĞİL!**

### 4. En İyi Kombinasyon

🥇 **qwen2.5:7b + CoT**: 7.0/10  
🥈 qwen2.5:7b + ReAct: 6.7/10  
🥉 qwen2.5:7b + Reflexion: 6.3/10

---

## 💡 Ne Öğrendik?

### ❌ Yanlış Bildiklerimiz:
- "Daha büyük model = daha iyi sonuç"
- "ReAct/Reflexion standart CoT'ten daha iyi"
- "RAG her zaman cevap kalitesini artırır"

### ✅ Doğru Olan:
- **Model seçimi kritik** - phi3 tamamen başarısız
- **Orta boy model optimal** - hem hızlı hem kaliteli
- **Basit orkestrasyon yeterli** - gereksiz karmaşıklık yok

---

## 🏗️ Sistem Mimarisi

Bu proje **Agent Swarm** pattern'i ile çalışıyor:

```
┌──────────────────────────────────────┐
│     Meta-Agent Swarm Orchestrator    │
├──────────────────────────────────────┤
│  🇹🇷 Agent 1: Knowledge + FAISS     │
│  🔬 Agent 2: Statistics + scipy      │
│  💻 Agent 3: Tool Calling + Retry   │
└──────────────────────────────────────┘
```

### Agent 1: Türkiye Siyaseti Uzmanı
- FAISS vector database
- Semantic search
- 2024-2025 güncel veriler

### Agent 2: Bilimsel Denetim Uzmanı
- ANOVA, t-test
- Cohen's d (effect size)
- Confidence intervals

### Agent 3: Kod/ML Mimarisi
- Real ReAct with tool calling
- Retry with exponential backoff
- Async execution

---

## 🎯 Pratik Çıkarımlar

1. **Model seçimi en önemli karar** - Doğru modeli seçin
2. **Orkestrasyona fazla yatırım yapmayın** - Basit tutun
3. **RAG her zaman gerekli değil** - Sadece bilgi tabanı sorularınız varsa kullanın
4. **Orta boy modeller optimal** - Maliyet/performans dengesi en iyi

---

## 🔬 Deney Metodolojisi

### Test Senaryosu
- Türkiye siyasi ve ekonomik analiz soruları
- Multi-step reasoning gerektiren sorgular
- 10 farklı konu kategorisi

### Değerlendirme Kriterleri
- Anlamlı cevap var mı? ("Cevap bulunamadı" değil)
- Cevap uzunluğu (>30 karakter)
- İlgili bilgi içeriyor mu?

### İstatistiksel Analiz
- ANOVA testi
- t-test
- Cohen's d (effect size)
- Confidence intervals

---

## 🌐 Kaynaklar

- **GitHub**: [Proje Kodu](https://github.com/barancanercan/bir-modeli-zeki-yapan-sey-ne)
- **Bulgular Raporu**: [results/findings_report.md](results/findings_report.md)

---

## ❓ Son Söz

> *"Zeka" tek bir şeyden değil, ama bu deney gösterdi ki: en önemli faktör MODEL'in kendisidir.*

Daha büyük model = daha zeki değil. İleri orkestrasyon = daha iyi sonuç değil. RAG = her zaman çözüm değil.

**Doğru modeli seçin, basit tutun, gereksiz karmaşıklıktan kaçının.**

---

*Bu deney, yerel sistemimdeki Ollama modelleri ile yapıldı. Siz de farklı modeller ve senaryolarla deneyebilirsiniz.*

---

#BIR_MODELI_ZEKI_YAPAN_SEH: MODELDIR! - ORKESTRASYON_DEGIL, VERI_DEGIL, SADECE_MODELDIR!
