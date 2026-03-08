# Bir Modeli Zeki Yapan Şey Ne?

## 360 Deneyin Ortaya Çıkardığı Şaşırtıcı Gerçekler

---

**"Daha büyük model = daha iyi sonuç"** diye düşünüyorsanız, bu yazı sizi rahatsız edecek.

Geçtiğimiz aylarda yapay zeka dünyasında bir yarış izledik: GPT-4, Claude 3, Gemini Ultra... Her biri bir öncekinden daha büyük, daha güçlü, daha "zeki" olma iddiasıyla sahneye çıktı. Şirketler milyarlarca parametre ile övünürken, biz geliştiriciler de bu dev modellere erişim için cüzdanlarımızı açtık.

Ama bir dakika. **Gerçekten büyük model her zaman kazanıyor mu?**

Ben de aynı soruyu sordum. Ve cevabı bulmak için kolları sıvadım.

---

### Herkesin Gözden Kaçırdığı Soru

Sektörde yaygın bir inanış var: Modelin zekasını artırmak istiyorsan, ya daha büyük bir model kullan, ya da ona daha fazla bilgi ver. RAG (Retrieval-Augmented Generation) sistemleri bu yüzden bu kadar popüler. "Modele doğru bilgiyi ver, o da doğru cevabı üretsin" mantığı kulağa son derece makul geliyor.

Peki ya bu varsayım yanlışsa?

Ya bir modeli gerçekten "zeki" yapan şey, ona verdiğimiz bilgi değil de, **onu nasıl çalıştırdığımızsa**?

---

### 360 Deney, 1 Gerçek

Bu soruların peşine düştüm. Laboratuvar ortamında değil, gerçek dünya senaryolarında. **360 farklı deney** tasarladım:

- Farklı model boyutları (küçükten dev modellere)
- Farklı mimari yaklaşımlar (tek model vs. çoklu agent)
- Farklı bilgi erişim stratejileri (RAG seviyeleri: boş, temel, kapsamlı)
- Farklı orkestrasyon teknikleri

Sonuçlar beni de şaşırttı.

**RAG sistemleri beklediğim etkiyi yaratmadı.** Daha fazla bilgi vermek, her zaman daha iyi sonuç anlamına gelmiyordu. Ama asıl bomba şuydu: **Küçük modeller, doğru orkestrasyon ile dev modelleri geçebiliyordu.**

---

### Bu Yazıda Ne Bulacaksınız?

Bu makalede, 360 deneyin ham verilerinden çıkardığım bulguları sizinle paylaşacağım:

- Neden "bilgi tabanı" yaklaşımı sanıldığı kadar etkili değil
- Orkestrasyon neden modelin kendisinden daha kritik
- Küçük modelleri "zeki" yapan mimari sırlar
- Ve en önemlisi: **Kendi projelerinizde nasıl uygulayabileceğiniz pratik çıkarımlar**

Hazırsanız, başlayalım.

---

## Metodoloji

### Deney Tasarımı

Bu çalışmada, LLM'lerin "zekasını" belirleyen faktörleri izole etmek için **tam faktöriyel deney tasarımı** kullandık. Bu yaklaşım, her bağımsız değişkenin etkisini ayrı ayrı ölçmemize olanak tanır.

**Deney Matrisi:**

| Faktör | Seviyeler | Açıklama |
|--------|-----------|----------|
| **Model Kapasitesi** | 3 | Farklı parametre boyutları |
| **Orkestrasyon** | 4 | Reasoning stratejileri |
| **Bilgi Seviyesi** | 3 | RAG entegrasyon derinliği |
| **Test Soruları** | 10 | Türkiye bağlamında sorular |

**Toplam Deney Sayısı:** 3 × 4 × 3 × 10 = **360 bağımsız deney**

### Model Seçimi

Parametre boyutu ve "zeka" ilişkisini test etmek için kasıtlı olarak farklı kapasitelerde üç model seçtik:

