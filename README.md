# Crypto Technical Dashboard

Dashboard analisis teknikal kripto real-time menggunakan CoinGecko API.

## Fitur
- Harga real-time (CoinGecko Free API, cache 60 detik)
- Candlestick chart + EMA 20/50
- Support & Resistance Channels (algoritma pivot point)
- Fibonacci Retracement (7 level)
- RSI (14), MACD (12,26,9)
- Sinyal Beli/Jual dengan TP1, TP2, Stop Loss, R/R ratio
- Pair: BTC, ETH, BNB, SOL, XRP, ADA, DOGE, AVAX
- Periode: 1d, 7d, 14d, 30d, 90d

## Deploy ke Streamlit Cloud

1. Upload folder ini ke GitHub (repository baru)
2. Buka https://share.streamlit.io
3. Klik "New app"
4. Pilih repository, branch: main, file: app.py
5. Klik "Deploy"

## Struktur file

```
├── app.py           # aplikasi utama
├── requirements.txt # dependencies
└── README.md
```

## Jalankan lokal

```bash
pip install -r requirements.txt
streamlit run app.py
```
