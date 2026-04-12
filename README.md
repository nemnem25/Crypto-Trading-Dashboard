# Crypto Trading Signal App (CTSA)

**v10.0** · Beta · Python & Streamlit · Data: CoinGecko API

---

## Tentang Aplikasi

CTSA adalah dashboard analisis teknikal kripto berbasis Python yang menggabungkan 9 indikator teknikal, Support/Resistance Channels, Fibonacci Retracement, Volume Profile Visible Range (VPVR), simulasi Monte Carlo, dan Fear & Greed Index dalam satu tampilan terpadu. Dirancang untuk membantu trader — dari pemula hingga berpengalaman — membuat keputusan entry dan exit yang lebih terstruktur berdasarkan data, bukan intuisi semata.

Tersedia untuk **57 pasangan aset** · Data real-time via CoinGecko Free API · Auto-refresh opsional 60 detik.

---

## Deploy ke Streamlit Cloud

1. Upload folder ini ke GitHub sebagai repository baru (public atau private)
2. Buka [share.streamlit.io](https://share.streamlit.io) dan login dengan akun GitHub
3. Klik **New app** → pilih repository → branch `main` → file: `app.py`
4. Klik **Deploy** — Streamlit Cloud otomatis install semua dependencies dari `requirements.txt`

URL app: `https://namamu-appname.streamlit.app`

### Jalankan secara lokal

```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## Struktur File

```
├── app.py           # Aplikasi utama (~2.160 baris)
├── requirements.txt # Dependencies Python
└── README.md        # Dokumentasi ini
```

---

## Fitur Lengkap

### Header Aplikasi

- Logogram CTSA — ikon lingkaran hitam dengan grafik harga hijau dan titik pivot kuning, muncul di sidebar dan pojok kanan header
- Nama aplikasi **Crypto Trading Signal App** dengan versi dan badge BETA
- Pair aktif, harga real-time, persentase perubahan 24 jam dengan warna dinamis
- Border kiri header berubah warna sesuai arah pergerakan harga (hijau naik / merah turun)
- Strip deskripsi singkat aplikasi di bawah header

### Chart Utama

- **Candlestick OHLC** — default hijau/merah, dapat diganti ke **Heikin-Ashi** via sidebar
- **EMA 20 & EMA 50** — golden cross dan death cross terlihat langsung di chart
- **Sinyal Beli/Jual** — segitiga hijau di bawah low candle (beli) dan segitiga merah di atas high candle (jual)
- **Support & Resistance Channels** — zona ditampilkan sebagai area warna
- **Fibonacci Retracement** — 7 level sebagai garis putus-putus berwarna

### Sub-chart Indikator

| Panel | Indikator | Keterangan |
|-------|-----------|------------|
| Panel 2 | RSI (14) | Garis ungu · overbought >70 / oversold <30 |
| Panel 2 | Stochastic RSI %K & %D | Garis biru & kuning putus-putus (opsional) |
| Panel 3 | MACD (12,26,9) | Histogram + garis MACD + Signal line |
| Panel 4 | ATR (14) | Area fill ungu — ukuran volatilitas harian |
| Panel 5 | ADX + DI+/DI- | Kekuatan tren · batas 25 = tren valid (opsional) |
| Panel 6 | OBV | Bar hijau/merah berdasarkan arah volume (opsional) |

### Sinyal Beli & Jual (Entry Box)

- Harga entry sebagai limit order dengan jarak persentase dari harga pasar
- Score sinyal dalam format `STRONG · score 8/12`
- Breakdown semua 9 indikator — titik hijau/merah dengan skor kontribusinya
- 3 level target profit dengan tangga visual:
  - TP1 = **R/R 2:1** — 2 ATR dari entry (standar profesional, tepat 2.00)
  - TP2 = **R/R 4:1** — 4 ATR dari entry
  - TP3 = **R/R 6:1+** — dari resistance/support S/R channel terdekat (dinamis)
- Stop Loss = 1 ATR dari entry
- Tombol aksi berubah warna dan teks sesuai kekuatan sinyal
- Peringatan otomatis bila sinyal MODERATE/WEAK berlawanan tren utama

Kekuatan sinyal:

| Label | Score | Artinya |
|-------|-------|---------|
| STRONG | ≥ 6 | Mayoritas indikator sepakat — layak dieksekusi |
| MODERATE | 3–5 | Sebagian sepakat — perlu konfirmasi tambahan |
| WEAK | < 3 | Sedikit konfirmasi — sebaiknya skip |

### Support / Resistance Channels

Implementasi algoritma Pine Script SR Channels oleh LonesomeTheBlue, dikonversi ke Python:

- Lebar channel dihitung dinamis dari 1.5× ATR — menghindari collapsed channels
- Pivot High/Low dideteksi otomatis, channel digabung berdasarkan proximity
- Deduplikasi channel yang overlap, ambil 8 terkuat
- Tabel: tipe zona, Low–High, lebar, jarak dari harga, pivot hits, bar sentuh, strength, rekomendasi aksi
- Callout support terdekat (hijau) dan resistance terdekat (merah)

### Fibonacci Retracement

- Swing High & Low dari 60 candle terakhir
- 7 level: 0%, 23.6%, 38.2%, 50%, 61.8%, 78.6%, 100%
- Tabel jarak dari harga sekarang dengan label posisi (above / below / AT LEVEL)

### VPVR — Volume Profile Visible Range *(baru di v10)*

Panel independen — sinyal beli/jual murni dari struktur volume, tidak melibatkan indikator teknikal lainnya. Hanya aktif untuk periode **30 hari** dan **90 hari**.

**Komponen yang ditampilkan:**

- Chart dua kolom: garis harga dengan 5 level kunci (POC, VAH, VAL, HVN, LVN) + histogram volume horizontal berwarna per level harga
- Tabel zona lengkap dari VAH hingga VAL beserta fungsi dan sinyal aksi
- Narasi posisi harga — teknikal dan bahasa awam — menjelaskan di mana harga berada relatif terhadap Value Area

**Kartu sinyal VPVR (beli & jual):**

Setiap kartu menampilkan harga entry, alasan teknikal satu baris, narasi awam satu alinea (italic), Target 1 & 2 berbasis zona volume, Stop Loss, dan R/R. Format narasi:

- Baris teknikal: "Retest POC dari atas — zona keseimbangan volume tertinggi"
- Baris awam: "Harga kembali ke titik di mana paling banyak transaksi pernah terjadi — zona beli favorit para pelaku besar."

**Level kunci VPVR:**

| Level | Definisi | Sinyal |
|-------|----------|--------|
| VAH | Batas atas Value Area (70% volume) | Resistance kuat — zona jual |
| POC | Level harga dengan volume tertinggi | Titik keseimbangan — beli saat retest |
| VAL | Batas bawah Value Area (70% volume) | Support kuat — beli agresif |
| HVN | High Volume Node (>P70 volume) | Support/resistance tambahan |
| LVN | Low Volume Node (<P30 volume) | Zona breakout cepat — waspadai |

### Simulasi Monte Carlo

- 600 simulasi Geometric Brownian Motion berbasis volatilitas historis
- Cone of uncertainty 5 layer: P10, P25, P50, P75, P90
- Garis vertikal di horizon: 3, 7, 30, 90, 365 hari
- Tabel prediksi 5 horizon waktu dengan probabilitas harga naik
- 3 metric cards: prob. naik 7, 30, 365 hari

### Fear & Greed Index

- Data dari alternative.me API (cache 1 jam)
- Gauge meter dengan warna zona
- Histori 14 hari sebagai bar chart
- Tabel interpretasi 5 zona

### Analisis Heikin-Ashi

- Panel ringkasan aktif saat checkbox HA diaktifkan
- HA Close, HA Open, warna candle, ukuran lower wick

### Narasi Teknikal (300 kata)

Di-generate otomatis dari nilai indikator aktual — 4 paragraf: tren (EMA, ADX), momentum (RSI, StochRSI, MACD), struktur harga (S/R, Fibonacci, ATR), outlook (Monte Carlo, Fear & Greed, kesimpulan). Siap disalin untuk referensi artikel atau konten.

### Ringkasan untuk Pemula (Narasi Awam)

- Hero section: verdict besar (BELI / JUAL / NETRAL) + bar kepercayaan sinyal
- Penjelasan kondisi pasar dalam bahasa sehari-hari dengan analogi
- Grid 6 kotak: tren, kekuatan, momentum, sentimen, peluang Monte Carlo, volatilitas
- Strip aksi dengan harga entry, TP1, TP2, Stop Loss
- Disclaimer investasi

---

## Pengaturan Sidebar

| Pengaturan | Pilihan | Keterangan |
|------------|---------|------------|
| Pair | 57 aset | Lihat daftar di bawah |
| Periode | 1d, 7d, 14d, 30d, 90d | Rentang data + granularitas candle |
| Heikin-Ashi | On/Off | Toggle gaya candle |
| Fibonacci | On/Off | Level Fibonacci Retracement |
| Support/Resistance | On/Off | S/R Channels |
| EMA 20/50 | On/Off | Moving average lines |
| Stochastic RSI | On/Off | %K dan %D di panel RSI |
| ADX/DI | On/Off | Panel ADX + DI+/DI- |
| OBV | On/Off | Panel On-Balance Volume |
| Sinyal Beli/Jual | On/Off | Entry box |
| Fear & Greed | On/Off | Panel sentimen |
| Monte Carlo | On/Off | Proyeksi probabilistik |
| Narasi Teknikal | On/Off | Narasi 300 kata |
| Narasi untuk Awam | On/Off | Ringkasan pemula |
| VPVR | On/Off | Volume Profile (30d & 90d) |
| Auto-refresh | On/Off | Refresh otomatis 60 detik |

### Keterangan Periode

| Periode | Granularitas | Cocok Untuk |
|---------|-------------|-------------|
| 1 hari | 30 menit | Intraday / scalping |
| 7 hari | 4 jam | Swing trading pendek |
| 14 hari | Harian | Swing trading |
| 30 hari | Harian | Position trading · VPVR aktif |
| 90 hari | Mingguan | Investasi jangka menengah · VPVR aktif |

---

## Daftar 57 Pasangan Aset

**Blue-chip:** BTC, ETH, BNB, SOL, XRP, ADA, DOGE, AVAX, TON, SHIB

**Large cap:** DOT, LINK, LTC, MATIC, UNI, ATOM, ICP, NEAR, APT, FIL, HBAR, VET, ALGO, XLM, XMR

**Mid cap / L2:** ARB, OP, INJ, SUI, TIA, IMX, STX, FTM, RUNE, THETA, EOS, NEO, ZEC, DASH, WAVES

**DeFi:** AAVE, MKR, CRV, LDO, GMX, DYDX, SNX, YFI, SUSHI, KAVA

**GameFi / NFT:** SAND, MANA, AXS, GALA

**Meme:** PEPE, BONK, WIF

---

## Sumber Data

| Data | Endpoint | Cache |
|------|----------|-------|
| OHLC (candlestick) | CoinGecko `/coins/{id}/ohlc` | 60 detik |
| Harga, market cap, volume | CoinGecko `/coins/{id}?market_data=true` | 60 detik |
| Volume harian (VPVR) | CoinGecko `/coins/{id}/market_chart` | 5 menit |
| Fear & Greed Index | alternative.me `/fng/?limit=30` | 1 jam |

Rate limit CoinGecko Free API: sekitar 10–30 request per menit. Jika error 429, tunggu 60 detik lalu refresh.

---

## Metodologi

### Risk/Reward — Standar Profesional

| Level | Kalkulasi | R/R |
|-------|-----------|-----|
| Stop Loss | Entry − 1 ATR | — |
| TP1 | Entry + 2 ATR | **2.00 : 1 (tepat)** |
| TP2 | Entry + 4 ATR | **4:1** |
| TP3 | S/R channel terdekat dinamis | **6:1+** |

R/R selalu ditampilkan **2.00:1** — hardcoded by design, bukan hasil pembulatan harga integer.

### Scoring Sinyal (Maksimum 12 Poin)

| Kondisi | Poin |
|---------|------|
| RSI oversold (<35) atau overbought (>65) | +2 |
| RSI low (35–45) atau high (55–65) | +1 |
| StochRSI cross up atau cross down | +2 |
| StochRSI oversold (<20) atau overbought (>80) | +1 |
| MACD cross up atau cross down | +2 |
| MACD positif atau negatif | +1 |
| EMA bullish atau bearish | +1 |
| ADX trending (>25) + arah DI | +2 |
| At support atau at resistance zone (<0.8%) | +2 |

### VPVR — Kalkulasi

1. Ambil data OHLCV harian via `/market_chart`
2. Bagi rentang harga (High–Low periode) menjadi 24 bucket
3. Distribusikan volume harian ke bucket secara proporsional berdasarkan overlap harga
4. POC = bucket dengan volume tertinggi
5. Value Area = bucket-bucket dengan total volume kumulatif ≥ 70%
6. HVN = bucket dengan volume > persentil ke-70
7. LVN = bucket dengan volume < persentil ke-30

### Sinyal VPVR — Logika

**Beli:** Entry di POC (jika harga di atas POC) atau di VAL (jika harga di bawah POC). Target ke VAH lalu HVN atas. Stop loss di HVN bawah terdekat.

**Jual:** Entry di VAH. Target ke POC lalu VAL. Stop loss di HVN atas terdekat.

Sinyal VPVR sepenuhnya independen dari indikator teknikal lainnya (RSI, MACD, EMA, dll).

### S/R Channel — Algoritma

Diadaptasi dari Pine Script `Support Resistance Channels` oleh LonesomeTheBlue (MPL 2.0):

1. Deteksi Pivot High/Low dengan window `n // 15` bar
2. Lebar channel = 1.5× ATR(14) — dinamis per aset
3. Pivot dalam radius channel width digabung menjadi satu zona
4. Strength = (pivot count × 10) + bar sentuh (150 bar terakhir)
5. Deduplikasi overlap, ambil 8 terkuat

### Monte Carlo — Geometric Brownian Motion

```
S(t+1) = S(t) × exp(μ + σ × Z)
```

- `μ` = rata-rata log return historis
- `σ` = standar deviasi log return historis
- `Z` ~ N(0,1)
- 600 simulasi, horizon 365 hari

---

## Disclaimer

Dashboard ini dibuat untuk tujuan **edukasi dan referensi** analisis teknikal semata. Bukan merupakan saran investasi dalam bentuk apapun. Keputusan trading sepenuhnya ada di tangan pengguna. Pasar kripto sangat volatil dan nilai investasi dapat turun secara signifikan. Selalu lakukan riset mandiri (DYOR) sebelum mengambil keputusan.

---

## Riwayat Versi

| Versi | Perubahan Utama |
|-------|-----------------|
| v1.0 | Dashboard dasar: harga, chart line, RSI, MACD |
| v2.0 | S/R Channels, Fibonacci, CoinGecko API |
| v3.0 | StochRSI, ADX, ATR, OBV, Heikin-Ashi, Fear & Greed |
| v4.0 | Entry box dengan breakdown indikator, tangga harga, R/R |
| v5.0 | TP3 dinamis, Monte Carlo, R/R 2:1, keterangan periode |
| v6.0 | Fix candlestick OHLC default, fix judul header |
| v7.0 | Fix S/R channel collapsed (ATR-based width), tabel S/R informatif |
| v8.0 | Logogram CTSA, nama aplikasi, deskripsi, fix encoding harga |
| v9.0 | Narasi teknikal 300 kata, narasi awam, 57 pair, fix HTML rendering |
| v9c | Fix R/R selalu tepat 2.00:1 — hardcoded by design |
| v10.0 | VPVR panel independen: chart, tabel zona, sinyal beli/jual murni volume, narasi teknikal + awam per sinyal |