| Model | Parametre | Boyut | Hipotez Rolü |
|-------|-----------|-------|--------------|
| **Qwen3.5** | ~8B | 6.6 GB | "Akıllı" - Yüksek kapasite |
| **Qwen2.5:7b** | 7B | 4.7 GB | "Orta" - Referans model |
| **Phi3:mini** | 3.8B | 2.2 GB | "Zayıf" - Düşük kapasite |

### Orkestrasyon Stratejileri

Dört farklı reasoning pattern'i test ettik:

1. **Chain of Thought (CoT):** Adım adım düşünme, ara çıkarımları açıkça ifade etme
2. **ReAct:** Düşünce-Aksiyon-Gözlem döngüsü, araç kullanımı ile entegre reasoning
3. **ReWOO:** Planlama ve yürütmeyi ayıran, önce tam plan sonra execution yaklaşımı
4. **Reflexion:** Kendi çıktısını değerlendirip iteratif iyileştirme yapan self-critique mekanizması

### Bilgi Seviyeleri (Knowledge Levels)

RAG sisteminin etkisini ölçmek için üç seviye tasarladık:

- **Empty:** RAG devre dışı, sadece model'in parametrik bilgisi
- **Basic:** Temel Türkiye verileri (genel istatistikler, ana olaylar)
- **Comprehensive:** Detaylı ve güncel veriler (ekonomik göstergeler, siyasi analizler, tarihsel bağlam)

### Teknik Altyapı

```
┌─────────────────────────────────────────────────┐
│                 Deney Framework'ü               │
├─────────────────────────────────────────────────┤
│  LLM Inference    │  Ollama (local deployment)  │
│  Vector Search    │  FAISS (similarity search)  │
│  Orchestration    │  LangChain (agent framework)│
│  Embedding        │  nomic-embed-text           │
└─────────────────────────────────────────────────┘
```

**Multi-Agent Mimarisi:** Dört uzman agent paralel çalışarak farklı perspektifler sunar:
- **Politics Expert:** Siyasi analiz ve değerlendirmeler
- **Science Expert:** Akademik ve bilimsel yaklaşım
- **Code Expert:** Veri analizi ve hesaplamalar
- **Meta-Agent:** Sentez ve final cevap üretimi

### Değerlendirme Metrikleri

Her deney için üç temel metrik ölçtük:

| Metrik | Ölçüm Yöntemi | Aralık |
|--------|---------------|--------|
| **Başarı Oranı** | Task completion (binary) | 0-1 |
| **Kalite Skoru** | Cevap değerlendirmesi | 0-100% |
| **Latency** | End-to-end response süresi | Saniye |

---

## Bulgular

### Model Performansı: Beklenmedik Şampiyon

Deneyimizin en çarpıcı sonucu, orta sınıf modelin hem en hızlı hem de en kaliteli sonuçları üretmesi oldu.

```
┌─────────────────────────────────────────────────────────────┐
│                    MODEL PERFORMANSI                        │
├─────────────────┬────────────┬─────────────┬───────────────┤
│ Model           │ Kalite     │ Süre        │ Verimlilik    │
├─────────────────┼────────────┼─────────────┼───────────────┤
│ medium (qwen2.5)│ ████████░░ │ ▓░░░░░░░░░  │ ★★★★★         │
│ 7B parametreli  │ %93        │ 19.1s       │ En verimli    │
├─────────────────┼────────────┼─────────────┼───────────────┤
│ smart (qwen3.5) │ ███████░░░ │ ▓▓▓▓▓▓▓▓▓▓  │ ★★☆☆☆         │
│ Büyük model     │ %87        │ 261.9s      │ 13.7x yavaş   │
├─────────────────┼────────────┼─────────────┼───────────────┤
│ dumb (phi3)     │ ██████░░░░ │ ▓░░░░░░░░░  │ ★★★☆☆         │
│ Küçük model     │ %70        │ 26.0s       │ Hızlı ama zayıf│
└─────────────────┴────────────┴─────────────┴───────────────┘
```

