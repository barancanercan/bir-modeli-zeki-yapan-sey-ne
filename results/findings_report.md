# Deney Bulguları: Bir Modeli Zeki Yapan Şey Ne?

> **Deney Tarihi:** Mart 2026
> **Metodoloji:** Faktöriyel Deney Tasarımı (3×4×3)
> **Toplam Deney:** 360 | **Başarı Oranı:** %99.4

---

## Deney Özeti

| Parametre | Değerler |
|-----------|----------|
| **Modeller** | smart (qwen3.5), medium (qwen2.5:7b), dumb (phi3) |
| **Orkestrasyonlar** | CoT, ReAct, ReWOO, Reflexion |
| **Bilgi Seviyeleri** | empty, basic, comprehensive |
| **Test Sorguları** | 10 soru (Türkiye siyasi/ekonomik konular) |

---

## Temel Bulgular

### 1. Model Performansı

| Model | Başarı Oranı | Kalite | Ort. Süre | Değerlendirme |
|-------|--------------|--------|-----------|---------------|
| **medium (qwen2.5:7b)** | 120/120 (%100) | **%93** | **19.1s** | EN İYİ |
| smart (qwen3.5) | 119/120 (%99) | %87 | 261.9s | Çok yavaş |
| dumb (phi3) | 119/120 (%99) | %70 | 26.0s | Sürpriz! |

**Önemli Bulgu:** phi3 (dumb) artık çalışıyor! ReWOO ve Reflexion ile %100 kalite elde etti.

---

### 2. Orkestrasyon Performansı (KRİTİK DEĞİŞİM!)

| Orkestrasyon | Kalite | Ort. Süre | Değerlendirme |
|--------------|--------|-----------|---------------|
| **ReWOO** | **%100** | 141.9s | EN GÜVENİLİR |
| **Reflexion** | **%99** | 118.1s | ÇOK İYİ |
| CoT | %91 | 111.9s | İyi |
| ReAct | %47 | 37.3s | SORUNLU |

**Kritik Bulgu:** Orkestrasyon artık önemli! Önceki deneyde fark yoktu çünkü tüm orkestrasyonlar aynı kodu çalıştırıyordu (bug). Düzeltme sonrası ReWOO ve Reflexion belirgin şekilde üstün.

---

### 3. Bilgi Seviyesi (RAG) Etkisi

| Bilgi Seviyesi | Kalite | Ort. Süre | Değerlendirme |
|----------------|--------|-----------|---------------|
| **empty** | **%87** | 80.9s | EN İYİ |
| basic | %83 | 100.1s | Orta |
| comprehensive | %82 | 126.0s | En yavaş |

**Şaşırtıcı Bulgu:** Daha fazla bilgi = daha iyi sonuç DEĞİL! Model kendi bilgisiyle daha iyi performans gösteriyor.

---

## En İyi Kombinasyonlar

| Sıra | Kombinasyon | Kalite | Süre | Not |
|------|-------------|--------|------|-----|
| 🥇 | medium + empty | %98 | 11.5s | EN HIZLI + EN KALİTELİ |
| 🥇 | medium + reflexion | %100 | 11.9s | MÜKEMMEL |
| 🥇 | medium + cot | %100 | 19.8s | KLASİK AMA ETKİLİ |
| 🥇 | medium + rewoo | %100 | 37.5s | EN GÜVENİLİR |
| 🥈 | dumb + rewoo | %100 | 39.0s | SÜRPRİZ! |

---

## Model + Orkestrasyon Detaylı Analiz

| Kombinasyon | Kalite | Süre | Yorum |
|-------------|--------|------|-------|
| medium+cot | %100 | 19.8s | Mükemmel balans |
| medium+react | %73 | 7.1s | En hızlı ama kalite düşük |
| medium+reflexion | %100 | 11.9s | En iyi hız/kalite |
| medium+rewoo | %100 | 37.5s | Güvenilir |
| smart+cot | %86 | 293.6s | Çok yavaş |
| smart+reflexion | %100 | 309.7s | Kaliteli ama maliyetli |
| smart+rewoo | %100 | 349.1s | Aşırı yavaş |
| dumb+cot | %86 | 33.1s | İyi sürpriz |
| dumb+react | %0 | 0.0s | Tool calling desteklemiyor |
| dumb+reflexion | %97 | 32.8s | Beklenmedik başarı |
| dumb+rewoo | %100 | 39.0s | Harika! |

