# 📈 Crypto Technical Dashboard

Dashboard analisis teknikal kripto **real-time** berbasis Streamlit, menggunakan data dari CoinGecko API dan Fear & Greed Index dari alternative.me.

---

## 🚀 Deploy ke Streamlit Cloud

1. Upload folder ini ke GitHub sebagai repository baru (public atau private)
2. Buka [share.streamlit.io](https://share.streamlit.io) → login dengan akun GitHub
3. Klik **New app** → pilih repository → branch `main` → file: `app.py`
4. Klik **Deploy** — Streamlit Cloud otomatis install semua dependencies

URL app akan tersedia di `https://namamu-appname.streamlit.app`

### Jalankan secara lokal

```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## 📦 Struktur File

```
├── app.py           # Aplikasi utama (~1.370 baris)
├── requirements.txt # Dependencies Python
└── README.md        # Dokumentasi ini
```

---

## ✨ Fitur Lengkap

### 📊 Chart Utama
- **Candlestick OHLC** — default hijau/merah, toggle ke **Heikin-Ashi** lewat sidebar
- **EMA 20 & EMA 50** — golden cross / death cross terlihat langsung di chart
- **Sinyal Beli/Jual** — segitiga hijau di bawah low candle (beli) dan segitiga merah di atas high candle (jual)
- **Support & Resistance Channels** — zona ditampilkan sebagai area warna di atas chart
- **Fibonacci Retracement** — 7 level (0%, 23.6%, 38.2%, 50%, 61.8%, 78.6%, 100%) sebagai garis putus-putus

### 📉 Sub-chart Indikator
| Panel | Indikator | Keterangan |
|-------|-----------|------------|
| Panel 2 | RSI (14) | Garis ungu · overbought >70 / oversold <30 |
| Panel 2 | Stochastic RSI %K & %D | Garis biru & kuning putus-putus (opsional) |
| Panel 3 | MACD (12,26,9) | Histogram + garis MACD + Signal line |
| Panel 4 | ATR (14) | Area fill ungu — ukuran volatilitas harian |
| Panel 5 | ADX + DI+/DI- | Kekuatan tren · batas 25 = tren valid (opsional) |
| Panel 6 | OBV | Bar hijau/merah berdasarkan arah perubahan volume (opsional) |

### 🎯 Sinyal Beli & Jual (Entry Box)
Setiap kartu sinyal menampilkan:
- **Harga entry** (limit order, 0.1% di bawah/atas harga pasar)
- **Breakdown semua indikator** — titik hijau/merah per indikator + skor kontribusinya
- **Score total** ditampilkan di pill: misalnya `STRONG · score 8/12`
- **3 level target profit** dengan R/R masing-masing:
  - TP1 = R/R **2:1** (2 ATR dari entry)
  - TP2 = R/R **4:1** (4 ATR dari entry)
  - TP3 = R/R **6:1+** — diambil dari resistance/support S/R channel terdekat (dinamis)
- **Stop Loss** = 1 ATR dari entry (standar profesional)
- **Tombol aksi** berubah warna dan teks sesuai kekuatan sinyal
- **Peringatan otomatis** bila sinyal MODERATE/WEAK berlawanan dengan tren utama

**Kekuatan sinyal:**
| Label | Score | Artinya |
|-------|-------|---------|
| 🟢 STRONG | ≥ 6 | Mayoritas indikator sepakat — layak dieksekusi |
| 🟡 MODERATE | 3–5 | Sebagian sepakat — perlu konfirmasi tambahan |
| ⚪ WEAK | < 3 | Sedikit konfirmasi — sebaiknya skip |

### 🧱 Support / Resistance Channels
Implementasi algoritma dari **Pine Script SR Channels** (LonesomeTheBlue), dikonversi ke Python:
- Lebar channel dihitung dinamis dari **1.5× ATR** (bukan persentase tetap)
- Pivot High/Low dideteksi otomatis, channel digabung berdasarkan proximity
- Deduplikasi channel yang overlap
- Tabel menampilkan: tipe (Support/Resistance/Inside), zona Low–High, lebar, jarak dari harga, pivot hits, bar sentuh, strength label, dan **rekomendasi aksi**
- Callout otomatis untuk **support terdekat** (hijau) dan **resistance terdekat** (merah)

### 🌀 Fibonacci Retracement
- Swing High dan Swing Low dihitung dari 60 candle terakhir
- 7 level: 0%, 23.6%, 38.2%, 50%, 61.8%, 78.6%, 100%
- Tabel jarak dari harga sekarang + label posisi (above / below / AT LEVEL)

### 🎲 Simulasi Monte Carlo
- **600 simulasi** Geometric Brownian Motion berbasis volatilitas historis
- **Cone of uncertainty** 5 layer: P10, P25, P50 (median), P75, P90
- Garis vertikal penanda di horizon: 3, 7, 30, 90, 365 hari
- **Tabel prediksi** untuk 5 horizon waktu:
  - Pesimis (P10), Bawah (P25), Median (P50), Atas (P75), Optimis (P90)
  - Probabilitas harga naik di setiap horizon
- 3 metric cards: prob. naik 7 hari, 30 hari, 365 hari
- Expander penjelasan cara membaca Monte Carlo

### 😨 Fear & Greed Index
- Data dari **alternative.me API** (cache 1 jam)
- Gauge meter animasi dengan warna sesuai zona
- Histori 14 hari sebagai bar chart
- Tabel interpretasi 5 zona (Extreme Fear → Extreme Greed)
- Callout otomatis saat kondisi ekstrem terdeteksi

### 🕯️ Analisis Heikin-Ashi
- Tampil saat checkbox HA diaktifkan di sidebar
- Panel ringkasan: HA Close, HA Open, warna candle, ukuran lower wick
- Lower wick sangat kecil = tren kuat (tidak ada tekanan balik)

---

## ⚙️ Pengaturan Sidebar

| Pengaturan | Pilihan | Keterangan |
|------------|---------|------------|
| Pair | BTC, ETH, BNB, SOL, XRP, ADA, DOGE, AVAX | Aset yang dianalisis |
| Periode | 1h, 7d, 14d, 30d, 90d | Rentang data + granularitas candle |
| Heikin-Ashi | On/Off | Toggle gaya candle (HA vs OHLC biasa) |
| Fibonacci | On/Off | Tampilkan/sembunyikan level Fib |
| Support/Resistance | On/Off | Tampilkan/sembunyikan S/R channels |
| EMA 20/50 | On/Off | Tampilkan/sembunyikan EMA lines |
| Stochastic RSI | On/Off | Panel RSI menampilkan %K dan %D |
| ADX/DI | On/Off | Tambah panel ADX + DI+/DI- |
| OBV | On/Off | Tambah panel On-Balance Volume |
| Sinyal Beli/Jual | On/Off | Tampilkan/sembunyikan entry box |
| Fear & Greed | On/Off | Tampilkan/sembunyikan panel sentimen |
| Monte Carlo | On/Off | Tampilkan/sembunyikan proyeksi probabilistik |
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

## 🔌 Sumber Data

| Data | Sumber | Cache |
|------|--------|-------|
| OHLC (candlestick) | CoinGecko `/coins/{id}/ohlc` | 60 detik |
| Harga, market cap, volume | CoinGecko `/coins/{id}?market_data=true` | 60 detik |
| Fear & Greed Index | alternative.me `/fng/?limit=30` | 1 jam |

> **Rate limit:** CoinGecko Free API ±10–30 request/menit. Jika muncul error 429, tunggu 60 detik lalu refresh. Cache 60 detik sudah dipasang untuk meminimalkan request.

---

## 📐 Metodologi Indikator

### R/R (Risk/Reward) — Standar Profesional
- **Stop Loss** = entry − 1 ATR (risiko tetap dan terukur)
- **TP1** = entry + 2 ATR → R/R **2:1**
- **TP2** = entry + 4 ATR → R/R **4:1**
- **TP3** = resistance/support S/R channel terdekat → R/R **6:1+** (dinamis)

### Scoring Sinyal
Setiap indikator berkontribusi poin ke buy score atau sell score:

| Kondisi | Poin |
|---------|------|
| RSI oversold (<35) atau overbought (>65) | +2 |
| RSI low (35–45) atau high (55–65) | +1 |
| StochRSI cross up/down | +2 |
| StochRSI oversold/overbought | +1 |
| MACD cross up/down | +2 |
| MACD positif/negatif | +1 |
| EMA bullish/bearish | +1 |
| ADX trending (>25) + DI arah | +2 |
| At support/resistance zone (<0.8%) | +2 |
| **Total maksimum** | **12** |

### S/R Channel — Algoritma
Diadaptasi dari Pine Script `Support Resistance Channels` oleh LonesomeTheBlue (MPL 2.0):
1. Deteksi Pivot High/Low dengan window `n // 15` bar
2. Lebar channel = 1.5× ATR(14) — dinamis per aset
3. Pivot dalam radius cwidth digabung jadi satu zona
4. Strength = (jumlah pivot × 10) + jumlah bar yang menyentuh zona (150 bar terakhir)
5. Deduplikasi zona yang overlap, ambil 8 terkuat

### Monte Carlo — Geometric Brownian Motion
```
S(t+1) = S(t) × exp(μ + σ × Z)
```
Di mana:
- `μ` = rata-rata log return historis (drift)
- `σ` = standar deviasi log return historis (volatilitas)
- `Z` = bilangan acak distribusi normal standar
- 600 simulasi, horizon hingga 365 hari

---

## ⚠️ Disclaimer

Dashboard ini dibuat untuk tujuan **edukasi dan referensi** analisis teknikal. Bukan merupakan saran investasi. Selalu lakukan riset mandiri (DYOR) sebelum mengambil keputusan trading. Pasar kripto sangat volatil dan berisiko tinggi.

---

## 📋 Versi

| Versi | Perubahan |
|-------|-----------|
| v1.0 | Dashboard dasar: harga, chart line, RSI, MACD |
| v2.0 | Tambah S/R Channels, Fibonacci, CoinGecko API |
| v3.0 | Tambah StochRSI, ADX, ATR, OBV, Heikin-Ashi, Fear & Greed |
| v4.0 | Upgrade entry box: breakdown indikator, tangga harga, R/R |
| v5.0 | Tambah TP3, Monte Carlo, R/R 2:1, keterangan periode |
| v6.0 | Fix judul tidak terlihat, fix candlestick OHLC default, sinyal di atas/bawah candle |