**Şaşırtıcı Bulgu #1:** "Smart" model, "medium" modelden hem **6 puan daha düşük kalite** üretmiş hem de **13.7 kat daha yavaş** çalışmıştır. Bu, "daha büyük = daha iyi" varsayımını kesinlikle çürütmektedir.

---

### Orkestrasyon Stratejileri: Yapı Her Şeyi Değiştiriyor

Orkestrasyon yaklaşımları arasındaki fark dramatik boyutlara ulaştı:

```
ORKESTRASYON ETKİNLİĞİ

ReWOO      ████████████████████████████████████████ %100  141.9s
Reflexion  ███████████████████████████████████████░ %99   118.1s
CoT        ██████████████████████████████████████░░ %91   111.9s
ReAct      ███████████████████░░░░░░░░░░░░░░░░░░░░░ %47   37.3s
           ─────────────────────────────────────────
           0%       25%       50%       75%      100%
```

**Şaşırtıcı Bulgu #2:** ReAct, en hızlı strateji olmasına rağmen **%47 kalite** ile ciddi şekilde geride kaldı. Öte yandan ReWOO, planlama aşamasına yatırım yaparak **mükemmel sonuç** elde etti.

**Kritik İçgörü:** Reflexion'ın öz-düzeltme mekanizması, CoT'a göre sadece 6 saniye daha yavaş çalışırken **8 puanlık kalite artışı** sağladı.

---

### Bilgi Tabanı Paradoksu

En beklenmedik sonuç bilgi tabanı deneyinden geldi:

```
┌────────────────────────────────────────────┐
│         BİLGİ SEVİYESİ vs KALİTE           │
├────────────────┬───────────────────────────┤
│ empty (boş)    │ ████████████████░░ %87    │
│ basic          │ ███████████████░░░ %83    │
│ comprehensive  │ ███████████████░░░ %82    │
└────────────────┴───────────────────────────┘
```

**Şaşırtıcı Bulgu #3:** Daha fazla bilgi, daha **düşük** performansa yol açtı! Boş bilgi tabanı, kapsamlı olandan **5 puan daha iyi** sonuç üretti.

---

### Altın Kombinasyonlar

```
┌─────────────────────────────────────────────────────────────┐
│                  EN İYİ KOMBİNASYONLAR                      │
├──────┬─────────────────────┬──────────┬─────────────────────┤
│ Sıra │ Kombinasyon         │ Kalite   │ Süre                │
├──────┼─────────────────────┼──────────┼─────────────────────┤
│  🥇  │ medium + reflexion  │ %100     │ 11.9s  ← EN HIZLI   │
│  🥈  │ medium + cot        │ %100     │ 19.8s               │
│  🥉  │ dumb + rewoo        │ %100     │ 39.0s               │
└──────┴─────────────────────┴──────────┴─────────────────────┘
```

**Nihai Bulgu:** Zayıf bir model (dumb/phi3), doğru orkestrasyon stratejisi (ReWOO) ile **mükemmel sonuç** üretebiliyor.

---

## Tartışma

### Büyük Model Yanılgısı

Bu araştırmanın en çarpıcı bulgusu, AI sektörünün temel varsayımlarından birini sorgulatıyor: **Daha büyük model gerçekten daha iyi mi?**

Sonuçlarımız açıkça gösteriyor ki `medium` seviye model, `smart` modelden tutarlı biçimde daha iyi performans sergiliyor. Smart model, 13 kat daha yavaş çalışmasına rağmen anlamlı bir kalite artışı sağlayamıyor.

Peki sektör neden sürekli olarak "daha büyük = daha iyi" varsayımına sarılıyor? Bunun birkaç nedeni olabilir: pazarlama baskısı, benchmark oyunları ve belki de daha derin bir sorun - **modellerin gerçek dünya görevlerinde nasıl davrandığını ölçmekte zorlanıyoruz**.

### RAG Paradoksu

Belki de en şaşırtıcı bulgumuz RAG ile ilgili. RAG destekli konfigürasyonlar, RAG'sız versiyonlarından **sistematik olarak daha kötü** performans gösterdi.

Üç olası açıklama:

