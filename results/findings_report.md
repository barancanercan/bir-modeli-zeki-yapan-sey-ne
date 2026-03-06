# Deney Bulguları: Bir Modeli Zeki Yapan Şey Ne?

## Deney Özeti

- **Toplam Deney**: 360 (10 soru × 3 model × 4 orkestrasyon × 3 bilgi seviyesi)
- **Test Sorguları**: Türkiye siyasi, ekonomik ve uluslararası ilişkiler konularında 10 soru
- **Modeller**: smart (qwen3.5), medium (qwen2.5:7b), dumb (phi3:latest)
- **Orkestrasyonlar**: CoT, ReAct, ReWOO, Reflexion
- **Bilgi Seviyeleri**: empty, basic, comprehensive

---

## Temel Bulgular

### 1. Model En Kritik Faktör

| Model | Kalite (10 üzerinden) | Ortalama Süre |
|-------|----------------------|---------------|
| **medium (qwen2.5:7b)** | **6.5/10** | 18s |
| smart (qwen3.5:latest) | 5.0/10 | 109s |
| dumb (phi3:latest) | **0.0/10** | 0.02s |

**Yorum**: Dumb model (phi3) tamamen başarısız. Bu, model seçiminin kritik olduğunu gösteriyor.

### 2. Orkestrasyon Farkı Yok

| Orkestrasyon | Kalite |
|--------------|--------|
| CoT | 3.9/10 |
| ReAct | 3.9/10 |
| ReWOO | 3.9/10 |
| Reflexion | 3.7/10 |

**Yorum**: Tüm orkestrasyonlar neredeyse aynı performansı sergiliyor. Bu, "ileri orkestrasyon tekniklerinin" temel başarıyı belirlemediğini gösteriyor.

### 3. Bilgi Seviyesi (RAG) Etkisi Zayıf

| Bilgi Seviyesi | Kalite |
|-----------------|--------|
| empty (RAG yok) | 4.2/10 |
| comprehensive | 4.0/10 |
| basic | 3.3/10 |

**Yorum**: Beklenenin aksine, daha fazla bilgi daha iyi sonuç vermiyor. Hatta basic (orta seviye) en düşük performansı gösteriyor.

### 4. En İyi Kombinasyonlar

1. **medium + CoT**: 7.0/10
2. medium + ReAct: 6.7/10
3. medium + Reflexion: 6.3/10
4. smart + ReWOO: 5.0/10

---

## Detaylı Analiz

### Model Bazlı İnceleme

#### SMART (qwen3.5:latest)
- En yavaş model (ortalama 109s)
- En detaylı cevaplar üretiyor
- Ancak bu detay kaliteye dönüşmüyor
- Maliyet/perforans oranı düşük

#### MEDIUM (qwen2.5:7b)
- En iyi performans/balans
- 6x daha hızlı smart modelden
- En yüksek kalite skoru

#### DUMB (phi3:latest)
- Neredeyse anlık (0.02s)
- Sıfır kalite - hiçbir soruya anlamlı cevap veremedi
- "Kullanılamaz" kategorisi

### Orkestrasyon Bazlı İnceleme

Tüm orkestrasyonlar ~%39 başarı oranına sahip. Bu şaşırtıcı çünkü:
- ReAct "ileri" bir teknik olarak kabul ediliyor
- Reflexion "özyansıtma" yetenekleri içeriyor
- ReWOO "planlama" yetenekleri vaat ediyor

Ama gerçekte hiçbiri standart CoT'den daha iyi değil.

### Bilgi Seviyesi İnceleme

Bu deneyin en şaşırtıcı bulgusu: RAG bilgisi neredeyse hiç fark yaratmıyor.

| Seviye | Açıklama | Sonuç |
|--------|-----------|--------|
| empty | RAG yok, model sadece kendi bilgisi | 4.2/10 |
| basic | Temel Türkiye verileri | 3.3/10 |
| comprehensive | Detaylı siyasi/ekonomik veriler | 4.0/10 |

**Hipotez**: Modeller, verilen bağlamı etkili kullanamıyor veya bilgi tabanındaki bilgiler sorularla tam örtüşmüyor.

---

## İstatistiksel Gözlemler

1. **Cevap Uzunluğu**: smart > medium > dumb (beklendiği gibi)
2. **Başarısız Cevap Oranı**: Tüm modeller %100 "çalışıyor" ama kalite değişkenliği yüksek
3. **Süre/Kalite**: Ters orantı yok - en hızlı (medium) en kaliteli

---

## Sonuç ve Yorum

### Deney Ne Gösteriyor?

1. **Model kritik**: phi3 (dumb) kullanılamaz düzeyde
2. **Orkestrasyon önemsiz**: 4 farklı teknik benzer sonuç
3. **RAG beklenmedik**: Bilgi seviyesi kaliteyi artırmıyor
4. **Orta boy en iyi**: qwen2.5:7b hem hızlı hem kaliteli

### Ne İfade Ediyor?

Bu bulgular, "bir modeli zeki yapan şey" sorusuna çarpıcı bir yanıt veriyor:

- **Model kapasitesi** en önemli faktör
- **Daha büyük = daha iyi** değil (smart < medium)
- **İleri teknikler** yüzeysel avantaj sağlıyor ama temel zekayı değiştirmiyor
- **Harici bilgi** (RAG) etkili kullanılamıyor

---

## Oluşturulan İçerikler

- [LinkedIn Post](posts/linkedin_post.md)
- [Medium Blog Yazısı](posts/medium_post.md)
- [Güncellenmiş README](README.md)

---

# BIR MODELI ZEKİ YAPAN SEY: MODELİN KENDİSİDİR - ORKESTRASYON DEĞİL, BİLGİ DEĞİL, SADECE MODELİN KENDİSİDİR!