---

## Model + Knowledge Level Analizi

| Kombinasyon | Kalite | Süre |
|-------------|--------|------|
| medium+empty | %98 | 11.5s |
| medium+basic | %92 | 12.4s |
| medium+comprehensive | %90 | 33.3s |
| smart+empty | %90 | 209.8s |
| smart+basic | %88 | 263.8s |
| smart+comprehensive | %88 | 317.4s |
| dumb+empty | %72 | 26.7s |
| dumb+basic | %70 | 24.0s |
| dumb+comprehensive | %69 | 28.0s |

---

## Sorunlu Kombinasyonlar

| Kombinasyon | Kalite | Sorun |
|-------------|--------|-------|
| dumb+react | %0 | phi3 tool calling desteklemiyor |
| smart+react | %67 | ReAct genel olarak sorunlu |
| medium+react | %73 | ReAct tool calling problemi |

---

## İstatistiksel Gözlemler

1. **Başarı Oranı:** %99.4 (358/360 deney başarılı)
2. **Hata Türleri:** JSON parse hatası (2 deney)
3. **Süre Dağılımı:** 0s - 349s arası (standart sapma yüksek)
4. **Kalite Korelasyonu:** Model > Orkestrasyon > Knowledge Level

---

## Önceki Deneyle Karşılaştırma

| Metrik | Önceki Deney | Güncel Deney | Değişim |
|--------|--------------|--------------|---------|
| Orkestrasyon farkı | Yok | **Var** | ✅ Bug düzeltildi |
| phi3 performansı | %0 | **%70** | ✅ Fallback eklendi |
| ReWOO kalitesi | %39 | **%100** | ✅ Doğru implementasyon |
| Knowledge level etkisi | Belirsiz | **Negatif** | ⚠️ RAG etkisiz |

---

## Sonuç ve Çıkarımlar

### Ana Bulgular

1. **Model kalitesi hala kritik** - Ancak mutlak belirleyici değil
2. **Orkestrasyon artık önemli** - ReWOO ve Reflexion üstün performans gösteriyor
3. **RAG bekleneni vermiyor** - Daha fazla bilgi daha iyi sonuç değil
4. **Küçük modeller şaşırttı** - phi3 doğru orkestrasyon ile kullanılabilir

### Pratik Öneriler

| Senaryo | Önerilen Kombinasyon |
|---------|---------------------|
| Hız öncelikli | medium + reflexion + empty |
| Kalite öncelikli | medium + rewoo + empty |
| Düşük kaynak | dumb + rewoo + empty |
| Genel kullanım | medium + cot + empty |

---

## Araştırma Sorusunun Cevabı

> **"Bir modeli zeki yapan şey nedir?"**

### Kısa Cevap:
**Model + Orkestrasyon kombinasyonu** - Tek başına ne model ne de orkestrasyon yeterli değil.

### Uzun Cevap:
1. **Model kapasitesi temel** - Ama en büyük en iyi değil (medium > smart)
2. **Orkestrasyon çarpan etkisi** - Doğru teknik ile küçük model bile başarılı
3. **RAG değil, reasoning** - Harici bilgi yerine düşünme yeteneği önemli
4. **Verimlilik anahtarı** - Optimum nokta hız ve kalite dengesi

---

## Oluşturulan İçerikler

- [LinkedIn Post](../posts/linkedin_post.md)
- [Medium Blog Yazısı](../posts/medium_post.md)
- [README](../README.md)

---

# SONUÇ: BİR MODELİ ZEKİ YAPAN ŞEY = MODEL + DOĞRU ORKESTRASYON

*"Zeka, ham güç değil - strateji ve uygulama kombinasyonudur."*
