# Crypto Trading Signal App (CTSA)

**v9.0** · Beta · Dibuat dengan Python & Streamlit · Data: CoinGecko API

---

## Tentang Aplikasi

CTSA adalah dashboard analisis teknikal kripto berbasis Python yang menggabungkan 9 indikator teknikal, Support/Resistance Channels, Fibonacci Retracement, simulasi Monte Carlo, dan Fear & Greed Index dalam satu tampilan terpadu. Dirancang untuk membantu trader — dari pemula hingga berpengalaman — membuat keputusan entry dan exit yang lebih terstruktur berdasarkan data, bukan intuisi semata.

Tersedia untuk **57 pasangan aset** · Data real-time via CoinGecko Free API · Auto-refresh opsional 60 detik.

---

## Deploy ke Streamlit Cloud

1. Upload folder ini ke GitHub sebagai repository baru (public atau private)
2. Buka [share.streamlit.io](https://share.streamlit.io) dan login dengan akun GitHub
3. Klik **New app** → pilih repository → branch `main` → file: `app.py`
4. Klik **Deploy** — Streamlit Cloud otomatis install semua dependencies

URL app: `https://namamu-appname.streamlit.app`

### Jalankan secara lokal

```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## Struktur File

```
├── app.py           # Aplikasi utama (~1.840 baris)
├── requirements.txt # Dependencies Python
└── README.md        # Dokumentasi ini
```

---

## Fitur Lengkap

### Header Aplikasi

Setiap halaman menampilkan:

- Logogram CTSA (ikon lingkaran hitam dengan grafik harga hijau dan titik pivot kuning) — muncul di sidebar dan pojok kanan header
- Nama aplikasi **Crypto Trading Signal App** dengan versi dan badge BETA
- Pair aktif, harga real-time, dan persentase perubahan 24 jam dengan warna dinamis (hijau naik / merah turun)
- Border kiri header berubah warna mengikuti arah pergerakan harga
- Strip deskripsi singkat tentang aplikasi di bawah header

### Chart Utama

- **Candlestick OHLC** — default hijau/merah, dapat diganti ke **Heikin-Ashi** via sidebar
- **EMA 20 & EMA 50** — golden cross dan death cross terlihat langsung di chart
- **Sinyal Beli/Jual** — segitiga hijau di bawah low candle (beli) dan segitiga merah di atas high candle (jual), diposisikan agar tidak bertumpuk dengan body candle
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

Setiap kartu sinyal menampilkan secara lengkap:

- **Harga entry** sebagai limit order (0.1% di bawah/atas harga pasar) dengan jarak persentase dari harga pasar
- **Score sinyal** dalam format `STRONG · score 8/12` — terlihat langsung seberapa penuh konfirmasi indikator
- **Breakdown semua indikator** — titik hijau/merah per indikator dengan skor kontribusinya, termasuk indikator yang belum terpenuhi
- **3 level target profit** dengan tangga visual dan R/R masing-masing:
  - TP1 = **R/R 2:1** — 2 ATR dari entry (standar profesional)
  - TP2 = **R/R 4:1** — 4 ATR dari entry
  - TP3 = **R/R 6:1+** — diambil dari resistance/support S/R channel terdekat (dinamis)
- **Stop Loss** = 1 ATR dari entry
- **R/R ditampilkan tepat 2.00:1** — nilai eksak by design, bukan hasil pembulatan harga integer
- **Tombol aksi** berubah warna dan teks sesuai kekuatan sinyal
- **Peringatan otomatis** bila sinyal MODERATE/WEAK berlawanan dengan tren utama

Kekuatan sinyal:

| Label | Score | Artinya |
|-------|-------|---------|
| STRONG | ≥ 6 | Mayoritas indikator sepakat — layak dieksekusi |
| MODERATE | 3–5 | Sebagian sepakat — perlu konfirmasi tambahan |
| WEAK | < 3 | Sedikit konfirmasi — sebaiknya skip |

### Support / Resistance Channels

Implementasi algoritma Pine Script SR Channels oleh LonesomeTheBlue, dikonversi ke Python:

- Lebar channel dihitung dinamis dari 1.5× ATR — menghindari collapsed channels (upper=lower=mid)
- Pivot High/Low dideteksi otomatis, channel digabung berdasarkan proximity
- Deduplikasi channel yang overlap
- Tabel menampilkan: tipe (Support/Resistance/Inside), zona Low–High, lebar zona, jarak dari harga saat ini, pivot hits, bar sentuh, strength label, dan rekomendasi aksi
- Callout otomatis untuk support terdekat (hijau) dan resistance terdekat (merah)

### Fibonacci Retracement

- Swing High dan Swing Low dihitung dari 60 candle terakhir
- 7 level: 0%, 23.6%, 38.2%, 50%, 61.8%, 78.6%, 100%
- Tabel jarak dari harga sekarang dengan label posisi (above / below / AT LEVEL)

### Simulasi Monte Carlo

- 600 simulasi Geometric Brownian Motion berbasis volatilitas historis
- Cone of uncertainty 5 layer: P10, P25, P50 (median), P75, P90
- Garis vertikal penanda di horizon: 3, 7, 30, 90, 365 hari
- Tabel prediksi untuk 5 horizon waktu dengan probabilitas harga naik per horizon
- 3 metric cards: probabilitas naik 7 hari, 30 hari, 365 hari
- Expander penjelasan cara membaca hasil simulasi

### Fear & Greed Index

- Data dari alternative.me API (cache 1 jam)
- Gauge meter dengan warna zona
- Histori 14 hari sebagai bar chart
- Tabel interpretasi 5 zona (Extreme Fear hingga Extreme Greed)
- Callout otomatis saat kondisi ekstrem terdeteksi

### Analisis Heikin-Ashi

- Panel ringkasan aktif saat checkbox HA diaktifkan
- Menampilkan HA Close, HA Open, warna candle terakhir, dan ukuran lower wick
- Lower wick sangat kecil mengindikasikan tren yang kuat tanpa tekanan balik

### Narasi Teknikal (300 kata)

Panel narasi yang di-generate otomatis dari nilai indikator aktual, terdiri dari 4 paragraf:

- Paragraf 1: kondisi tren — EMA dan ADX
- Paragraf 2: momentum — RSI, StochRSI, dan MACD
- Paragraf 3: struktur harga — S/R, Fibonacci, dan ATR
- Paragraf 4: outlook — Monte Carlo, Fear & Greed, dan kesimpulan

Dilengkapi tag ringkasan dan instruksi salin — siap digunakan sebagai bahan referensi artikel atau konten.

### Ringkasan untuk Pemula (Narasi Awam)

Panel terpisah dalam bahasa sederhana tanpa istilah teknikal:

- Hero section dengan verdict besar (BELI / JUAL / NETRAL) dan bar kepercayaan sinyal dalam persen
- Penjelasan kondisi pasar menggunakan analogi sehari-hari
- Grid 6 kotak: tren, kekuatan tren, momentum, sentimen pasar, peluang Monte Carlo, volatilitas ATR
- Strip aksi dengan harga entry, TP1, TP2, dan Stop Loss
- Disclaimer investasi

---

## Pengaturan Sidebar

| Pengaturan | Pilihan | Keterangan |
|------------|---------|------------|
| Pair | 57 aset | Lihat daftar lengkap di bawah |
| Periode | 1d, 7d, 14d, 30d, 90d | Rentang data + granularitas candle |
| Heikin-Ashi | On/Off | Toggle gaya candle (HA vs OHLC) |
| Fibonacci | On/Off | Tampilkan/sembunyikan level Fibonacci |
| Support/Resistance | On/Off | Tampilkan/sembunyikan S/R channels |
| EMA 20/50 | On/Off | Tampilkan/sembunyikan EMA lines |
| Stochastic RSI | On/Off | Panel RSI menampilkan %K dan %D |
| ADX/DI | On/Off | Tambah panel ADX + DI+/DI- |
| OBV | On/Off | Tambah panel On-Balance Volume |
| Sinyal Beli/Jual | On/Off | Tampilkan/sembunyikan entry box |
| Fear & Greed | On/Off | Tampilkan/sembunyikan panel sentimen |
| Monte Carlo | On/Off | Tampilkan/sembunyikan proyeksi probabilistik |
| Narasi Teknikal | On/Off | Tampilkan/sembunyikan narasi 300 kata |
| Narasi untuk Awam | On/Off | Tampilkan/sembunyikan ringkasan pemula |
| Auto-refresh | On/Off | Refresh otomatis setiap 60 detik |

### Keterangan Periode

| Periode | Granularitas Candle | Cocok Untuk |
|---------|--------------------|----|
| 1 hari | 30 menit | Intraday / scalping |
| 7 hari | 4 jam | Swing trading pendek |
| 14 hari | Harian | Swing trading |
| 30 hari | Harian | Position trading |
| 90 hari | Mingguan | Investasi jangka menengah |

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

| Data | Sumber | Cache |
|------|--------|-------|
| OHLC (candlestick) | CoinGecko `/coins/{id}/ohlc` | 60 detik |
| Harga, market cap, volume | CoinGecko `/coins/{id}?market_data=true` | 60 detik |
| Fear & Greed Index | alternative.me `/fng/?limit=30` | 1 jam |

Rate limit CoinGecko Free API sekitar 10–30 request per menit. Jika muncul error 429, tunggu 60 detik lalu refresh.

---

## Metodologi

### Risk/Reward — Standar Profesional

| Level | Kalkulasi | R/R |
|-------|-----------|-----|
| Stop Loss | Entry − 1 ATR | — |
| Target 1 (TP1) | Entry + 2 ATR | **2:1 (tepat)** |
| Target 2 (TP2) | Entry + 4 ATR | **4:1** |
| Target 3 (TP3) | S/R channel terdekat dinamis | **6:1+** |

R/R ditampilkan sebagai **2.00:1** — nilai eksak by design. TP3 tidak simetris antara sinyal beli dan jual karena mengikuti posisi S/R channel aktual di pasar.

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

### S/R Channel — Algoritma

Diadaptasi dari Pine Script `Support Resistance Channels` oleh LonesomeTheBlue (MPL 2.0):

1. Deteksi Pivot High/Low dengan window `n // 15` bar
2. Lebar channel = 1.5× ATR(14) — dinamis per aset dan periode
3. Pivot dalam radius channel width digabung menjadi satu zona
4. Strength = (jumlah pivot × 10) + jumlah bar yang menyentuh zona dalam 150 bar terakhir
5. Deduplikasi zona yang overlap, ambil 8 terkuat

### Monte Carlo — Geometric Brownian Motion

```
S(t+1) = S(t) × exp(μ + σ × Z)
```

- `μ` = rata-rata log return historis (drift)
- `σ` = standar deviasi log return historis (volatilitas)
- `Z` = bilangan acak distribusi normal standar N(0,1)
- 600 simulasi, horizon hingga 365 hari

---

## Disclaimer

Dashboard ini dibuat untuk tujuan **edukasi dan referensi** analisis teknikal semata. Bukan merupakan saran investasi dalam bentuk apapun. Keputusan trading sepenuhnya ada di tangan pengguna. Pasar kripto sangat volatil dan nilai investasi dapat turun secara signifikan dalam waktu singkat. Selalu lakukan riset mandiri (DYOR) sebelum mengambil keputusan.

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
| v7.0 | Fix S/R channel (ATR-based width), tabel S/R informatif |
| v8.0 | Logogram CTSA, nama aplikasi di header dan sidebar, deskripsi |
| v9.0 | Narasi teknikal 300 kata, narasi awam, 57 pair aset, fix HTML rendering |
| v9c | Fix R/R selalu tepat 2.00:1 — hardcoded by design |
