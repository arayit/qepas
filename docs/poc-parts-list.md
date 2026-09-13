# PoC malzeme listesi — kapalı döngü bitki odacığı + ADM

Hedef bileşik: metil salisilat (CAS 119-36-8).
Döngü sırası: **odacık → filtre → PCD → ADM → pompa → iğne vana → MFC → odacık**

---

## A. Elimizde olanlar (satın alınmayacak)

| Parça | Not |
|---|---|
| Thorlabs ADM01 | QTF f₀ 12458,83 Hz, mikrorezonatör Ø1,6 × 12,4 mm |
| MIRcat darbeli EC-QCL | 1111–2000 cm⁻¹ |
| Lock-in | 1f genlik modülasyonu |
| Alicat MFC, 200 sccm | Döngüde **akış ölçer** olarak, gaz seçimi "Air" |
| Alicat MFC, 10 sccm | Kalibrasyon seyreltmesi için |
| Alicat PCD, 15 PSIA | Kör dal basınç okuyucu; Inlet + Exhaust kapalı |
| İğne vana | Mevcut QEPAS hattından |
| N₂ tüpü | Sadece deneyler arası süpürme |

---

## B. Satın alınacak — gaz hattı

| # | Parça | Şartname | Adet |
|---|---|---|---|
| 1 | **Sirkülasyon pompası** | Yağsız diyafram, **PTFE kaplı diyafram** (NBR/EPDM olmaz), sızdırmaz kafa, fırçasız DC (devir ayarlanabilsin), düşük ısınma. Serbest akış 0,5–1 L/dk sınıfı. Aday: KNF NMP830 KTDC, KNF NMP015, Parker T5-1IC | 1 |
| 2 | **Partikül filtresi** | Hat içi, 0,45 µm **PTFE** membran, PTFE veya SS gövde, 6 mm bağlantı. ADM'yi kirlenmeden korur | 1 + 5 yedek membran |
| 3 | **PTFE boru** | 6 mm dış / 4 mm iç çap | 5 m |
| 4 | **Sıkıştırmalı rakor** | 6 mm boru için, SS veya pirinç, düz birleştirme. **Push-in pnömatik rakor olmaz** | 14 |
| 5 | **T rakor** | 6 mm, SS. PCD kör dalı + süpürme portu | 3 |
| 6 | **Duvar geçiş rakoru (bulkhead)** | 6 mm, SS veya PTFE. Odacık giriş + çıkış | 2 |
| 7 | **Kapama vanası** | 6 mm, süpürme portu için | 1 |

> **Sipariş öncesi mutlaka doğrula:** ADM01'in gaz portu diş tipi, PCD'nin fiziksel port tipi (1/8" NPT mi, sıkıştırmalı mı), MFC port tipi. Rakor bunlara göre seçilir, tersi değil. 6 mm ile 1/4" aynı şey değildir.

---

## C. Satın alınacak — odacık

| # | Parça | Şartname | Adet |
|---|---|---|---|
| 8 | **Cam kavanoz** | 1 L borosilikat, geniş ağız, PTFE astarlı kapak. Hacim küçüldükçe derişim artar | 1 |
| 9 | Plastik kutu | 400 × 300 × 400 mm PP/PE, kapaklı — kavanozu ve ışığı içine alan dış kabuk | mevcut |
| 10 | **Silikon conta** | Kutu kapağı için | 1 m |
| 11 | **T/RH sensörü** | SHT31 veya muadili, kayıt alınacak | 1 |
| 12 | **Eldiven portu** | Nitril eldiven + kelepçe, kutu ön yüzüne iki delik. Kapak açmadan kesim | 2 takım |
| 13 | Makas | Paslanmaz, odacık içinde kalacak | 1 |

---

## D. Satın alınacak — test bileşiği ve kalibrasyon

| # | Parça | Şartname | Adet |
|---|---|---|---|
| 14 | **Metil salisilat** | CAS 119-36-8, **reaktif saflığı ≥%99**. Kış yeşili yağı ALMA, o bir karışım | 100 mL |
| 15 | **Mikrolitre şırınga** | 10 µL gaz sızdırmaz. Tek doz ~0,2–1 µL | 1 |
| 16 | **Kalibrasyon kaynağı** | İki seçenek: (a) termostatlı cam kabarcıklandırıcı, ucuz ama doygunluğun doğrulanması gerekir; (b) sertifikalı permeasyon tüpü + fırın, pahalı ama tartışmasız | 1 |

---

## E. Satın alınmayacak ama gerekli — veri

| Ne | Nereden | Niçin |
|---|---|---|
| Metil salisilatın **nicel** gaz fazı spektrumu | PNNL/NWIR kütüphanesi (Sharpe ve ark. 2004, Appl Spectrosc 58:1452) veya DTIC ADA392033 | Elimizdeki NIST spektrumunun soğurma ölçeği keyfi. Gerçek kesit, mV/ppm ve LOD ancak bununla çıkar |

---

## Notlar

**Akış.** Kapalı döngüde akış derişimi belirlemez, sadece karışma süresini ve akış
gürültüsünü belirler. Hedef 200–300 sccm. 1 L kavanozu 3–5 dakikada bir çevirir.
30 L kutuyu aynı akış 100–150 dakikada çevirir — bu yüzden gazın biriktiği hacim
kavanoz olmalı, kutu sadece dış kabuk.

**Kısma her zaman pompadan sonra.** Pompa ADM'nin emme tarafında; ADM ile kutu
arası atmosfer basıncında kalır. İğne vana pompa çıkışında. Pompa DC ise vanayı
hiç kullanmadan voltajla ayarlamak en temizi, pompa da zorlanmaz.

**Malzeme.** Gazın değdiği her yüzey cam, metal veya PTFE olacak (Tholl 2006;
Jansen 2011). Poliüretan/naylon boru ve NBR O-ring uçucuları emer, sonra geri
verir — hayalet sinyal olur.

**Set noktaları.** Birincil 1304,7 cm⁻¹, teyit bandı 1254,1 cm⁻¹. İkisinin oranı
sabit kalmalı; nem kayarsa 1310 oynar, 1254 oynamaz.
