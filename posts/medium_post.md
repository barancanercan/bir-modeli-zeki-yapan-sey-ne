# LLM'i Zeki Yapan Şey Ne? 

## Ampirik Bir Deney: Model mi? Veri mi? Orkestrasyon mu?

---

### Soru

"Bir LLM sistemini zeki yapan şey tam olarak nedir?"

Bu soru kafamda uzun zamandır dönüyordu. Üç ana faktör var:
1. **Model** - Hangi LLM'i kullanıyorsun?
2. **Veri** - Ne kadar bilgi tabanına erişiyor?
3. **Orkestrasyon** - Nasıl düşünüyor (CoT, ReAct, Reflexion...)?

Cevabı tahmin etmek yerine, **deney yaptım**.

---

## 🧪 Deney Tasarımı

### Setup
- **Senaryo**: Multi-step siyasi araştırma agent'ı
- **10 test sorusu**: Türkiye ekonomisi, ABD-Çin, AB seçimleri, Rusya-Ukrayna...
- **Platform**: Ollama (local inference)

### Değişkenler

| Faktör | Seçenekler |
|--------|------------|
| **Model** | qwen3.5 (6.6GB), qwen2.5:7b (4.7GB), phi3 (2.2GB) |
| **Veri** | Empty, Basic, Comprehensive |
| **Orkestrasyon** | CoT, ReAct, ReWOO, Reflexion |

**Toplam**: 3 × 3 × 4 × 10 = **360 kombinasyon**

---

## 📊 İlk Sonuçlar

> [Deney çalıştırılacak - sonuçlar eklenecek]

### Model Karşılaştırması
| Model | Boyut | Ortalama Puan | Ortalama Süre |
|-------|-------|---------------|---------------|
| qwen3.5 | 6.6GB | TBD | TBD |
| qwen2.5:7b | 4.7GB | TBD | TBD |
| phi3 | 2.2GB | TBD | TBD |

### Orkestrasyon Karşılaştırması
| Pattern | Ortalama Puan | Notlar |
|---------|---------------|--------|
| CoT | TBD | Sadece düşün |
| ReAct | TBD | Düşün + Eyle |
| ReWOO | TBD | Planla + Paralle |
| Reflexion | TBD | Kendini eleştir |

### Bilgi Seviyesi Etkisi
| Seviye | Ortalama Puan |
|--------|---------------|
| Empty | TBD |
| Basic | TBD |
| Comprehensive | TBD |

---

## 🔍 Ön Gözlemler

> Deney tamamlandıktan sonra doldurulacak

1. **Model boyutu önemli mi?** Küçük model büyük veri ile yetişebiliyor mu?
2. **Veri mi, orkestrasyon mu?** Hangisi daha çok etkiliyor?
3. **Orkestrasyon pattern'i ne kadar kritik?**

---

## 💡 Deneyden Çıkarılan Dersler

[Tamamlandıktan sonra yazılacak]

---

## 🎯 Sonuç

> "Zeka" tek bir şeyden değil, üç faktörün etkileşiminden doğuyor.

Devamı için deneyin GitHub'daki kodlarını inceleyebilir veya kendi bilgisayarınızda çalıştırabilirsiniz.

**GitHub**: [Link eklenecek]
**LinkedIn**: [Link eklenecek]

---

*Bu deney, yerel sistemimdeki Ollama modelleri ile yapıldı. Siz de farklı modeller ve senaryolarla deneyebilirsiniz.*