1. **Gürültü Hipotezi**: Retrieve edilen dokümanlar, modelin dikkatini dağıtan irrelevant bilgi içeriyor olabilir.

2. **Self-Knowledge Üstünlüğü**: Bu görevler için modelin internal knowledge'ı, external retrieval'dan daha güvenilir olabilir.

3. **Implementation Quality**: Basit bir RAG implementasyonu, hiç RAG kullanmamaktan daha kötü olabilir.

### Orkestrasyon: Göz Ardı Edilen Kritik Faktör

**ReWOO ve Reflexion'ın üstünlüğü**, orkestrasyon deseninin model seçiminden bile daha kritik olabileceğini gösteriyor. `phi3` gibi küçük bir modelin ReWOO ile %100 doğruluk yakalaması, bu argümanı güçlendiriyor.

Reflexion'ın self-critique mekanizması başka bir boyut ekliyor: **Model kendi hatalarını düzeltebilirse, ilk cevabın doğruluğu daha az kritik hale geliyor**.

### Pratik Çıkarımlar

- **Model büyüklüğüne değil, görev uyumluluğuna odaklanın**
- **RAG'ı varsayılan olarak eklemeyin** - her use case için değerini kanıtlayın
- **Orkestrasyon deseni seçimine model seçimi kadar zaman ayırın**
- **Küçük model + doğru orkestrasyon**, büyük model + basit prompt'tan üstün olabilir

---

## Sonuç: Zekayı Yaratan Şey Model Değil, Orkestrasyon

Bu deney serisinin bize öğrettiği en önemli ders şu: **Bir modeli zeki yapan şey, modelin kendisi kadar onu nasıl kullandığınızdır.**

### Üç Temel Bulgu

**1. Model seçimi önemli, ama tek başına yeterli değil.**
En güçlü modeli alıp naive bir şekilde kullanmak, orta seviye bir modeli akıllıca orkestre etmekten daha kötü sonuç verebilir.

**2. Orkestrasyon çarpan etkisi yapıyor.**
ReWOO ve Reflexion gibi stratejiler, aynı model üzerinde %15-25 oranında performans artışı sağladı.

**3. RAG her zaman cevap değil.**
RAG eklemek her senaryoda fayda sağlamadı; hatta bazı durumlarda performansı düşürdü.

### Pratik Rehber

| Senaryonuz | Önerimiz |
|------------|----------|
| **Hız öncelikli** | Orta model + Reflexion + RAG'sız |
| **Kalite öncelikli** | Orta model + ReWOO + RAG'sız |
| **Düşük kaynak** | Küçük model + ReWOO + RAG'sız |

### Sıra Sizde

Bu deneylerin tüm kodu açık kaynak olarak GitHub'da mevcut.

Sizden ricam:
- Kodu indirin ve kendi use case'lerinizde deneyin
- Farklı model kombinasyonlarını test edin
- Sonuçlarınızı toplulukla paylaşın

---

**Unutmayın: Zeki bir sistem inşa etmek için en pahalı modeli satın almanız gerekmiyor. Doğru orkestrasyon stratejisini seçmeniz gerekiyor.**

*Model + Doğru Orkestrasyon = Gerçek Zeka*

---

*Bu makale, 360 bağımsız deneyin sonuçlarına dayanmaktadır. Tüm kod ve veriler açık kaynak olarak paylaşılmıştır.*

---

**Etiketler:** #MachineLearning #LLM #AI #RAG #Orchestration #AgentSystems #ArtificialIntelligence

---

## Yazar Hakkında

**Baran Can Ercan** — Yapay zeka, LLM sistemleri ve agent mimarileri üzerine araştırmalar yapıyorum. Karmaşık konuları anlaşılır kılmayı ve bulguları toplulukla paylaşmayı seviyorum.

Diğer yazılarıma ve projelerime ulaşmak için:

[Medium @barancanercan](https://medium.com/@barancanercan)

Sorularınız veya işbirliği önerileriniz için Medium üzerinden bana ulaşabilirsiniz.