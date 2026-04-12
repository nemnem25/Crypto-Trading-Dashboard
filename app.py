import streamlit as st
import requests
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import time

st.set_page_config(
    page_title="Crypto Technical Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .block-container { padding-top: 0.5rem !important; padding-bottom: 0rem; }
    .fg-extreme-fear  { background:#fcebeb; border-radius:8px; padding:8px 12px; text-align:center; }
    .fg-fear          { background:#faeeda; border-radius:8px; padding:8px 12px; text-align:center; }
    .fg-neutral       { background:#f1efe8; border-radius:8px; padding:8px 12px; text-align:center; }
    .fg-greed         { background:#eaf3de; border-radius:8px; padding:8px 12px; text-align:center; }
    .fg-extreme-greed { background:#c0dd97; border-radius:8px; padding:8px 12px; text-align:center; }
    div[data-testid="stMetric"] { background:#f8f9fa; border-radius:8px; padding:10px 14px; }
    h1 { font-size:1.4rem !important; }
    h2 { font-size:1.1rem !important; }
    h3 { font-size:1.0rem !important; }
    .eb-card { border-radius:12px; padding:18px; border-width:1px; border-style:solid; font-family:monospace; }
    .eb-buy  { background:#eaf3de; border-color:#3b6d11; }
    .eb-sell { background:#fcebeb; border-color:#a32d2d; }
    .eb-hdr  { display:flex; align-items:center; justify-content:space-between; margin-bottom:12px; }
    .eb-label-buy  { font-size:10px; font-weight:600; letter-spacing:.7px; color:#27500a; }
    .eb-label-sell { font-size:10px; font-weight:600; letter-spacing:.7px; color:#791f1f; }
    .eb-pill-buy  { font-size:10px; font-weight:500; padding:3px 10px; border-radius:20px; background:#3b6d11; color:#eaf3de; }
    .eb-pill-sell { font-size:10px; font-weight:500; padding:3px 10px; border-radius:20px; background:#a32d2d; color:#fcebeb; }
    .eb-pill-mod  { font-size:10px; font-weight:500; padding:3px 10px; border-radius:20px; background:#854f0b; color:#faeeda; }
    .eb-pill-weak { font-size:10px; font-weight:500; padding:3px 10px; border-radius:20px; background:#5f5e5a; color:#f1efe8; }
    .eb-entry-block { margin-bottom:12px; padding-bottom:12px; border-bottom:1px solid; }
    .eb-entry-block-buy  { border-color:rgba(59,109,17,.25); }
    .eb-entry-block-sell { border-color:rgba(163,45,45,.25); }
    .eb-entry-lbl  { font-size:9px; text-transform:uppercase; letter-spacing:.5px; color:#5f5e5a; margin-bottom:2px; }
    .eb-price-buy  { font-size:26px; font-weight:600; color:#27500a; letter-spacing:-1px; line-height:1.1; }
    .eb-price-sell { font-size:26px; font-weight:600; color:#791f1f; letter-spacing:-1px; line-height:1.1; }
    .eb-price-sub  { font-size:10px; color:#5f5e5a; margin-top:3px; }
    .eb-ind-block  { margin-bottom:12px; padding-bottom:12px; border-bottom:1px solid; }
    .eb-ind-block-buy  { border-color:rgba(59,109,17,.25); }
    .eb-ind-block-sell { border-color:rgba(163,45,45,.25); }
    .eb-ind-title-buy  { font-size:9px; text-transform:uppercase; letter-spacing:.5px; color:#3b6d11; font-weight:600; margin-bottom:7px; }
    .eb-ind-title-sell { font-size:9px; text-transform:uppercase; letter-spacing:.5px; color:#a32d2d; font-weight:600; margin-bottom:7px; }
    .eb-ind-row { display:flex; align-items:center; justify-content:space-between; margin-bottom:5px; }
    .eb-ind-name { font-size:11px; color:#444441; display:flex; align-items:center; gap:6px; }
    .eb-dot-on-buy  { width:7px; height:7px; border-radius:50%; background:#3b6d11; flex-shrink:0; }
    .eb-dot-on-sell { width:7px; height:7px; border-radius:50%; background:#a32d2d; flex-shrink:0; }
    .eb-dot-off { width:7px; height:7px; border-radius:50%; background:#d3d1c7; flex-shrink:0; }
    .eb-ind-score-buy  { font-size:11px; font-weight:600; color:#3b6d11; }
    .eb-ind-score-sell { font-size:11px; font-weight:600; color:#a32d2d; }
    .eb-ind-score-off  { font-size:11px; color:#b4b2a9; }
    .eb-levels { margin-bottom:12px; }
    .eb-lev-title { font-size:9px; text-transform:uppercase; letter-spacing:.5px; color:#888; margin-bottom:8px; font-weight:500; }
    .eb-ladder { position:relative; padding-left:22px; }
    .eb-ladder-line-buy  { position:absolute; left:9px; top:8px; bottom:8px; width:2px; background:linear-gradient(to bottom,#3b6d11 0%,#3b6d11 50%,rgba(163,45,45,.4) 100%); }
    .eb-ladder-line-sell { position:absolute; left:9px; top:8px; bottom:8px; width:2px; background:linear-gradient(to bottom,rgba(59,109,17,.4) 0%,#a32d2d 50%,#a32d2d 100%); }
    .eb-lev-row { display:flex; align-items:center; justify-content:space-between; margin-bottom:7px; position:relative; }
    .eb-lev-dot { width:10px; height:10px; border-radius:50%; position:absolute; left:-18px; top:2px; border:2px solid #fff; }
    .eb-lev-key { font-size:11px; color:#5f5e5a; }
    .eb-lev-key-entry { font-size:11px; font-weight:600; color:#222; }
    .eb-lev-right { display:flex; align-items:center; gap:7px; }
    .eb-lev-price { font-size:12px; font-weight:500; color:#222; }
    .eb-lev-price-entry { font-size:13px; font-weight:700; }
    .eb-badge { font-size:9px; padding:2px 6px; border-radius:3px; font-weight:500; }
    .eb-badge-tp-buy   { background:#c0dd97; color:#27500a; }
    .eb-badge-tp-sell  { background:#f09595; color:#501313; }
    .eb-badge-sl-buy   { background:#f09595; color:#501313; }
    .eb-badge-sl-sell  { background:#c0dd97; color:#27500a; }
    .eb-badge-entry    { background:#d3d1c7; color:#444441; }
    .eb-rr-block { display:flex; align-items:center; justify-content:space-between; padding:9px 12px; border-radius:8px; margin-bottom:10px; }
    .eb-rr-buy   { background:rgba(59,109,17,.12); }
    .eb-rr-sell  { background:rgba(163,45,45,.12); }
    .eb-rr-label { font-size:9px; text-transform:uppercase; letter-spacing:.5px; color:#5f5e5a; }
    .eb-rr-val-buy  { font-size:16px; font-weight:600; color:#27500a; }
    .eb-rr-val-sell { font-size:16px; font-weight:600; color:#791f1f; }
    .eb-rr-interp { font-size:10px; color:#5f5e5a; margin-top:2px; }
    .eb-action-buy    { border-radius:8px; padding:9px 12px; text-align:center; font-size:12px; font-weight:600; background:#3b6d11; color:#eaf3de; }
    .eb-action-sell   { border-radius:8px; padding:9px 12px; text-align:center; font-size:12px; font-weight:600; background:#a32d2d; color:#fcebeb; }
    .eb-action-warn   { border-radius:8px; padding:9px 12px; text-align:center; font-size:12px; font-weight:500; background:#f1efe8; color:#444441; border:1px solid #b4b2a9; }
    .eb-advice { font-size:10px; color:#5f5e5a; text-align:center; margin-top:6px; }
</style>
""", unsafe_allow_html=True)

COINS = {
    # ── Layer 1: Blue-chip
    "BTC / USD":  "bitcoin",
    "ETH / USD":  "ethereum",
    "BNB / USD":  "binancecoin",
    "SOL / USD":  "solana",
    "XRP / USD":  "ripple",
    "ADA / USD":  "cardano",
    "DOGE / USD": "dogecoin",
    "AVAX / USD": "avalanche-2",
    "TON / USD":  "the-open-network",
    "SHIB / USD": "shiba-inu",
    # ── Layer 2: Large cap
    "DOT / USD":  "polkadot",
    "LINK / USD": "chainlink",
    "LTC / USD":  "litecoin",
    "MATIC / USD":"matic-network",
    "UNI / USD":  "uniswap",
    "ATOM / USD": "cosmos",
    "ICP / USD":  "internet-computer",
    "NEAR / USD": "near",
    "APT / USD":  "aptos",
    "FIL / USD":  "filecoin",
    "HBAR / USD": "hedera-hashgraph",
    "VET / USD":  "vechain",
    "ALGO / USD": "algorand",
    "XLM / USD":  "stellar",
    "XMR / USD":  "monero",
    # ── Layer 3: Mid cap / L2
    "ARB / USD":  "arbitrum",
    "OP / USD":   "optimism",
    "INJ / USD":  "injective-protocol",
    "SUI / USD":  "sui",
    "TIA / USD":  "celestia",
    "IMX / USD":  "immutable-x",
    "STX / USD":  "blockstack",
    "FTM / USD":  "fantom",
    "RUNE / USD": "thorchain",
    "THETA / USD":"theta-token",
    "EOS / USD":  "eos",
    "NEO / USD":  "neo",
    "ZEC / USD":  "zcash",
    "DASH / USD": "dash",
    "WAVES / USD":"waves",
    # ── Layer 4: DeFi
    "AAVE / USD": "aave",
    "MKR / USD":  "maker",
    "CRV / USD":  "curve-dao-token",
    "LDO / USD":  "lido-dao",
    "GMX / USD":  "gmx",
    "DYDX / USD": "dydx",
    "SNX / USD":  "havven",
    "YFI / USD":  "yearn-finance",
    "SUSHI / USD":"sushi",
    "KAVA / USD": "kava",
    # ── Layer 5: GameFi / NFT
    "SAND / USD": "the-sandbox",
    "MANA / USD": "decentraland",
    "AXS / USD":  "axie-infinity",
    "GALA / USD": "gala",
    # ── Layer 6: Meme
    "PEPE / USD": "pepe",
    "BONK / USD": "bonk",
    "WIF / USD":  "dogwifcoin",
}

LOGO_SVG = """
<svg viewBox="0 0 60 60" xmlns="http://www.w3.org/2000/svg">
  <circle cx="30" cy="30" r="30" fill="#111"/>
  <circle cx="30" cy="30" r="28" fill="none" stroke="#222" stroke-width="1"/>
  <path d="M9,40 L15,28 L21,33 L29,17 L37,25 L44,13 L51,19"
        fill="none" stroke="#3b6d11" stroke-width="2.4"
        stroke-linecap="round" stroke-linejoin="round"/>
  <circle cx="21" cy="33" r="2.8" fill="#ef9f27"/>
  <circle cx="37" cy="25" r="2.8" fill="#ef9f27"/>
  <line x1="9" y1="45" x2="51" y2="45" stroke="#2a2a2a" stroke-width="1.2"/>
  <text x="30" y="55" text-anchor="middle"
        font-size="8.5" font-weight="800" fill="#666"
        font-family="Arial,sans-serif" letter-spacing="1.5">CTSA</text>
</svg>
"""

DAYS_MAP = {
    "1 hari":  1,
    "7 hari":  7,
    "14 hari": 14,
    "30 hari": 30,
    "90 hari": 90,
}

CG_BASE = "https://api.coingecko.com/api/v3"


# ── DATA FETCHING ─────────────────────────────────────────────────────────────

@st.cache_data(ttl=60)
def fetch_ohlc(coin_id: str, days: int):
    url = f"{CG_BASE}/coins/{coin_id}/ohlc"
    r = requests.get(url, params={"vs_currency": "usd", "days": days}, timeout=15)
    r.raise_for_status()
    df = pd.DataFrame(r.json(), columns=["timestamp", "open", "high", "low", "close"])
    df["time"] = pd.to_datetime(df["timestamp"], unit="ms")
    return df


@st.cache_data(ttl=60)
def fetch_market(coin_id: str):
    url = f"{CG_BASE}/coins/{coin_id}"
    r = requests.get(url, params={
        "localization": "false", "tickers": "false",
        "market_data": "true", "community_data": "false", "developer_data": "false"
    }, timeout=15)
    r.raise_for_status()
    return r.json()


@st.cache_data(ttl=3600)
def fetch_fear_greed():
    try:
        r = requests.get("https://api.alternative.me/fng/?limit=30", timeout=10)
        r.raise_for_status()
        data = r.json().get("data", [])
        return data
    except Exception:
        return []


@st.cache_data(ttl=300)
def fetch_volume_chart(coin_id: str, days: int):
    url = f"{CG_BASE}/coins/{coin_id}/market_chart"
    r = requests.get(url, params={"vs_currency": "usd", "days": days}, timeout=15)
    r.raise_for_status()
    data = r.json()
    prices  = pd.DataFrame(data["prices"],  columns=["ts", "price"])
    volumes = pd.DataFrame(data["total_volumes"], columns=["ts", "volume"])
    prices["date"]  = pd.to_datetime(prices["ts"],  unit="ms").dt.date
    volumes["date"] = pd.to_datetime(volumes["ts"], unit="ms").dt.date
    daily_p = prices.groupby("date")["price"].agg(["first","max","min","last"]).reset_index()
    daily_p.columns = ["date","open","high","low","close"]
    daily_v = volumes.groupby("date")["volume"].sum().reset_index()
    merged  = daily_p.merge(daily_v, on="date")
    return merged


def calc_vpvr(df_vol: pd.DataFrame, n_buckets: int = 24):
    hi = df_vol["high"].max()
    lo = df_vol["low"].min()
    bucket_size = (hi - lo) / n_buckets
    buckets = []
    for i in range(n_buckets):
        b_lo = lo + i * bucket_size
        b_hi = b_lo + bucket_size
        b_mid = (b_lo + b_hi) / 2
        vol = 0
        for _, row in df_vol.iterrows():
            overlap = max(0, min(row["high"], b_hi) - max(row["low"], b_lo))
            rng = row["high"] - row["low"]
            if rng > 0:
                vol += row["volume"] * (overlap / rng)
        buckets.append({"price": b_mid, "lo": b_lo, "hi": b_hi, "volume": vol})

    total_vol = sum(b["volume"] for b in buckets)
    for b in buckets:
        b["vol_pct"] = b["volume"] / total_vol if total_vol > 0 else 0

    poc = max(buckets, key=lambda x: x["volume"])

    sorted_by_vol = sorted(buckets, key=lambda x: -x["volume"])
    va_vol, va_buckets = 0, []
    for b in sorted_by_vol:
        va_vol += b["volume"]
        va_buckets.append(b)
        if va_vol >= total_vol * 0.70:
            break

    vah_price = max(b["hi"]  for b in va_buckets)
    val_price = min(b["lo"]  for b in va_buckets)

    sorted_by_price = sorted(buckets, key=lambda x: x["price"])
    hvn_threshold   = np.percentile([b["volume"] for b in buckets], 70)
    lvn_threshold   = np.percentile([b["volume"] for b in buckets], 30)
    hvn_zones = [b for b in sorted_by_price if b["volume"] >= hvn_threshold
                 and abs(b["price"] - poc["price"]) / poc["price"] > 0.005]
    lvn_zones = [b for b in sorted_by_price if b["volume"] <= lvn_threshold
                 and abs(b["price"] - poc["price"]) / poc["price"] > 0.005]

    return {
        "buckets":  sorted_by_price,
        "poc":      poc["price"],
        "vah":      vah_price,
        "val":      val_price,
        "hvn_list": hvn_zones,
        "lvn_list": lvn_zones,
        "max_vol":  max(b["volume"] for b in buckets),
        "bucket_size": bucket_size,
    }


def get_vpvr_signals(vpvr: dict, cur_price: float):
    poc  = vpvr["poc"]
    vah  = vpvr["vah"]
    val  = vpvr["val"]
    hvns = sorted(vpvr["hvn_list"], key=lambda x: x["price"])
    lvns = sorted(vpvr["lvn_list"], key=lambda x: x["price"])

    # Nearest HVN above and below current price
    hvn_above = [h for h in hvns if h["price"] > cur_price]
    hvn_below = [h for h in hvns if h["price"] < cur_price]
    nearest_hvn_above = hvn_above[0]["price"]  if hvn_above else vah
    nearest_hvn_below = hvn_below[-1]["price"] if hvn_below else val

    # Nearest LVN above and below
    lvn_above = [l for l in lvns if l["price"] > cur_price]
    lvn_below = [l for l in lvns if l["price"] < cur_price]
    nearest_lvn_above = lvn_above[0]["price"]  if lvn_above else (cur_price + (vah-cur_price)*0.5)
    nearest_lvn_below = lvn_below[-1]["price"] if lvn_below else (cur_price - (cur_price-val)*0.5)

    above_poc = cur_price >= poc

    # BUY signal
    if above_poc:
        buy_entry   = round(poc * 1.001, 0)
        buy_reason  = "Retest POC dari atas — zona keseimbangan volume tertinggi"
        buy_reason_awam = "Harga kembali ke titik di mana paling banyak transaksi pernah terjadi — zona beli favorit para pelaku besar."
    else:
        buy_entry   = round(val * 1.001, 0)
        buy_reason  = "Harga menyentuh VAL — batas bawah Value Area dengan volume tinggi"
        buy_reason_awam = "Harga sudah turun ke area batas bawah zona 'harga wajar' pasar — historis ini sering menjadi titik balik naik."

    buy_tp1 = round(vah, 0)
    buy_tp2 = round(nearest_hvn_above if nearest_hvn_above > vah else vah * 1.02, 0)
    buy_sl  = round(nearest_hvn_below if nearest_hvn_below < buy_entry else val * 0.99, 0)
    buy_risk   = buy_entry - buy_sl
    buy_rr_tp1 = round((buy_tp1 - buy_entry) / buy_risk, 2) if buy_risk > 0 else 0

    # SELL signal
    sell_entry  = round(vah * 0.999, 0)
    sell_reason = "Harga mencapai VAH — batas atas Value Area, resistance volume tinggi"
    sell_reason_awam = "Harga menyentuh batas atas zona 'harga wajar' pasar — di sinilah banyak penjual menunggu, dan harga sering berbalik turun."
    sell_tp1 = round(poc, 0)
    sell_tp2 = round(val, 0)
    sell_sl  = round(nearest_hvn_above if nearest_hvn_above > vah else vah * 1.02, 0)
    sell_risk   = sell_sl - sell_entry
    sell_rr_tp1 = round((sell_entry - sell_tp1) / sell_risk, 2) if sell_risk > 0 else 0

    # Price position narrative
    if cur_price > vah:
        pos_tech  = f"Harga berada DI ATAS Value Area (>{fmt_price(vah)}). Ini adalah zona breakout — pergerakan di atas VAH sering berlanjut cepat karena volume tipis, namun juga berisiko reversal tajam kembali ke dalam Value Area."
        pos_awam  = f"Harga sudah keluar dari zona 'harga wajar' ke atas. Bayangkan balon yang melayang terlalu tinggi — bisa terus naik, tapi bisa juga tiba-tiba turun kembali. Hati-hati membeli di sini."
    elif cur_price < val:
        pos_tech  = f"Harga berada DI BAWAH Value Area (<{fmt_price(val)}). Zona ini bisa menjadi peluang beli agresif jika ada konfirmasi pembalikan, namun juga bisa berlanjut turun jika support VAL gagal."
        pos_awam  = f"Harga sudah jatuh di bawah zona 'harga wajar'. Ini bisa jadi kesempatan beli yang baik — seperti diskon besar — tapi pastikan ada tanda-tanda harga berhenti turun dulu sebelum masuk."
    elif cur_price >= poc:
        pos_tech  = f"Harga berada ANTARA POC ({fmt_price(poc)}) dan VAH ({fmt_price(vah)}). Bias bullish — harga di atas pusat gravitasi volume. Resistance berikutnya adalah VAH."
        pos_awam  = f"Harga sedang berada di zona sehat di atas titik keseimbangan pasar. Seperti bola yang menggelinding ke atas — momentum masih mendukung kenaikan, tapi VAH di {fmt_price(vah)} adalah tembok berikutnya."
    else:
        pos_tech  = f"Harga berada ANTARA VAL ({fmt_price(val)}) dan POC ({fmt_price(poc)}). Pasar dalam fase akumulasi. POC menjadi resistance terdekat yang harus ditembus untuk konfirmasi bullish."
        pos_awam  = f"Harga berada di zona bawah area 'harga wajar', belum sampai ke titik keseimbangan utama. Pasar masih ragu-ragu. Tunggu harga berhasil menembus {fmt_price(poc)} sebelum mengambil posisi beli."

    return {
        "buy_entry": buy_entry, "buy_tp1": buy_tp1, "buy_tp2": buy_tp2,
        "buy_sl": buy_sl, "buy_rr": buy_rr_tp1,
        "buy_reason": buy_reason, "buy_reason_awam": buy_reason_awam,
        "sell_entry": sell_entry, "sell_tp1": sell_tp1, "sell_tp2": sell_tp2,
        "sell_sl": sell_sl, "sell_rr": sell_rr_tp1,
        "sell_reason": sell_reason, "sell_reason_awam": sell_reason_awam,
        "pos_tech": pos_tech, "pos_awam": pos_awam,
        "above_poc": above_poc,
    }


# ── INDICATORS ────────────────────────────────────────────────────────────────

def calc_ema(series: pd.Series, period: int) -> pd.Series:
    return series.ewm(span=period, adjust=False).mean()


def calc_rsi(series: pd.Series, period: int = 14) -> pd.Series:
    delta = series.diff()
    gain = delta.clip(lower=0).rolling(period).mean()
    loss = -delta.clip(upper=0).rolling(period).mean()
    rs = gain / loss.replace(0, np.nan)
    return 100 - (100 / (1 + rs))


def calc_stoch_rsi(series: pd.Series, rsi_period=14, stoch_period=14, k_period=3, d_period=3):
    rsi = calc_rsi(series, rsi_period)
    rsi_min = rsi.rolling(stoch_period).min()
    rsi_max = rsi.rolling(stoch_period).max()
    stoch = 100 * (rsi - rsi_min) / (rsi_max - rsi_min).replace(0, np.nan)
    k = stoch.rolling(k_period).mean()
    d = k.rolling(d_period).mean()
    return k, d


def calc_macd(series: pd.Series):
    e12 = calc_ema(series, 12)
    e26 = calc_ema(series, 26)
    macd_line = e12 - e26
    signal = calc_ema(macd_line, 9)
    hist = macd_line - signal
    return macd_line, signal, hist


def calc_bb(series: pd.Series, period: int = 20):
    mid = series.rolling(period).mean()
    std = series.rolling(period).std()
    return mid + 2 * std, mid, mid - 2 * std


def calc_adx(df: pd.DataFrame, period: int = 14):
    high = df["high"]
    low  = df["low"]
    close = df["close"]
    tr = pd.concat([
        high - low,
        (high - close.shift()).abs(),
        (low  - close.shift()).abs()
    ], axis=1).max(axis=1)
    dm_plus  = ((high - high.shift()) > (low.shift() - low)).astype(float) * (high - high.shift()).clip(lower=0)
    dm_minus = ((low.shift() - low) > (high - high.shift())).astype(float) * (low.shift() - low).clip(lower=0)
    atr_s    = tr.ewm(alpha=1/period, adjust=False).mean()
    di_plus  = 100 * dm_plus.ewm(alpha=1/period, adjust=False).mean() / atr_s.replace(0, np.nan)
    di_minus = 100 * dm_minus.ewm(alpha=1/period, adjust=False).mean() / atr_s.replace(0, np.nan)
    dx = 100 * (di_plus - di_minus).abs() / (di_plus + di_minus).replace(0, np.nan)
    adx = dx.ewm(alpha=1/period, adjust=False).mean()
    return adx, di_plus, di_minus


def calc_atr(df: pd.DataFrame, period: int = 14) -> pd.Series:
    high, low, close = df["high"], df["low"], df["close"]
    tr = pd.concat([
        high - low,
        (high - close.shift()).abs(),
        (low  - close.shift()).abs()
    ], axis=1).max(axis=1)
    return tr.rolling(period).mean()


def calc_obv(df: pd.DataFrame) -> pd.Series:
    direction = np.sign(df["close"].diff()).fillna(0)
    return (direction * df.get("volume", pd.Series(np.ones(len(df)), index=df.index))).cumsum()


def calc_heikin_ashi(df: pd.DataFrame) -> pd.DataFrame:
    ha = df.copy()
    ha["ha_close"] = (df["open"] + df["high"] + df["low"] + df["close"]) / 4
    ha_open = [(df["open"].iloc[0] + df["close"].iloc[0]) / 2]
    for i in range(1, len(df)):
        ha_open.append((ha_open[i-1] + ha["ha_close"].iloc[i-1]) / 2)
    ha["ha_open"]  = ha_open
    ha["ha_high"]  = pd.concat([df["high"], ha["ha_open"], ha["ha_close"]], axis=1).max(axis=1)
    ha["ha_low"]   = pd.concat([df["low"],  ha["ha_open"], ha["ha_close"]], axis=1).min(axis=1)
    return ha


def calc_sr_channels(df: pd.DataFrame):
    highs  = df["high"].values
    lows   = df["low"].values
    closes = df["close"].values
    n      = len(highs)

    # Dynamic channel width: 1.5x ATR (last 14 bars)
    tr_vals = [max(highs[i]-lows[i],
                   abs(highs[i]-closes[i-1]),
                   abs(lows[i]-closes[i-1]))
               for i in range(max(1,n-14), n)]
    atr14   = np.mean(tr_vals) if tr_vals else closes[-1] * 0.01
    cwidth  = atr14 * 1.5

    prd = max(3, n // 15)
    pivots = []
    for i in range(prd, n - prd):
        if highs[i] >= np.max(highs[i-prd:i+prd+1]):
            pivots.append({"val": highs[i], "idx": i, "type": "high"})
        if lows[i]  <= np.min(lows[i-prd:i+prd+1]):
            pivots.append({"val": lows[i],  "idx": i, "type": "low"})

    channels, used = [], set()
    for i, p in enumerate(pivots):
        if i in used: continue
        lo = hi = p["val"]; count = 1; members = [i]
        for j, q in enumerate(pivots):
            if j == i or j in used: continue
            w = hi - q["val"] if q["val"] <= hi else q["val"] - lo
            if w <= cwidth:
                lo = min(lo, q["val"]); hi = max(hi, q["val"])
                count += 1; members.append(j); used.add(j)

        # Touch count: bars where high/low graze the zone
        touch = sum(1 for k in range(max(0, n-150), n)
                    if (highs[k] <= hi and highs[k] >= lo) or
                       (lows[k]  <= hi and lows[k]  >= lo))
        # Pivot count weighted + touch count
        strength = count * 10 + touch
        channels.append({"hi": hi, "lo": lo, "strength": strength,
                         "pivot_count": count, "touch_count": touch,
                         "width": hi - lo})
        for m in members: used.add(m)

    channels.sort(key=lambda x: -x["strength"])
    # Deduplicate overlapping channels
    final = []
    for ch in channels:
        overlap = any(
            ch["lo"] < ex["hi"] and ch["hi"] > ex["lo"]
            for ex in final
        )
        if not overlap:
            final.append(ch)
        if len(final) >= 8:
            break
    return final


def calc_fibonacci(df: pd.DataFrame, lookback: int = 60):
    sl = df.tail(min(lookback, len(df)))
    swing_h, swing_l = sl["high"].max(), sl["low"].min()
    diff   = swing_h - swing_l
    ratios = [0, 0.236, 0.382, 0.5, 0.618, 0.786, 1.0]
    colors = ["#e24b4a","#d85a30","#ef9f27","#639922","#185fa5","#534ab7","#3b6d11"]
    return [{"ratio": r, "price": swing_h - diff*r, "label": f"{r*100:.1f}%", "color": colors[i]}
            for i, r in enumerate(ratios)]


def get_signals(df, rsi, stoch_k, stoch_d, macd_hist, ema20, ema50, adx_val, di_plus, di_minus, atr_series, sr_channels):
    price     = df["close"].iloc[-1]
    rsi_val   = rsi.iloc[-1]   if not pd.isna(rsi.iloc[-1])   else 50
    hist_val  = macd_hist.iloc[-1] if not pd.isna(macd_hist.iloc[-1]) else 0
    prev_hist = macd_hist.iloc[-2] if len(macd_hist) > 1 else 0
    sk        = stoch_k.iloc[-1] if not pd.isna(stoch_k.iloc[-1]) else 50
    sd        = stoch_d.iloc[-1] if not pd.isna(stoch_d.iloc[-1]) else 50
    adx       = adx_val.iloc[-1] if not pd.isna(adx_val.iloc[-1]) else 20
    dip       = di_plus.iloc[-1] if not pd.isna(di_plus.iloc[-1]) else 20
    dim       = di_minus.iloc[-1] if not pd.isna(di_minus.iloc[-1]) else 20
    atr       = atr_series.iloc[-1] if not pd.isna(atr_series.iloc[-1]) else price * 0.01
    e20, e50  = ema20.iloc[-1], ema50.iloc[-1]

    buy_score = sell_score = 0
    buy_r, sell_r = [], []

    # RSI
    if rsi_val < 35:   buy_score += 2; buy_r.append("RSI oversold")
    elif rsi_val < 45: buy_score += 1; buy_r.append("RSI low")
    if rsi_val > 65:   sell_score += 2; sell_r.append("RSI overbought")
    elif rsi_val > 55: sell_score += 1; sell_r.append("RSI high")

    # Stoch RSI
    if sk < 20 and sk > sd:   buy_score += 2; buy_r.append("StochRSI cross up")
    elif sk < 30:              buy_score += 1; buy_r.append("StochRSI oversold")
    if sk > 80 and sk < sd:   sell_score += 2; sell_r.append("StochRSI cross down")
    elif sk > 70:              sell_score += 1; sell_r.append("StochRSI overbought")

    # MACD
    if hist_val > 0 and prev_hist <= 0:   buy_score += 2; buy_r.append("MACD cross up")
    elif hist_val > 0:                     buy_score += 1
    if hist_val < 0 and prev_hist >= 0:   sell_score += 2; sell_r.append("MACD cross down")
    elif hist_val < 0:                     sell_score += 1

    # EMA
    if e20 > e50:  buy_score += 1; buy_r.append("EMA bullish")
    else:          sell_score += 1; sell_r.append("EMA bearish")

    # ADX
    if adx > 25:
        if dip > dim:  buy_score += 2; buy_r.append(f"ADX trend({adx:.0f})")
        else:          sell_score += 2; sell_r.append(f"ADX trend({adx:.0f})")

    # S/R
    for ch in sr_channels:
        if abs(price - ch["lo"]) / price < 0.008:
            buy_score += 2; buy_r.append("At support"); break
        if abs(price - ch["hi"]) / price < 0.008:
            sell_score += 2; sell_r.append("At resistance"); break

    dp = 2 if price < 100 else 0

    # ── R/R 2:1 profesional ─────────────────────────────────────────────────
    # SL = 1 ATR dari entry → TP1 = 2 ATR (2:1) → TP2 = 4 ATR (4:1)
    # TP3 = resistance/support terdekat dari S/R channels (dinamis)
    buy_entry = round(price * 0.999, dp)
    buy_sl    = round(buy_entry - atr * 1.0, dp)          # risiko 1 ATR
    buy_tp1   = round(buy_entry + atr * 2.0, dp)          # R/R 2:1
    buy_tp2   = round(buy_entry + atr * 4.0, dp)          # R/R 4:1
    # TP3: resistance terdekat di atas TP2, fallback ke ATR * 6
    res_above = [ch["lo"] for ch in sr_channels
                 if ch["lo"] > buy_tp2 and ch["lo"] > buy_entry]
    buy_tp3   = round(min(res_above), dp) if res_above else round(buy_entry + atr * 6.0, dp)
    buy_risk  = buy_entry - buy_sl
    buy_rr    = 2.0   # by design: TP1 = 2×ATR, SL = 1×ATR → always 2:1

    sell_entry = round(price * 1.001, dp)
    sell_sl    = round(sell_entry + atr * 1.0, dp)        # risiko 1 ATR
    sell_tp1   = round(sell_entry - atr * 2.0, dp)        # R/R 2:1
    sell_tp2   = round(sell_entry - atr * 4.0, dp)        # R/R 4:1
    # TP3: support terdekat di bawah TP2, fallback ke ATR * 6
    sup_below  = [ch["hi"] for ch in sr_channels
                  if ch["hi"] < sell_tp2 and ch["hi"] < sell_entry]
    sell_tp3   = round(max(sup_below), dp) if sup_below else round(sell_entry - atr * 6.0, dp)
    sell_risk  = sell_sl - sell_entry
    sell_rr    = 2.0   # by design: TP1 = 2×ATR, SL = 1×ATR → always 2:1

    buy_pct  = lambda p: f"{(p - buy_entry)  / buy_entry  * 100:+.2f}%"
    sell_pct = lambda p: f"{(p - sell_entry) / sell_entry * 100:+.2f}%"

    MAX_SCORE = 12
    bs = "STRONG" if buy_score >= 6 else "MODERATE" if buy_score >= 3 else "WEAK"
    ss = "STRONG" if sell_score >= 6 else "MODERATE" if sell_score >= 3 else "WEAK"

    all_indicators = [
        ("RSI oversold",       rsi_val < 35,   2),
        ("RSI low",            35 <= rsi_val < 45, 1),
        ("StochRSI cross up",  sk < 20 and sk > sd, 2),
        ("StochRSI oversold",  20 <= sk < 30,  1),
        ("MACD cross up",      hist_val > 0 and prev_hist <= 0, 2),
        ("MACD positif",       hist_val > 0 and not (hist_val > 0 and prev_hist <= 0), 1),
        ("EMA bullish",        e20 > e50,       1),
        ("ADX trend bullish",  adx > 25 and dip > dim, 2),
        ("At support",         any(abs(price - ch["lo"]) / price < 0.008 for ch in sr_channels), 2),
    ]
    sell_indicators = [
        ("RSI overbought",     rsi_val > 65,   2),
        ("RSI high",           55 < rsi_val <= 65, 1),
        ("StochRSI cross down",sk > 80 and sk < sd, 2),
        ("StochRSI overbought",70 <= sk <= 80, 1),
        ("MACD cross down",    hist_val < 0 and prev_hist >= 0, 2),
        ("MACD negatif",       hist_val < 0 and not (hist_val < 0 and prev_hist >= 0), 1),
        ("EMA bearish",        e20 <= e50,      1),
        ("ADX trend bearish",  adx > 25 and dim > dip, 2),
        ("At resistance",      any(abs(price - ch["hi"]) / price < 0.008 for ch in sr_channels), 2),
    ]

    # Recommendation text
    if bs == "STRONG":
        buy_action = f"Pasang limit buy di {fmt_price(buy_entry)}"
        buy_advice = "Sinyal kuat — entry layak dieksekusi"
    elif bs == "MODERATE":
        buy_action = f"Pertimbangkan limit buy di {fmt_price(buy_entry)}"
        buy_advice = "Konfirmasi tambahan disarankan sebelum entry"
    else:
        buy_action = "Tahan — sinyal lemah"
        buy_advice = "Tunggu lebih banyak indikator sepakat"

    if ss == "STRONG":
        sell_action = f"Pasang limit sell di {fmt_price(sell_entry)}"
        sell_advice = "Sinyal jual kuat — exit atau short layak"
    elif ss == "MODERATE":
        sell_action = "Hati-hati — tren utama mungkin masih bullish"
        sell_advice = "Skip atau kurangi ukuran posisi"
    else:
        sell_action = "Abaikan sinyal jual"
        sell_advice = "Tidak ada konfirmasi yang cukup"

    return {
        "price": price, "rsi": rsi_val, "hist": hist_val, "stoch_k": sk, "stoch_d": sd,
        "e20": e20, "e50": e50, "adx": adx, "dip": dip, "dim": dim, "atr": atr,
        "buy_score": buy_score, "sell_score": sell_score, "max_score": MAX_SCORE,
        "buy_strength": bs, "sell_strength": ss,
        "buy_reason":  " + ".join(buy_r)  or "Mixed signals",
        "sell_reason": " + ".join(sell_r) or "Mixed signals",
        "buy_entry": buy_entry, "buy_tp1": buy_tp1, "buy_tp2": buy_tp2, "buy_tp3": buy_tp3,
        "buy_sl": buy_sl, "buy_rr": buy_rr,
        "buy_tp1_pct": buy_pct(buy_tp1), "buy_tp2_pct": buy_pct(buy_tp2),
        "buy_tp3_pct": buy_pct(buy_tp3),
        "buy_sl_pct":  f"{(buy_sl - buy_entry) / buy_entry * 100:+.2f}%",
        "buy_entry_pct": f"{(buy_entry - price) / price * 100:+.2f}%",
        "sell_entry": sell_entry, "sell_tp1": sell_tp1, "sell_tp2": sell_tp2, "sell_tp3": sell_tp3,
        "sell_sl": sell_sl, "sell_rr": sell_rr,
        "sell_tp1_pct": sell_pct(sell_tp1), "sell_tp2_pct": sell_pct(sell_tp2),
        "sell_tp3_pct": sell_pct(sell_tp3),
        "sell_sl_pct":  f"{(sell_sl - sell_entry) / sell_entry * 100:+.2f}%",
        "sell_entry_pct": f"{(sell_entry - price) / price * 100:+.2f}%",
        "all_indicators": all_indicators,
        "sell_indicators": sell_indicators,
        "buy_action": buy_action, "buy_advice": buy_advice,
        "sell_action": sell_action, "sell_advice": sell_advice,
    }


# ── CHARTS ────────────────────────────────────────────────────────────────────

def build_main_chart(df, ha, ema20, ema50, sr_channels, fib_levels,
                     rsi, stoch_k, stoch_d, macd_hist, adx_val, di_plus, di_minus,
                     obv, atr_series, show_ha, show_adx, show_obv, show_stochrsi):
    n_rows   = 4 + (1 if show_adx else 0) + (1 if show_obv else 0)
    heights  = [0.40, 0.15, 0.15, 0.15]
    subtitles = ["Price + S/R + Fibonacci", "RSI (14) & Stoch RSI", "MACD (12,26,9)", "ATR (14)"]
    if show_adx:
        heights.append(0.15); subtitles.append("ADX (14)")
    if show_obv:
        heights.append(0.15); subtitles.append("OBV")

    total = sum(heights)
    heights = [h / total for h in heights]

    fig = make_subplots(
        rows=n_rows, cols=1,
        shared_xaxes=True,
        row_heights=heights,
        vertical_spacing=0.025,
        subplot_titles=subtitles
    )

    price = df["close"].iloc[-1]

    # Fibonacci
    for fib in fib_levels:
        fig.add_hline(y=fib["price"], line_color=fib["color"], line_dash="dot", line_width=0.8,
                      annotation_text=f"Fib {fib['label']} ${fib['price']:,.2f}",
                      annotation_position="right", annotation_font_size=9,
                      annotation_font_color=fib["color"], row=1, col=1)

    # S/R channels
    for i, ch in enumerate(sr_channels[:6]):
        is_res = ch["hi"] > price and ch["lo"] > price
        is_sup = ch["hi"] < price
        color  = "rgba(163,45,45,0.3)" if is_res else "rgba(59,109,17,0.3)" if is_sup else "rgba(136,135,128,0.25)"
        label  = "R" if is_res else "S" if is_sup else "IN"
        fig.add_hrect(y0=ch["lo"], y1=ch["hi"], fillcolor=color,
                      line_color=color.replace("0.3","0.6").replace("0.25","0.5"), line_width=0.8,
                      annotation_text=f"{label}{i+1}", annotation_position="right",
                      annotation_font_size=8, row=1, col=1)

    # Candles: default OHLC candlestick, switch to Heikin-Ashi if selected
    if show_ha:
        fig.add_trace(go.Candlestick(
            x=ha["time"], open=ha["ha_open"], high=ha["ha_high"],
            low=ha["ha_low"], close=ha["ha_close"],
            name="Heikin-Ashi",
            increasing_line_color="#3b6d11", increasing_fillcolor="rgba(59,109,17,0.75)",
            decreasing_line_color="#a32d2d", decreasing_fillcolor="rgba(163,45,45,0.75)",
        ), row=1, col=1)
    else:
        fig.add_trace(go.Candlestick(
            x=df["time"], open=df["open"], high=df["high"],
            low=df["low"], close=df["close"],
            name="OHLC",
            increasing_line_color="#3b6d11", increasing_fillcolor="rgba(59,109,17,0.75)",
            decreasing_line_color="#a32d2d", decreasing_fillcolor="rgba(163,45,45,0.75)",
        ), row=1, col=1)

    fig.add_trace(go.Scatter(x=df["time"], y=ema20, name="EMA 20",
                             line=dict(color="#ef9f27", width=1.2)), row=1, col=1)
    fig.add_trace(go.Scatter(x=df["time"], y=ema50, name="EMA 50",
                             line=dict(color="#d85a30", width=1, dash="dash")), row=1, col=1)

    buy_mask  = (rsi < 38) | ((macd_hist > 0) & (macd_hist.shift(1) <= 0)) | ((stoch_k < 20) & (stoch_k > stoch_d))
    sell_mask = (rsi > 62) | ((macd_hist < 0) & (macd_hist.shift(1) >= 0)) | ((stoch_k > 80) & (stoch_k < stoch_d))
    # Place triangles below candle low / above candle high for clarity
    buy_y  = df["low"][buy_mask]  * 0.9985
    sell_y = df["high"][sell_mask] * 1.0015
    fig.add_trace(go.Scatter(x=df["time"][buy_mask], y=buy_y, mode="markers",
                             name="Buy", marker=dict(symbol="triangle-up", size=10, color="#3b6d11")), row=1, col=1)
    fig.add_trace(go.Scatter(x=df["time"][sell_mask], y=sell_y, mode="markers",
                             name="Sell", marker=dict(symbol="triangle-down", size=10, color="#a32d2d")), row=1, col=1)

    # Row 2: RSI + StochRSI
    fig.add_trace(go.Scatter(x=df["time"], y=rsi, name="RSI",
                             line=dict(color="#534ab7", width=1.5),
                             hovertemplate="RSI: %{y:.1f}<extra></extra>"), row=2, col=1)
    if show_stochrsi:
        fig.add_trace(go.Scatter(x=df["time"], y=stoch_k, name="StochRSI %K",
                                 line=dict(color="#185fa5", width=1.2, dash="dot")), row=2, col=1)
        fig.add_trace(go.Scatter(x=df["time"], y=stoch_d, name="StochRSI %D",
                                 line=dict(color="#ef9f27", width=1.2, dash="dot")), row=2, col=1)
    fig.add_hline(y=70, line_color="rgba(163,45,45,0.5)", line_dash="dot", line_width=1, row=2, col=1)
    fig.add_hline(y=30, line_color="rgba(59,109,17,0.5)", line_dash="dot", line_width=1, row=2, col=1)
    fig.add_hrect(y0=70, y1=100, fillcolor="rgba(163,45,45,0.05)", line_width=0, row=2, col=1)
    fig.add_hrect(y0=0,  y1=30,  fillcolor="rgba(59,109,17,0.05)",  line_width=0, row=2, col=1)

    # Row 3: MACD
    macd_line, signal_line, _ = calc_macd(df["close"])
    fig.add_trace(go.Bar(x=df["time"], y=macd_hist, name="MACD Hist",
                         marker_color=["rgba(59,109,17,0.7)" if v >= 0 else "rgba(163,45,45,0.7)"
                                       for v in macd_hist.fillna(0)]), row=3, col=1)
    fig.add_trace(go.Scatter(x=df["time"], y=macd_line,  name="MACD",   line=dict(color="#185fa5", width=1)), row=3, col=1)
    fig.add_trace(go.Scatter(x=df["time"], y=signal_line,name="Signal", line=dict(color="#ef9f27", width=1, dash="dot")), row=3, col=1)

    # Row 4: ATR
    fig.add_trace(go.Scatter(x=df["time"], y=atr_series, name="ATR",
                             line=dict(color="#534ab7", width=1.2), fill="tozeroy",
                             fillcolor="rgba(83,74,183,0.08)",
                             hovertemplate="ATR: $%{y:,.4f}<extra></extra>"), row=4, col=1)

    # Row 5+: ADX
    if show_adx:
        row_adx = 5
        fig.add_trace(go.Scatter(x=df["time"], y=adx_val, name="ADX",
                                 line=dict(color="#1d9e75", width=1.8)), row=row_adx, col=1)
        fig.add_trace(go.Scatter(x=df["time"], y=di_plus, name="+DI",
                                 line=dict(color="#3b6d11", width=1, dash="dot")), row=row_adx, col=1)
        fig.add_trace(go.Scatter(x=df["time"], y=di_minus, name="-DI",
                                 line=dict(color="#a32d2d", width=1, dash="dot")), row=row_adx, col=1)
        fig.add_hline(y=25, line_color="rgba(136,135,128,0.6)", line_dash="dash", line_width=1, row=row_adx, col=1)

    # Row OBV
    if show_obv:
        row_obv = (6 if show_adx else 5)
        obv_color = ["rgba(59,109,17,0.65)" if obv.iloc[i] >= obv.iloc[i-1] else "rgba(163,45,45,0.65)"
                     for i in range(len(obv))]
        fig.add_trace(go.Bar(x=df["time"], y=obv, name="OBV",
                             marker_color=obv_color), row=row_obv, col=1)

    fig.update_layout(
        height=820,
        margin=dict(l=10, r=130, t=30, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(248,249,250,0.5)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02,
                    xanchor="left", x=0, font=dict(size=10)),
        hovermode="x unified",
        xaxis_rangeslider_visible=False,
    )
    fig.update_yaxes(gridcolor="rgba(128,128,128,0.1)", tickfont=dict(size=10))
    fig.update_xaxes(gridcolor="rgba(128,128,128,0.1)", tickfont=dict(size=10))
    fig.update_yaxes(range=[0, 100], row=2, col=1)
    return fig


def build_sr_chart(sr_channels, price):
    top = sr_channels[:6]
    labels, strengths, colors = [], [], []
    for i, ch in enumerate(top):
        is_res = ch["hi"] > price and ch["lo"] > price
        is_sup = ch["hi"] < price
        t = "R" if is_res else "S" if is_sup else "IN"
        mid = (ch["hi"] + ch["lo"]) / 2
        labels.append(f"{t}{i+1}  ${mid:,.2f}")
        strengths.append(ch["strength"])
        colors.append("rgba(163,45,45,0.75)" if is_res else
                       "rgba(59,109,17,0.75)"  if is_sup else "rgba(136,135,128,0.65)")
    fig = go.Figure(go.Bar(
        x=strengths, y=labels, orientation="h",
        marker_color=colors,
        text=[f"  {s}" for s in strengths], textposition="outside", textfont=dict(size=10),
    ))
    fig.update_layout(height=220, margin=dict(l=10, r=40, t=10, b=10),
                      paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(248,249,250,0.5)",
                      xaxis=dict(title="Strength", tickfont=dict(size=10), gridcolor="rgba(128,128,128,0.1)"),
                      yaxis=dict(tickfont=dict(size=10)))
    return fig


def build_fg_gauge(value: int):
    if value <= 24:   color, label = "#a32d2d", "Extreme Fear"
    elif value <= 44: color, label = "#d85a30", "Fear"
    elif value <= 55: color, label = "#888780", "Neutral"
    elif value <= 74: color, label = "#639922", "Greed"
    else:             color, label = "#3b6d11", "Extreme Greed"
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        number={"font": {"size": 36, "color": color}},
        gauge={
            "axis": {"range": [0, 100], "tickwidth": 1, "tickfont": {"size": 10}},
            "bar": {"color": color, "thickness": 0.25},
            "bgcolor": "rgba(248,249,250,0.5)",
            "steps": [
                {"range": [0,  25], "color": "rgba(163,45,45,0.15)"},
                {"range": [25, 45], "color": "rgba(215,90,48,0.15)"},
                {"range": [45, 55], "color": "rgba(136,135,128,0.15)"},
                {"range": [55, 75], "color": "rgba(99,153,34,0.15)"},
                {"range": [75,100], "color": "rgba(59,109,17,0.15)"},
            ],
            "threshold": {"line": {"color": color, "width": 3}, "thickness": 0.8, "value": value}
        },
        title={"text": f"<b>{label}</b>", "font": {"size": 13, "color": color}}
    ))
    fig.update_layout(height=200, margin=dict(l=20, r=20, t=30, b=10),
                      paper_bgcolor="rgba(0,0,0,0)")
    return fig


def build_fg_history(fg_data):
    if not fg_data:
        return None
    vals  = [int(d["value"]) for d in reversed(fg_data[:14])]
    dates = [datetime.fromtimestamp(int(d["timestamp"])).strftime("%d %b") for d in reversed(fg_data[:14])]
    bar_colors = []
    for v in vals:
        if v <= 24:   bar_colors.append("#a32d2d")
        elif v <= 44: bar_colors.append("#d85a30")
        elif v <= 55: bar_colors.append("#888780")
        elif v <= 74: bar_colors.append("#639922")
        else:         bar_colors.append("#3b6d11")
    fig = go.Figure(go.Bar(x=dates, y=vals, marker_color=bar_colors,
                           text=vals, textposition="outside", textfont=dict(size=9)))
    fig.update_layout(height=180, margin=dict(l=10, r=10, t=10, b=30),
                      paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(248,249,250,0.5)",
                      yaxis=dict(range=[0, 110], tickfont=dict(size=9), gridcolor="rgba(128,128,128,0.1)"),
                      xaxis=dict(tickfont=dict(size=9)))
    return fig


def run_monte_carlo(closes: pd.Series, n_sim: int = 600, max_days: int = 365):
    log_ret = np.log(closes / closes.shift(1)).dropna()
    mu      = log_ret.mean()
    sigma   = log_ret.std()
    last    = closes.iloc[-1]
    np.random.seed(42)
    sims = np.zeros((max_days, n_sim))
    for s in range(n_sim):
        price = last
        for d in range(max_days):
            shock  = np.random.normal(mu, sigma)
            price  = price * np.exp(shock)
            sims[d, s] = price
    return sims, last


def build_monte_carlo_chart(closes: pd.Series, coin_lbl: str):
    n_sim, max_days = 600, 365
    sims, last = run_monte_carlo(closes, n_sim, max_days)
    days_range = np.arange(1, max_days + 1)

    p10  = np.percentile(sims, 10, axis=1)
    p25  = np.percentile(sims, 25, axis=1)
    p50  = np.percentile(sims, 50, axis=1)
    p75  = np.percentile(sims, 75, axis=1)
    p90  = np.percentile(sims, 90, axis=1)

    fig = go.Figure()

    # Cone bands
    fig.add_trace(go.Scatter(
        x=np.concatenate([days_range, days_range[::-1]]),
        y=np.concatenate([p90, p10[::-1]]),
        fill="toself", fillcolor="rgba(83,74,183,0.08)",
        line=dict(color="rgba(0,0,0,0)"), name="P10–P90 (80%)",
        hoverinfo="skip"
    ))
    fig.add_trace(go.Scatter(
        x=np.concatenate([days_range, days_range[::-1]]),
        y=np.concatenate([p75, p25[::-1]]),
        fill="toself", fillcolor="rgba(83,74,183,0.15)",
        line=dict(color="rgba(0,0,0,0)"), name="P25–P75 (50%)",
        hoverinfo="skip"
    ))

    # Percentile lines
    fig.add_trace(go.Scatter(x=days_range, y=p90, name="P90 (optimis)",
                             line=dict(color="#3b6d11", width=1, dash="dot"),
                             hovertemplate="Hari %{x}<br>P90: $%{y:,.2f}<extra></extra>"))
    fig.add_trace(go.Scatter(x=days_range, y=p75, name="P75",
                             line=dict(color="#639922", width=1, dash="dot"),
                             hovertemplate="Hari %{x}<br>P75: $%{y:,.2f}<extra></extra>"))
    fig.add_trace(go.Scatter(x=days_range, y=p50, name="Median (P50)",
                             line=dict(color="#534ab7", width=2),
                             hovertemplate="Hari %{x}<br>Median: $%{y:,.2f}<extra></extra>"))
    fig.add_trace(go.Scatter(x=days_range, y=p25, name="P25",
                             line=dict(color="#d85a30", width=1, dash="dot"),
                             hovertemplate="Hari %{x}<br>P25: $%{y:,.2f}<extra></extra>"))
    fig.add_trace(go.Scatter(x=days_range, y=p10, name="P10 (pesimis)",
                             line=dict(color="#a32d2d", width=1, dash="dot"),
                             hovertemplate="Hari %{x}<br>P10: $%{y:,.2f}<extra></extra>"))

    # Vertical markers at key horizons
    for d, lbl in [(3,"3d"), (7,"7d"), (30,"30d"), (90,"90d"), (365,"365d")]:
        fig.add_vline(x=d, line_color="rgba(136,135,128,0.4)", line_dash="dash", line_width=1,
                      annotation_text=lbl, annotation_position="top",
                      annotation_font_size=9, annotation_font_color="#888780")

    # Current price line
    fig.add_hline(y=last, line_color="rgba(136,135,128,0.5)", line_dash="dot", line_width=1,
                  annotation_text=f"Harga kini ${last:,.2f}",
                  annotation_position="right", annotation_font_size=9)

    fig.update_layout(
        height=420,
        margin=dict(l=10, r=80, t=20, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(248,249,250,0.5)",
        legend=dict(orientation="h", yanchor="bottom", y=1.01,
                    xanchor="left", x=0, font=dict(size=10)),
        hovermode="x unified",
        xaxis=dict(title="Hari ke depan", tickfont=dict(size=10),
                   gridcolor="rgba(128,128,128,0.08)"),
        yaxis=dict(tickfont=dict(size=10), gridcolor="rgba(128,128,128,0.08)",
                   tickprefix="$", tickformat=",.0f"),
    )
    return fig, sims, p10, p25, p50, p75, p90


# ── HELPERS ───────────────────────────────────────────────────────────────────

def fmt_price(p):
    if p is None: return "—"
    if p >= 10000: return f"${p:,.0f}"
    if p >= 100:   return f"${p:,.2f}"
    if p >= 1:     return f"${p:.4f}"
    return f"${p:.6f}"

def fmt_large(n):
    if n >= 1e12: return f"${n/1e12:.2f}T"
    if n >= 1e9:  return f"${n/1e9:.2f}B"
    if n >= 1e6:  return f"${n/1e6:.2f}M"
    return f"${n:,.0f}"

def badge(val, good_above=None, bad_above=None):
    if good_above and val > good_above: return "🟢"
    if bad_above  and val > bad_above:  return "🔴"
    return "🟡"


def generate_technical_narrative(coin_lbl, cur_price, pct_24h, sig,
                                  fib_levels, sr_channels,
                                  fg_now=None, mc_prob_7d=None, days_lbl=""):
    coin_name  = coin_lbl.split(" / ")[0]
    price_str  = fmt_price(cur_price)
    pct_str    = f"{pct_24h:+.2f}%"
    rsi        = round(sig["rsi"], 1)
    sk         = round(sig["stoch_k"], 1)
    hist       = sig["hist"]
    e20, e50   = sig["e20"], sig["e50"]
    adx        = round(sig["adx"], 1)
    dip, dim   = sig["dip"], sig["dim"]
    atr        = sig["atr"]
    total      = sig["buy_score"] - sig["sell_score"]

    ema_rel  = "di atas" if e20 > e50 else "di bawah"
    trend_lbl= "bullish" if e20 > e50 else "bearish"

    if adx > 35:   adx_lbl = "sangat kuat"
    elif adx > 25: adx_lbl = "valid dan terukur"
    elif adx > 18: adx_lbl = "sedang terbentuk"
    else:          adx_lbl = "lemah — pasar cenderung sideways"

    adx_bias = "berpihak pada kenaikan" if dip > dim else "mengarah pada tekanan jual"

    if rsi < 35:   rsi_lbl = "berada dalam kondisi oversold"
    elif rsi < 45: rsi_lbl = "berada di area rendah dengan potensi pemulihan"
    elif rsi < 55: rsi_lbl = "berada di zona netral"
    elif rsi < 65: rsi_lbl = "menunjukkan momentum beli yang sehat"
    else:          rsi_lbl = "mendekati zona overbought"

    macd_lbl = ("menunjukkan momentum beli yang menguat" if hist > 0
                else "mengindikasikan tekanan jual yang mendominasi")

    sup_zones = [ch for ch in sr_channels if ch["hi"] < cur_price]
    res_zones = [ch for ch in sr_channels if ch["lo"] > cur_price]
    if sup_zones:
        ns = max(sup_zones, key=lambda x: x["hi"])
        sup_txt = f"${ns['lo']:,.2f}–${ns['hi']:,.2f}"
    else:
        sup_txt = "tidak teridentifikasi dalam periode ini"
    if res_zones:
        nr = min(res_zones, key=lambda x: x["lo"])
        res_txt = f"${nr['lo']:,.2f}–${nr['hi']:,.2f}"
    else:
        res_txt = "tidak teridentifikasi dalam periode ini"

    near_fib = (min(fib_levels, key=lambda f: abs(cur_price - f["price"]))
                if fib_levels else None)
    fib_txt = (f"level {near_fib['label']} di {fmt_price(near_fib['price'])}"
               if near_fib else "area tengah swing")
    fib_dist = (f"{(cur_price - near_fib['price']) / cur_price * 100:+.2f}%"
                if near_fib else "")

    mc_txt = (f"Simulasi Monte Carlo dengan enam ratus iterasi menunjukkan probabilitas "
              f"{mc_prob_7d:.0f}% bahwa harga akan berada lebih tinggi dalam tujuh hari ke depan."
              if mc_prob_7d is not None else "")

    if fg_now is not None:
        if fg_now <= 24:   fg_lbl = f"Extreme Fear ({fg_now}/100), yang secara historis merupakan zona akumulasi bagi investor jangka menengah"
        elif fg_now <= 44: fg_lbl = f"Fear ({fg_now}/100), mengindikasikan ketidakpastian yang masih mendominasi psikologi pasar"
        elif fg_now <= 55: fg_lbl = f"Neutral ({fg_now}/100), pasar dalam fase konsolidasi psikologis"
        elif fg_now <= 74: fg_lbl = f"Greed ({fg_now}/100), sentimen positif yang perlu dipantau agar tidak berlebihan"
        else:              fg_lbl = f"Extreme Greed ({fg_now}/100), zona yang sering mendahului koreksi signifikan"
        fg_txt = f"Fear & Greed Index berada di zona {fg_lbl}."
    else:
        fg_txt = ""

    if total > 3:    concl = "secara keseluruhan condong kuat ke arah beli, dengan mayoritas indikator memberikan konfirmasi yang searah"
    elif total > 0:  concl = "menunjukkan bias beli yang moderat, meskipun belum semua indikator memberikan sinyal yang selaras"
    elif total == 0: concl = "berada dalam keseimbangan antara tekanan beli dan jual, mencerminkan kondisi pasar yang masih konsolidasi"
    elif total > -3: concl = "menunjukkan kecenderungan jual yang perlu diwaspadai sebelum mengambil posisi baru"
    else:            concl = "memberikan sinyal jual yang cukup tegas dari berbagai indikator teknikal secara bersamaan"

    p1 = (f"{coin_name} saat ini diperdagangkan di harga {price_str} dengan perubahan {pct_str} dalam dua puluh empat jam terakhir. "
          f"Dari perspektif analisis tren jangka menengah, EMA dua puluh periode berada {ema_rel} EMA lima puluh periode, "
          f"mempertahankan struktur {trend_lbl} yang terbentuk pada beberapa sesi perdagangan terakhir. "
          f"ADX dengan nilai {adx} menunjukkan kekuatan tren yang {adx_lbl}, di mana arah dominan {adx_bias}.")

    p2 = (f"Dari sisi indikator momentum, RSI-14 {rsi_lbl} di angka {rsi}, "
          f"sementara Stochastic RSI %K berada di {sk} yang memberikan gambaran lebih sensitif tentang kondisi pasar jangka pendek. "
          f"MACD histogram yang bernilai {'positif' if hist > 0 else 'negatif'} saat ini {macd_lbl}. "
          f"Kombinasi ketiga indikator momentum ini {concl}.")

    p3 = (f"Dari sisi struktur harga, zona support terdekat teridentifikasi di kisaran {sup_txt}, "
          f"sementara area resistance pertama yang perlu ditembus berada di {res_txt}. "
          f"Level Fibonacci Retracement menempatkan harga saat ini paling dekat dengan {fib_txt} ({fib_dist} dari harga sekarang), "
          f"sebuah area yang kerap menjadi titik keputusan penting bagi pelaku pasar institusional. "
          f"ATR empat belas periode senilai {fmt_price(round(atr, 2 if cur_price < 100 else 0))} "
          f"mencerminkan volatilitas harian yang perlu diperhitungkan dalam penentuan ukuran posisi dan jarak stop loss.")

    p4 = (f"{mc_txt} {fg_txt} "
          f"Secara keseluruhan, kondisi teknikal {coin_name} pada periode {days_lbl} ini menempatkan pasar dalam posisi yang "
          f"{'menarik untuk dicermati oleh trader aktif dengan manajemen risiko yang ketat' if total >= 0 else 'memerlukan kewaspadaan ekstra dan kesabaran sebelum mengambil posisi baru'}. "
          f"Seperti selalu dalam analisis teknikal, tidak ada sinyal yang sempurna — penempatan stop loss yang disiplin "
          f"di bawah zona support kritis dan pengelolaan ukuran posisi yang proporsional tetap menjadi fondasi utama dalam setiap keputusan trading.")

    return "\n\n".join([p1, p2, p3, p4])


def generate_simple_narrative(coin_lbl, cur_price, pct_24h, sig,
                               sr_channels, fg_now=None, mc_prob_7d=None):
    coin_name  = coin_lbl.split(" / ")[0]
    price_str  = fmt_price(cur_price)
    total      = sig["buy_score"] - sig["sell_score"]
    rsi        = round(sig["rsi"], 1)
    adx        = round(sig["adx"], 1)
    sk         = round(sig["stoch_k"], 1)
    e20, e50   = sig["e20"], sig["e50"]
    atr        = sig["atr"]

    is_bull   = total > 0
    is_strong = abs(total) > 3

    if total > 3:    bias = "BELI"; bias_color = "#27500a"; bias_bg = "#eaf3de"; bar_color = "#3b6d11"
    elif total > 0:  bias = "BELI (hati-hati)"; bias_color = "#27500a"; bias_bg = "#eaf3de"; bar_color = "#639922"
    elif total == 0: bias = "NETRAL / TUNGGU"; bias_color = "#444"; bias_bg = "#f1efe8"; bar_color = "#888"
    elif total > -3: bias = "JUAL / HATI-HATI"; bias_color = "#791f1f"; bias_bg = "#fcebeb"; bar_color = "#d85a30"
    else:            bias = "JUAL"; bias_color = "#791f1f"; bias_bg = "#fcebeb"; bar_color = "#a32d2d"

    conf = min(92, max(35, abs(total) * 9 + 40))
    conf_lbl = "Kuat" if conf >= 70 else "Sedang" if conf >= 50 else "Lemah"

    trend_str = "naik" if e20 > e50 else "turun"
    trend_analogy = (
        "seperti arus sungai yang sedang mengalir ke atas — belum berhenti dan masih memiliki tenaga"
        if is_bull else
        "seperti mobil di turunan — gravitasi sedang bekerja ke bawah dan perlu rem ekstra"
    )

    rsi_txt = ("pasar belum memasuki zona jenuh beli" if rsi < 60
               else "pasar sudah mendekati zona jenuh beli, perlu hati-hati"
               if rsi < 70 else "pasar dalam kondisi jenuh beli yang kuat")

    mc_txt = (f"Proyeksi probabilistik menunjukkan kemungkinan {mc_prob_7d:.0f}% harga akan lebih tinggi dalam tujuh hari ke depan."
              if mc_prob_7d is not None else "")

    fg_txt = ""
    if fg_now is not None:
        if fg_now <= 24:   fg_txt = f"Sentimen pasar saat ini adalah Extreme Fear ({fg_now}/100) — secara historis ini justru sering menjadi peluang beli yang baik."
        elif fg_now <= 44: fg_txt = f"Sentimen pasar masih dalam zona Fear ({fg_now}/100) — banyak investor yang masih ragu dan cemas."
        elif fg_now <= 55: fg_txt = f"Sentimen pasar berada di zona Netral ({fg_now}/100) — pasar sedang mencari arah."
        elif fg_now <= 74: fg_txt = f"Sentimen pasar berada di Greed ({fg_now}/100) — euforia mulai terasa, waspadai potensi koreksi."
        else:              fg_txt = f"Sentimen pasar dalam kondisi Extreme Greed ({fg_now}/100) — ini zona di mana banyak koreksi besar dimulai."

    if is_bull:
        action_main = "Pertimbangkan posisi BELI dengan manajemen risiko ketat"
        action_sub  = "Pasang limit order — jangan gunakan market order. Selalu pasang stop loss sebelum entry."
        summary = (
            f"{coin_name} saat ini menunjukkan tanda-tanda yang {'cukup menarik' if is_strong else 'mulai menarik'} untuk diperhatikan. "
            f"Harga {price_str} berada dalam kondisi {trend_analogy}. "
            f"Secara sederhana, sebagian besar sinyal teknikal saat ini mendukung kenaikan harga lebih lanjut, {rsi_txt}. "
            f"{mc_txt} {fg_txt} "
            f"Meski begitu, ingatlah bahwa tidak ada yang namanya kepastian di pasar kripto — "
            f"selalu siapkan skenario terburuk sebelum masuk posisi."
        )
    elif total == 0:
        action_main = "Tunggu — sinyal belum jelas ke arah manapun"
        action_sub  = "Pasar sedang dalam fase konsolidasi. Tunggu breakout yang dikonfirmasi sebelum entry."
        summary = (
            f"{coin_name} saat ini berada dalam kondisi yang belum memberikan arah yang jelas. "
            f"Harga {price_str} bergerak sideways, {trend_analogy}. "
            f"Indikator teknikal sedang saling bertentangan satu sama lain — sebagian mendukung kenaikan, sebagian lagi mengindikasikan penurunan. "
            f"{fg_txt} Dalam kondisi seperti ini, kesabaran adalah strategi terbaik. "
            f"Tunggu hingga salah satu arah dikonfirmasi oleh lebih banyak indikator sebelum mengambil posisi."
        )
    else:
        action_main = "Tahan / Pertimbangkan Ambil Profit"
        action_sub  = "Jika sudah punya posisi beli, perketat stop loss. Jika belum masuk, tunggu dulu."
        summary = (
            f"{coin_name} saat ini menunjukkan tanda-tanda {'pelemahan yang signifikan' if not is_strong else 'tekanan jual yang perlu diwaspadai'}. "
            f"Harga {price_str} bergerak {trend_analogy}. "
            f"Beberapa indikator teknikal mulai memberikan sinyal kehati-hatian — bayangkan seperti lampu kuning di persimpangan: bukan berarti berhenti total, "
            f"tapi perlambat dan waspada. "
            f"{mc_txt} {fg_txt} "
            f"Jika Anda sudah memiliki posisi beli, ini saat yang tepat untuk memperketat stop loss atau mempertimbangkan ambil sebagian profit."
        )

    sup_zones = [ch for ch in sr_channels if ch["hi"] < cur_price]
    res_zones = [ch for ch in sr_channels if ch["lo"] > cur_price]
    sup_price = fmt_price(max(sup_zones, key=lambda x: x["hi"])["hi"]) if sup_zones else "—"
    res_price = fmt_price(min(res_zones, key=lambda x: x["lo"])["lo"]) if res_zones else "—"

    return {
        "bias": bias, "bias_color": bias_color, "bias_bg": bias_bg,
        "bar_color": bar_color, "is_bull": is_bull,
        "conf": conf, "conf_lbl": conf_lbl,
        "summary": summary, "action_main": action_main, "action_sub": action_sub,
        "rsi": rsi, "adx": adx, "sk": sk,
        "trend_str": trend_str, "fg_now": fg_now,
        "sup_price": sup_price, "res_price": res_price,
        "mc_prob": mc_prob_7d,
        "buy_entry": sig["buy_entry"], "sell_entry": sig["sell_entry"],
        "buy_tp1": sig["buy_tp1"], "sell_tp1": sig["sell_tp1"],
        "buy_tp2": sig["buy_tp2"], "sell_tp2": sig["sell_tp2"],
        "buy_sl": sig["buy_sl"], "sell_sl": sig["sell_sl"],
    }


# ── SIDEBAR ───────────────────────────────────────────────────────────────────

with st.sidebar:
    # Logogram
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:10px;padding:10px 4px 14px 4px;border-bottom:1px solid #e8e8e8;margin-bottom:14px">
      <div style="width:44px;height:44px;flex-shrink:0">{LOGO_SVG}</div>
      <div>
        <div style="font-size:13px;font-weight:700;color:#111;font-family:sans-serif;letter-spacing:-0.2px">Crypto Trading Signal App</div>
        <div style="font-size:10px;color:#888;font-family:sans-serif;letter-spacing:.8px;margin-top:1px">CTSA &nbsp;·&nbsp; v8.0 &nbsp;<span style="background:#111;color:#fff;padding:1px 5px;border-radius:3px;font-size:9px">BETA</span></div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    coin_label = st.selectbox("Pair", list(COINS.keys()), index=0)
    coin_id    = COINS[coin_label]

    days_label = st.selectbox("Periode", list(DAYS_MAP.keys()), index=0)
    days       = DAYS_MAP[days_label]

    PERIOD_INFO = {
        "1 hari":  "Candle 30 menit · cocok untuk intraday / scalping",
        "7 hari":  "Candle 4 jam · cocok untuk swing trading pendek",
        "14 hari": "Candle harian · cocok untuk swing trading",
        "30 hari": "Candle harian · cocok untuk position trading",
        "90 hari": "Candle mingguan · cocok untuk investasi jangka menengah",
    }
    st.caption(f"ℹ️ {PERIOD_INFO[days_label]}")

    st.markdown("---")
    st.markdown("**Tampilan chart**")
    show_ha       = st.checkbox("Heikin-Ashi (ganti dari candle OHLC)", value=False)
    show_fib      = st.checkbox("Fibonacci Retracement", value=True)
    show_sr       = st.checkbox("Support / Resistance", value=True)
    show_ema      = st.checkbox("EMA 20 / 50", value=True)
    show_stochrsi = st.checkbox("Stochastic RSI", value=True)
    show_adx      = st.checkbox("ADX / DI", value=True)
    show_obv      = st.checkbox("OBV", value=True)
    show_signals  = st.checkbox("Sinyal Beli / Jual", value=True)
    show_fg       = st.checkbox("Fear & Greed Index", value=True)
    show_mc       = st.checkbox("Simulasi Monte Carlo", value=True)
    show_narasi   = st.checkbox("Narasi Teknikal (300 kata)", value=True)
    show_awam     = st.checkbox("Narasi untuk Awam", value=True)
    show_vpvr     = st.checkbox("VPVR — Volume Profile", value=True)

    st.markdown("---")
    auto_refresh = st.checkbox("Auto-refresh (60 dtk)", value=False)
    if st.button("🔄 Refresh sekarang"):
        st.cache_data.clear()
        st.rerun()

    st.markdown("---")
    st.caption("Data: CoinGecko API · Fear & Greed: alternative.me\nCache 60 dtk · v8.0")


# ── MAIN ──────────────────────────────────────────────────────────────────────

with st.spinner("Mengambil data dari CoinGecko..."):
    try:
        df     = fetch_ohlc(coin_id, days)
        market = fetch_market(coin_id)
    except requests.exceptions.HTTPError as e:
        st.warning("⚠️ CoinGecko rate limit. Tunggu 60 detik lalu refresh.") if "429" in str(e) else st.error(f"Error: {e}")
        st.stop()
    except Exception as e:
        st.error(f"Gagal mengambil data: {e}"); st.stop()

fg_data = fetch_fear_greed() if show_fg else []

md        = market.get("market_data", {})
cur_price = md.get("current_price", {}).get("usd", df["close"].iloc[-1])
pct_24h   = md.get("price_change_percentage_24h", 0) or 0
high_24h  = md.get("high_24h", {}).get("usd", df["high"].max())
low_24h   = md.get("low_24h", {}).get("usd", df["low"].min())
mkt_cap   = md.get("market_cap", {}).get("usd", 0)
vol_24h   = md.get("total_volume", {}).get("usd", 0)

# ── Title (after data so pct_24h is available)
pct_sign    = "+" if pct_24h >= 0 else ""
pct_bg      = "#eaf3de" if pct_24h >= 0 else "#fcebeb"
pct_color   = "#27500a" if pct_24h >= 0 else "#791f1f"
bar_color   = "#3b6d11" if pct_24h >= 0 else "#a32d2d"
price_str_h = f"${cur_price:,.2f}"
pct_str_h   = f"{pct_sign}{pct_24h:.2f}%"
time_str_h  = datetime.now().strftime("%H:%M:%S")

st.markdown(f"""
<div style="margin:0 0 0 0;padding:14px 18px;border-left:4px solid {bar_color};background:#f8f9fa;border-radius:0 8px 8px 0;display:flex;align-items:stretch;justify-content:space-between;gap:16px;flex-wrap:wrap">
  <div>
    <div style="font-size:10px;font-weight:700;letter-spacing:1.5px;color:#999;text-transform:uppercase;margin-bottom:6px;font-family:sans-serif">
      Dashboard &nbsp;·&nbsp; {days_label} &nbsp;·&nbsp; {time_str_h}
    </div>
    <div style="display:flex;align-items:center;gap:12px;flex-wrap:wrap">
      <span style="font-size:20px;font-weight:700;color:#111;font-family:sans-serif">{coin_label}</span>
      <span style="font-size:24px;font-weight:700;color:#111;font-family:sans-serif;letter-spacing:-0.5px">{price_str_h}</span>
      <span style="font-size:13px;font-weight:600;padding:3px 10px;border-radius:20px;background:{pct_bg};color:{pct_color};font-family:sans-serif">{pct_str_h}</span>
    </div>
  </div>
  <div style="display:flex;align-items:center;gap:12px;padding-left:18px;border-left:1px solid #e0e0e0">
    <div style="width:48px;height:48px;flex-shrink:0">{LOGO_SVG}</div>
    <div style="text-align:right">
      <div style="font-size:15px;font-weight:700;color:#111;font-family:sans-serif;letter-spacing:-0.3px;white-space:nowrap">Crypto Trading Signal App</div>
      <div style="font-size:11px;font-weight:600;color:#888;font-family:sans-serif;letter-spacing:1px;margin-top:1px;white-space:nowrap">CTSA &nbsp;·&nbsp; v8.0</div>
      <div style="margin-top:5px"><span style="font-size:9px;font-weight:600;padding:2px 7px;border-radius:3px;background:#111;color:#fff;font-family:sans-serif;letter-spacing:.5px">BETA</span></div>
    </div>
  </div>
</div>
<div style="margin:0 0 16px 0;padding:9px 18px;background:#f4f4f4;border-radius:0 0 8px 8px;border:0.5px solid #e8e8e8;border-top:none">
  <span style="font-size:11px;color:#666;line-height:1.6;font-family:sans-serif">
    <strong style="color:#333">CTSA</strong> menggabungkan 9 indikator teknikal, S/R Channels, Fibonacci, Monte Carlo, dan Fear &amp; Greed Index dalam satu dashboard — membantu trader membuat keputusan entry/exit yang lebih terstruktur. Tersedia untuk <strong style="color:#333">{len(COINS)} pasangan aset</strong> · Data real-time via CoinGecko API.
  </span>
</div>
""", unsafe_allow_html=True)

# Compute all indicators
ema20      = calc_ema(df["close"], 20)
ema50      = calc_ema(df["close"], min(50, max(10, len(df)//2)))
rsi        = calc_rsi(df["close"])
stoch_k, stoch_d = calc_stoch_rsi(df["close"])
_, _, macd_hist  = calc_macd(df["close"])
adx_val, di_plus, di_minus = calc_adx(df)
atr_series = calc_atr(df)
obv        = calc_obv(df)
ha         = calc_heikin_ashi(df)
sr_channels = calc_sr_channels(df) if show_sr else []
sig_atr = atr_series.iloc[-1] if not atr_series.empty and not pd.isna(atr_series.iloc[-1]) else cur_price * 0.01
fib_levels  = calc_fibonacci(df)   if show_fib else []
sig = get_signals(df, rsi, stoch_k, stoch_d, macd_hist, ema20, ema50,
                  adx_val, di_plus, di_minus, atr_series, sr_channels)

# ── Metric strip
c1, c2, c3, c4, c5, c6 = st.columns(6)
c1.metric("Harga",       fmt_price(cur_price), f"{pct_24h:+.2f}%")
c2.metric("24h High",    fmt_price(high_24h))
c3.metric("24h Low",     fmt_price(low_24h))
c4.metric("Market Cap",  fmt_large(mkt_cap))
c5.metric("Volume 24h",  fmt_large(vol_24h))
atr_now = round(sig["atr"], 2 if cur_price < 100 else 0)
c6.metric("ATR (14)",    fmt_price(atr_now), "volatilitas harian")

st.markdown("---")

# ── Main chart
fig_main = build_main_chart(
    df, ha,
    ema20 if show_ema else pd.Series([None]*len(df), index=df.index),
    ema50 if show_ema else pd.Series([None]*len(df), index=df.index),
    sr_channels, fib_levels,
    rsi, stoch_k, stoch_d, macd_hist,
    adx_val, di_plus, di_minus,
    obv, atr_series,
    show_ha, show_adx, show_obv, show_stochrsi
)
st.plotly_chart(fig_main, use_container_width=True)

# ── S/R + Fibonacci row
col_sr, col_fib = st.columns(2)
with col_sr:
    st.markdown("##### Support / Resistance Channels")
    st.caption(
        "Zona harga di mana pasar berulang kali berbalik arah. "
        "Semakin tinggi Strength, semakin kuat zona tersebut sebagai batas pergerakan."
    )
    if sr_channels:
        st.plotly_chart(build_sr_chart(sr_channels, cur_price), use_container_width=True)

        sr_rows = []
        for i, ch in enumerate(sr_channels[:6]):
            is_res = ch["hi"] > cur_price and ch["lo"] > cur_price
            is_sup = ch["hi"] < cur_price
            is_in  = not is_res and not is_sup

            tipe   = "🔴 Resistance" if is_res else "🟢 Support" if is_sup else "🟡 Inside"
            mid    = (ch["hi"] + ch["lo"]) / 2
            width  = ch["hi"] - ch["lo"]
            width_pct = width / cur_price * 100

            # Distance from current price to nearest edge of zone
            if is_res:
                dist_pct = (ch["lo"] - cur_price) / cur_price * 100
                dist_lbl = f"+{dist_pct:.2f}%"
            elif is_sup:
                dist_pct = (cur_price - ch["hi"]) / cur_price * 100
                dist_lbl = f"-{dist_pct:.2f}%"
            else:
                dist_lbl = "Di dalam zona"

            # Action suggestion
            if is_res:
                if (ch["lo"] - cur_price) / cur_price < 0.015:
                    aksi = "⚠️ Dekat — siap jual / ambil profit"
                else:
                    aksi = "Target TP / area jual"
            elif is_sup:
                if (cur_price - ch["hi"]) / cur_price < 0.015:
                    aksi = "⚠️ Dekat — siap beli / tambah posisi"
                else:
                    aksi = "Area beli / pasang limit order"
            else:
                aksi = "Harga sedang di dalam zona — tunggu breakout"

            # Strength label
            s = ch["strength"]
            s_lbl = "🔥 Sangat kuat" if s >= 30 else "💪 Kuat" if s >= 20 else "👌 Sedang"

            sr_rows.append({
                "No": f"#{i+1}",
                "Tipe": tipe,
                "Zona (Low – High)": f"{fmt_price(ch['lo'])} – {fmt_price(ch['hi'])}",
                "Lebar zona": f"{fmt_price(width)} ({width_pct:.2f}%)",
                "Jarak dari harga": dist_lbl,
                "Pivot hits": ch.get("pivot_count", "—"),
                "Bar sentuh": ch.get("touch_count", "—"),
                "Strength": f"{s_lbl} ({s})",
                "Rekomendasi": aksi,
            })

        df_sr = pd.DataFrame(sr_rows)
        st.dataframe(df_sr, use_container_width=True, hide_index=True)

        # Callout: nearest support and resistance
        sup_zones = [ch for ch in sr_channels if ch["hi"] < cur_price]
        res_zones = [ch for ch in sr_channels if ch["lo"] > cur_price]
        if sup_zones:
            nearest_sup = max(sup_zones, key=lambda x: x["hi"])
            d = (cur_price - nearest_sup["hi"]) / cur_price * 100
            st.success(
                f"**Support terdekat:** {fmt_price(nearest_sup['lo'])} – {fmt_price(nearest_sup['hi'])}  "
                f"| Jarak: {d:.2f}% di bawah harga sekarang  "
                f"| Pivot hits: {nearest_sup.get('pivot_count','—')}x"
            )
        if res_zones:
            nearest_res = min(res_zones, key=lambda x: x["lo"])
            d = (nearest_res["lo"] - cur_price) / cur_price * 100
            st.error(
                f"**Resistance terdekat:** {fmt_price(nearest_res['lo'])} – {fmt_price(nearest_res['hi'])}  "
                f"| Jarak: {d:.2f}% di atas harga sekarang  "
                f"| Pivot hits: {nearest_res.get('pivot_count','—')}x"
            )

with col_fib:
    st.markdown("##### Fibonacci Retracement")
    if fib_levels:
        fib_rows = []
        for f in fib_levels:
            dist = (cur_price - f["price"]) / cur_price * 100
            zone = "AT LEVEL" if abs(dist) < 0.5 else ("above" if dist > 0 else "below")
            fib_rows.append({"Level": f["label"], "Harga": fmt_price(f["price"]),
                              "Jarak": f"{dist:+.2f}%", "Posisi": zone})
        st.dataframe(pd.DataFrame(fib_rows), use_container_width=True, hide_index=True)

st.markdown("---")

# ── Signals
if show_signals:
    st.markdown("##### Sinyal Beli & Jual")
    st.caption("Entry berbasis limit order — pasang di harga yang tertera, bukan market order.")
    sc1, sc2 = st.columns(2)

    def pill(strength, side):
        score = sig["buy_score"] if side == "buy" else sig["sell_score"]
        mx    = sig["max_score"]
        label = f"{strength} · score {score}/{mx}"
        if strength == "STRONG":
            cls = "eb-pill-buy" if side == "buy" else "eb-pill-sell"
        elif strength == "MODERATE":
            cls = "eb-pill-mod"
        else:
            cls = "eb-pill-weak"
        return f'<span class="{cls}">{label}</span>'

    def ind_rows_html(indicators, side):
        rows = ""
        dot_on  = "eb-dot-on-buy" if side == "buy" else "eb-dot-on-sell"
        sc_on   = "eb-ind-score-buy" if side == "buy" else "eb-ind-score-sell"
        for name, fired, pts in indicators:
            dot = dot_on if fired else "eb-dot-off"
            sc  = f'<span class="{sc_on}">+{pts}</span>' if fired else '<span class="eb-ind-score-off">—</span>'
            rows += f'''<div class="eb-ind-row">
              <span class="eb-ind-name"><span class="{dot}"></span>{name}</span>{sc}
            </div>'''
        return rows

    def ladder_buy():
        return f'''
        <div class="eb-ladder">
          <div class="eb-ladder-line-buy"></div>
          <div class="eb-lev-row">
            <span class="eb-lev-dot" style="background:#27500a"></span>
            <span class="eb-lev-key">Target 3 <small style="color:#888;font-size:9px">(R/R 6:1 · S/R dinamis)</small></span>
            <div class="eb-lev-right">
              <span class="eb-lev-price">{fmt_price(sig["buy_tp3"])}</span>
              <span class="eb-badge eb-badge-tp-buy">{sig["buy_tp3_pct"]}</span>
            </div>
          </div>
          <div class="eb-lev-row">
            <span class="eb-lev-dot" style="background:#3b6d11"></span>
            <span class="eb-lev-key">Target 2 <small style="color:#888;font-size:9px">(R/R 4:1)</small></span>
            <div class="eb-lev-right">
              <span class="eb-lev-price">{fmt_price(sig["buy_tp2"])}</span>
              <span class="eb-badge eb-badge-tp-buy">{sig["buy_tp2_pct"]}</span>
            </div>
          </div>
          <div class="eb-lev-row">
            <span class="eb-lev-dot" style="background:#639922"></span>
            <span class="eb-lev-key">Target 1 <small style="color:#888;font-size:9px">(R/R 2:1)</small></span>
            <div class="eb-lev-right">
              <span class="eb-lev-price">{fmt_price(sig["buy_tp1"])}</span>
              <span class="eb-badge eb-badge-tp-buy">{sig["buy_tp1_pct"]}</span>
            </div>
          </div>
          <div class="eb-lev-row">
            <span class="eb-lev-dot" style="background:#888;border:2px solid #27500a"></span>
            <span class="eb-lev-key-entry">Entry</span>
            <div class="eb-lev-right">
              <span class="eb-lev-price eb-lev-price-entry" style="color:#27500a">{fmt_price(sig["buy_entry"])}</span>
              <span class="eb-badge eb-badge-entry">limit</span>
            </div>
          </div>
          <div class="eb-lev-row">
            <span class="eb-lev-dot" style="background:#a32d2d"></span>
            <span class="eb-lev-key" style="color:#a32d2d">Stop Loss <small style="color:#888;font-size:9px">(1 ATR)</small></span>
            <div class="eb-lev-right">
              <span class="eb-lev-price" style="color:#a32d2d">{fmt_price(sig["buy_sl"])}</span>
              <span class="eb-badge eb-badge-sl-buy">{sig["buy_sl_pct"]}</span>
            </div>
          </div>
        </div>'''

    def ladder_sell():
        return f'''
        <div class="eb-ladder">
          <div class="eb-ladder-line-sell"></div>
          <div class="eb-lev-row">
            <span class="eb-lev-dot" style="background:#3b6d11"></span>
            <span class="eb-lev-key" style="color:#3b6d11">Stop Loss <small style="color:#888;font-size:9px">(1 ATR)</small></span>
            <div class="eb-lev-right">
              <span class="eb-lev-price" style="color:#3b6d11">{fmt_price(sig["sell_sl"])}</span>
              <span class="eb-badge eb-badge-sl-sell">{sig["sell_sl_pct"]}</span>
            </div>
          </div>
          <div class="eb-lev-row">
            <span class="eb-lev-dot" style="background:#888;border:2px solid #791f1f"></span>
            <span class="eb-lev-key-entry">Entry</span>
            <div class="eb-lev-right">
              <span class="eb-lev-price eb-lev-price-entry" style="color:#791f1f">{fmt_price(sig["sell_entry"])}</span>
              <span class="eb-badge eb-badge-entry">limit</span>
            </div>
          </div>
          <div class="eb-lev-row">
            <span class="eb-lev-dot" style="background:#d85a30"></span>
            <span class="eb-lev-key">Target 1 <small style="color:#888;font-size:9px">(R/R 2:1)</small></span>
            <div class="eb-lev-right">
              <span class="eb-lev-price">{fmt_price(sig["sell_tp1"])}</span>
              <span class="eb-badge eb-badge-tp-sell">{sig["sell_tp1_pct"]}</span>
            </div>
          </div>
          <div class="eb-lev-row">
            <span class="eb-lev-dot" style="background:#a32d2d"></span>
            <span class="eb-lev-key">Target 2 <small style="color:#888;font-size:9px">(R/R 4:1)</small></span>
            <div class="eb-lev-right">
              <span class="eb-lev-price">{fmt_price(sig["sell_tp2"])}</span>
              <span class="eb-badge eb-badge-tp-sell">{sig["sell_tp2_pct"]}</span>
            </div>
          </div>
          <div class="eb-lev-row">
            <span class="eb-lev-dot" style="background:#501313"></span>
            <span class="eb-lev-key">Target 3 <small style="color:#888;font-size:9px">(R/R 6:1 · S/R dinamis)</small></span>
            <div class="eb-lev-right">
              <span class="eb-lev-price">{fmt_price(sig["sell_tp3"])}</span>
              <span class="eb-badge eb-badge-tp-sell">{sig["sell_tp3_pct"]}</span>
            </div>
          </div>
        </div>'''

    buy_action_cls  = "eb-action-buy"  if sig["buy_strength"]  == "STRONG"   else "eb-action-warn"
    sell_action_cls = "eb-action-sell" if sig["sell_strength"] == "STRONG"   else "eb-action-warn"

    rr_buy_interp  = "Profit 2× lebih besar dari risiko (standar profesional)"
    rr_sell_interp = "Profit 2× lebih besar dari risiko (standar profesional)"

    with sc1:
        st.markdown(f"""
        <div class="eb-card eb-buy">
          <div class="eb-hdr">
            <span class="eb-label-buy">BUY SIGNAL</span>
            {pill(sig['buy_strength'], 'buy')}
          </div>
          <div class="eb-entry-block eb-entry-block-buy">
            <div class="eb-entry-lbl">Entry — pasang limit order di</div>
            <div class="eb-price-buy">{fmt_price(sig['buy_entry'])}</div>
            <div class="eb-price-sub">{sig['buy_entry_pct']} dari harga pasar ({fmt_price(sig['price'])})</div>
          </div>
          <div class="eb-ind-block eb-ind-block-buy">
            <div class="eb-ind-title-buy">Konfirmasi indikator</div>
            {ind_rows_html(sig['all_indicators'], 'buy')}
          </div>
          <div class="eb-levels">
            <div class="eb-lev-title">Level harga</div>
            {ladder_buy()}
          </div>
          <div class="eb-rr-block eb-rr-buy">
            <div>
              <div class="eb-rr-label">Risk / Reward</div>
              <div class="eb-rr-interp">{rr_buy_interp}</div>
            </div>
            <div class="eb-rr-val-buy">{sig['buy_rr']} : 1</div>
          </div>
          <div class="{buy_action_cls}">{sig['buy_action']}</div>
          <div class="eb-advice">{sig['buy_advice']}</div>
        </div>
        """, unsafe_allow_html=True)

    with sc2:
        st.markdown(f"""
        <div class="eb-card eb-sell">
          <div class="eb-hdr">
            <span class="eb-label-sell">SELL SIGNAL</span>
            {pill(sig['sell_strength'], 'sell')}
          </div>
          <div class="eb-entry-block eb-entry-block-sell">
            <div class="eb-entry-lbl">Entry — pasang limit order di</div>
            <div class="eb-price-sell">{fmt_price(sig['sell_entry'])}</div>
            <div class="eb-price-sub">{sig['sell_entry_pct']} dari harga pasar ({fmt_price(sig['price'])})</div>
          </div>
          <div class="eb-ind-block eb-ind-block-sell">
            <div class="eb-ind-title-sell">Konfirmasi indikator</div>
            {ind_rows_html(sig['sell_indicators'], 'sell')}
          </div>
          <div class="eb-levels">
            <div class="eb-lev-title">Level harga</div>
            {ladder_sell()}
          </div>
          <div class="eb-rr-block eb-rr-sell">
            <div>
              <div class="eb-rr-label">Risk / Reward</div>
              <div class="eb-rr-interp">{rr_sell_interp}</div>
            </div>
            <div class="eb-rr-val-sell">{sig['sell_rr']} : 1</div>
          </div>
          <div class="{sell_action_cls}">{sig['sell_action']}</div>
          <div class="eb-advice">{sig['sell_advice']}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

# ── Indicator summary
st.markdown("##### Ringkasan Indikator")
i1, i2, i3, i4, i5, i6 = st.columns(6)

rsi_v   = round(sig["rsi"], 1)
rsi_lbl = "Oversold" if rsi_v < 35 else "Overbought" if rsi_v > 65 else "Neutral"
i1.metric("RSI (14)", f"{rsi_v}", rsi_lbl)

sk_v = round(sig["stoch_k"], 1); sd_v = round(sig["stoch_d"], 1)
sk_lbl = "Oversold" if sk_v < 20 else "Overbought" if sk_v > 80 else "Neutral"
i2.metric("Stoch RSI %K", f"{sk_v}", sk_lbl)

hist_v  = round(sig["hist"], 2)
i3.metric("MACD Hist", f"{hist_v:+}", "Bullish" if hist_v > 0 else "Bearish")

adx_v = round(sig["adx"], 1)
adx_lbl = "Trending" if adx_v > 25 else "Sideways"
adx_dir = "+DI" if sig["dip"] > sig["dim"] else "-DI"
i4.metric("ADX (14)", f"{adx_v}", f"{adx_lbl} · {adx_dir}")

ema_gap = round((sig["e20"]-sig["e50"])/sig["e50"]*100, 3) if sig["e50"] else 0
i5.metric("EMA 20/50", f"{ema_gap:+.2f}%", "Golden cross" if ema_gap > 0 else "Death cross")

total = sig["buy_score"] - sig["sell_score"]
trend = "Bullish" if total > 2 else "Bearish" if total < -2 else "Sideways"
i6.metric("Trend Bias", trend, f"score {total:+}")

# ── Fear & Greed section
if show_fg and fg_data:
    st.markdown("---")
    st.markdown("##### Fear & Greed Index")
    fg1, fg2, fg3 = st.columns([1, 2, 2])

    fg_now   = int(fg_data[0]["value"])
    fg_yday  = int(fg_data[1]["value"]) if len(fg_data) > 1 else fg_now
    fg_7d    = int(fg_data[6]["value"]) if len(fg_data) > 6 else fg_now
    fg_label = fg_data[0]["value_classification"]

    with fg1:
        st.plotly_chart(build_fg_gauge(fg_now), use_container_width=True)
        st.markdown(f"""
        <div style="font-size:11px;color:var(--text-color,#444);margin-top:-10px">
          <div style="display:flex;justify-content:space-between;padding:3px 0;border-top:1px solid #eee">
            <span style="color:#888">Kemarin</span><span><b>{fg_yday}</b></span>
          </div>
          <div style="display:flex;justify-content:space-between;padding:3px 0;border-top:1px solid #eee">
            <span style="color:#888">7 hari lalu</span><span><b>{fg_7d}</b></span>
          </div>
        </div>""", unsafe_allow_html=True)

    with fg2:
        st.markdown("**Histori 14 hari**")
        fg_hist_fig = build_fg_history(fg_data)
        if fg_hist_fig:
            st.plotly_chart(fg_hist_fig, use_container_width=True)

    with fg3:
        st.markdown("**Cara membaca**")
        st.markdown("""
| Nilai | Klasifikasi | Sinyal |
|-------|-------------|--------|
| 0–24  | Extreme Fear | Potensi beli (contrarian) |
| 25–44 | Fear | Hati-hati, bias beli |
| 45–55 | Neutral | Tunggu konfirmasi |
| 56–74 | Greed | Mulai kurangi posisi |
| 75–100 | Extreme Greed | Potensi jual (contrarian) |
""")
        if fg_now <= 24:
            st.success(f"Saat ini Extreme Fear ({fg_now}) — secara historis ini zona akumulasi.")
        elif fg_now >= 75:
            st.warning(f"Saat ini Extreme Greed ({fg_now}) — pasar mungkin overbought.")
        else:
            st.info(f"Saat ini {fg_label} ({fg_now}).")

# ── Heikin-Ashi info
if show_ha:
    st.markdown("---")
    st.markdown("##### Analisis Heikin-Ashi")
    ha_last = ha.iloc[-1]
    ha_body = ha_last["ha_close"] - ha_last["ha_open"]
    ha_upper_wick = ha_last["ha_high"] - max(ha_last["ha_close"], ha_last["ha_open"])
    ha_lower_wick = min(ha_last["ha_close"], ha_last["ha_open"]) - ha_last["ha_low"]

    h1, h2, h3, h4 = st.columns(4)
    h1.metric("HA Close", fmt_price(ha_last["ha_close"]))
    h2.metric("HA Open",  fmt_price(ha_last["ha_open"]))
    color_candle = "Bullish (hijau)" if ha_body > 0 else "Bearish (merah)"
    h3.metric("Candle", color_candle)
    no_lower = ha_lower_wick < abs(ha_body) * 0.1
    h4.metric("Lower wick", "Sangat kecil — tren kuat" if no_lower else fmt_price(ha_lower_wick))

st.markdown("---")
st.caption(
    f"Sumber: CoinGecko API · Fear & Greed: alternative.me · "
    f"Terakhir diperbarui: {datetime.now().strftime('%H:%M:%S')} · "
    f"Candle: {len(df)} · Disclaimer: bukan saran investasi."
)

# ── Monte Carlo panel
if show_mc:
    st.markdown("---")
    st.markdown("##### Simulasi Monte Carlo — Proyeksi Harga")
    st.caption(
        "Menjalankan 600 simulasi acak berbasis volatilitas historis (Geometric Brownian Motion). "
        "Bukan prediksi pasti — ini distribusi probabilitas skenario yang mungkin terjadi. "
        "Area ungu gelap = 50% simulasi masuk rentang ini. Area ungu muda = 80% simulasi."
    )

    with st.spinner("Menjalankan 600 simulasi Monte Carlo..."):
        mc_fig, mc_sims, mc_p10, mc_p25, mc_p50, mc_p75, mc_p90 = build_monte_carlo_chart(df["close"], coin_label)

    st.plotly_chart(mc_fig, use_container_width=True)

    # Prediction table per horizon
    horizons = [
        (3,   "3 hari"),
        (7,   "7 hari"),
        (30,  "30 hari"),
        (90,  "90 hari"),
        (365, "365 hari"),
    ]
    mc_rows = []
    for d, lbl in horizons:
        idx = d - 1
        p10v  = mc_p10[idx]
        p25v  = mc_p25[idx]
        p50v  = mc_p50[idx]
        p75v  = mc_p75[idx]
        p90v  = mc_p90[idx]
        prob_up = (mc_sims[idx] > cur_price).mean() * 100
        mc_rows.append({
            "Horizon":         lbl,
            "Pesimis (P10)":   fmt_price(p10v),
            "Bawah (P25)":     fmt_price(p25v),
            "Median (P50)":    fmt_price(p50v),
            "Atas (P75)":      fmt_price(p75v),
            "Optimis (P90)":   fmt_price(p90v),
            "Prob. naik":      f"{prob_up:.1f}%",
            "Rentang P25–P75": f"{fmt_price(p25v)} – {fmt_price(p75v)}",
        })
    st.dataframe(pd.DataFrame(mc_rows), use_container_width=True, hide_index=True)

    # Key callouts
    mc_col1, mc_col2, mc_col3 = st.columns(3)
    d7_up   = (mc_sims[6]   > cur_price).mean() * 100
    d30_up  = (mc_sims[29]  > cur_price).mean() * 100
    d365_up = (mc_sims[364] > cur_price).mean() * 100
    mc_col1.metric("Prob. naik 7 hari",   f"{d7_up:.1f}%",
                   "bullish" if d7_up > 55 else "bearish" if d7_up < 45 else "netral")
    mc_col2.metric("Prob. naik 30 hari",  f"{d30_up:.1f}%",
                   "bullish" if d30_up > 55 else "bearish" if d30_up < 45 else "netral")
    mc_col3.metric("Prob. naik 365 hari", f"{d365_up:.1f}%",
                   "bullish" if d365_up > 55 else "bearish" if d365_up < 45 else "netral")

    with st.expander("Cara membaca simulasi Monte Carlo"):
        st.markdown("""
**Apa itu Monte Carlo?**
Model ini mensimulasikan ribuan kemungkinan jalur harga di masa depan berdasarkan dua parameter historis: **drift** (kecenderungan rata-rata naik/turun) dan **volatilitas** (seberapa liar pergerakan harganya).

**Cara membaca tabel:**
| Kolom | Artinya |
|-------|---------|
| Pesimis P10 | 90% simulasi menghasilkan harga di atas angka ini |
| Bawah P25 | 75% simulasi menghasilkan harga di atas angka ini |
| Median P50 | Titik tengah — 50% di atas, 50% di bawah |
| Atas P75 | Hanya 25% simulasi mencapai harga ini atau lebih |
| Optimis P90 | Hanya 10% simulasi mencapai harga ini (skenario paling bullish) |
| Prob. naik | Persentase simulasi yang berakhir di atas harga sekarang |

**Catatan penting:**
Monte Carlo bukan crystal ball. Semakin jauh horizon waktu, semakin lebar cone ketidakpastiannya. Gunakan sebagai **konteks risiko**, bukan sebagai sinyal entry/exit.
        """)

# ── Collect MC and FG values for narratives
_mc_prob_7d  = float((mc_sims[6] > cur_price).mean() * 100) if show_mc and 'mc_sims' in dir() else None
_fg_now      = int(fg_data[0]["value"]) if (show_fg and fg_data) else None
_sr_all      = calc_sr_channels(df)   # always compute for narratives

# ── Narasi Teknikal (300 kata)
if show_narasi:
    st.markdown("---")
    st.markdown("##### Narasi Teknikal")
    st.caption("Ringkasan analisis teknikal dalam format narasi — dapat disalin untuk referensi artikel atau konten.")

    narasi_teknikal = generate_technical_narrative(
        coin_label, cur_price, pct_24h, sig,
        fib_levels if fib_levels else calc_fibonacci(df),
        _sr_all, _fg_now, _mc_prob_7d, days_label
    )

    # Header kartu narasi
    total_score = sig["buy_score"] - sig["sell_score"]
    bias_lbl  = "Bullish" if total_score > 0 else "Bearish" if total_score < 0 else "Netral"
    bias_clr  = "#27500a" if total_score > 0 else "#791f1f" if total_score < 0 else "#444"
    bias_bg2  = "#eaf3de" if total_score > 0 else "#fcebeb" if total_score < 0 else "#f1efe8"
    tags_html = "".join([
        f'<span style="font-size:10px;padding:2px 8px;border-radius:20px;background:#f1f1f1;color:#666;font-family:sans-serif;margin-right:4px">{t}</span>'
        for t in [coin_label, days_label, bias_lbl,
                  f"RSI {round(sig['rsi'],1)}",
                  f"ADX {round(sig['adx'],1)}",
                  f"MC {_mc_prob_7d:.0f}%" if _mc_prob_7d else ""]
        if t
    ])
    st.markdown(f"""
<div style="background:#fff;border:0.5px solid #e8e8e8;border-radius:12px;padding:22px 26px;font-family:sans-serif">
  <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:14px;padding-bottom:10px;border-bottom:1px solid #f0f0f0;flex-wrap:wrap;gap:8px">
    <span style="font-size:13px;font-weight:700;color:#111">Analisis Teknikal — {coin_label} &nbsp;·&nbsp; {days_label}</span>
    <span style="font-size:10px;color:#aaa;text-align:right">
      {datetime.now().strftime("%d %b %Y, %H:%M")} &nbsp;·&nbsp;
      <span style="font-weight:700;color:{bias_clr}">{bias_lbl}</span>
    </span>
  </div>
  <div style="font-size:13px;line-height:1.9;color:#333;text-align:justify;white-space:pre-line">{narasi_teknikal}</div>
  <div style="margin-top:14px;padding-top:10px;border-top:1px solid #f0f0f0;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:8px">
    <div>{tags_html}</div>
    <span style="font-size:10px;color:#bbb;font-style:italic">Salin teks di atas untuk referensi artikel atau konten</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Narasi untuk Awam
if show_awam:
    st.markdown("---")
    st.markdown("##### Ringkasan untuk Pemula")
    st.caption("Penjelasan kondisi pasar dalam bahasa sederhana — fokus pada keputusan: beli, jual, atau tunggu.")

    aw = generate_simple_narrative(
        coin_label, cur_price, pct_24h, sig,
        _sr_all, _fg_now, _mc_prob_7d
    )

    is_bull_aw = aw["is_bull"]
    hero_bg    = "#eaf3de" if is_bull_aw else "#fcebeb" if aw["bias"].startswith("JUAL") else "#f1f0eb"
    strip_bg   = "#f2faf0" if is_bull_aw else "#fff8f8" if aw["bias"].startswith("JUAL") else "#f8f8f6"
    icon_svg   = (
        '<svg width="26" height="26" viewBox="0 0 26 26" fill="none" xmlns="http://www.w3.org/2000/svg">'
        '<polyline points="4,18 10,10 16,14 22,5" stroke="#fff" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>'
        '<polyline points="22,5 22,11" stroke="#fff" stroke-width="2.5" stroke-linecap="round"/>'
        '<polyline points="22,5 16,5" stroke="#fff" stroke-width="2.5" stroke-linecap="round"/>'
        '</svg>'
        if is_bull_aw else
        '<svg width="26" height="26" viewBox="0 0 26 26" fill="none" xmlns="http://www.w3.org/2000/svg">'
        '<polyline points="4,8 10,16 16,12 22,21" stroke="#fff" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>'
        '<polyline points="22,21 22,15" stroke="#fff" stroke-width="2.5" stroke-linecap="round"/>'
        '<polyline points="22,21 16,21" stroke="#fff" stroke-width="2.5" stroke-linecap="round"/>'
        '</svg>'
    )

    entry_p  = fmt_price(aw["buy_entry"]  if is_bull_aw else aw["sell_entry"])
    tp1_p    = fmt_price(aw["buy_tp1"]   if is_bull_aw else aw["sell_tp1"])
    tp2_p    = fmt_price(aw["buy_tp2"]   if is_bull_aw else aw["sell_tp2"])
    sl_p     = fmt_price(aw["buy_sl"]    if is_bull_aw else aw["sell_sl"])
    entry_lbl= "Beli di" if is_bull_aw else "Jual di"

    info_items = [
        ("Tren saat ini",       aw["trend_str"].capitalize(),              "EMA 20/50"),
        ("Kekuatan tren",       "ADX " + str(aw['adx']),                  "Kuat" if aw['adx']>25 else "Lemah"),
        ("Momentum",            "RSI " + str(aw['rsi']),                  "Oversold" if aw['rsi']<35 else "Overbought" if aw['rsi']>65 else "Normal"),
        ("Sentimen pasar",      ("F&amp;G " + str(_fg_now) + "/100") if _fg_now else "—",
                                ("Extreme Fear" if _fg_now<=24 else "Greed" if _fg_now>=60 else "Neutral") if _fg_now else "—"),
        ("Peluang naik 7 hari", (str(round(_mc_prob_7d)) + "%") if _mc_prob_7d else "—", "Monte Carlo"),
        ("Volatilitas harian",  fmt_price(round(sig['atr'], 2 if cur_price<100 else 0)), "ATR 14"),
    ]

    # Build info grid as a clean string (no nested f-strings)
    info_divs = ""
    for lbl, val, sub in info_items:
        info_divs += (
            '<div style="background:#f8f8f8;border-radius:8px;padding:10px 12px">'
            '<div style="font-size:9px;font-weight:700;text-transform:uppercase;letter-spacing:.8px;'
            'color:#999;margin-bottom:3px;font-family:sans-serif">' + lbl + '</div>'
            '<div style="font-size:13px;font-weight:700;color:#111;font-family:sans-serif">' + val + '</div>'
            '<div style="font-size:10px;color:#888;margin-top:1px;font-family:sans-serif">' + sub + '</div>'
            '</div>'
        )

    tp_color  = "#27500a" if is_bull_aw else "#791f1f"
    sl_color  = "#791f1f" if is_bull_aw else "#27500a"
    n_ind     = str(len(sig['all_indicators']))
    conf_w    = str(aw['conf']) + "%"

    awam_html = (
        '<div style="border-radius:12px;overflow:hidden;border:1px solid #e0e0e0;font-family:sans-serif">'

        # Hero
        '<div style="padding:18px 22px;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:14px;background:' + hero_bg + '">'
          '<div style="display:flex;align-items:center;gap:14px">'
            '<div style="width:50px;height:50px;border-radius:50%;background:' + aw['bar_color'] + ';display:flex;align-items:center;justify-content:center;flex-shrink:0">'
              + icon_svg +
            '</div>'
            '<div>'
              '<div style="font-size:22px;font-weight:800;color:' + aw['bias_color'] + ';letter-spacing:-0.5px;line-height:1.1">Sinyal ' + aw['bias'] + '</div>'
              '<div style="font-size:12px;color:#5f5e5a;margin-top:3px;font-weight:500">Berdasarkan analisis ' + n_ind + ' indikator teknikal</div>'
            '</div>'
          '</div>'
          '<div style="text-align:right">'
            '<div style="font-size:10px;color:#888;text-transform:uppercase;letter-spacing:.8px;margin-bottom:4px">Kepercayaan sinyal</div>'
            '<div style="width:120px;height:8px;background:rgba(0,0,0,.1);border-radius:4px;overflow:hidden;margin-left:auto">'
              '<div style="height:100%;width:' + conf_w + ';background:' + aw['bar_color'] + ';border-radius:4px"></div>'
            '</div>'
            '<div style="font-size:16px;font-weight:700;color:' + aw['bias_color'] + ';margin-top:4px">' + conf_w + ' <span style="font-size:11px;font-weight:500;color:#888">' + aw['conf_lbl'] + '</span></div>'
          '</div>'
        '</div>'

        # Body
        '<div style="padding:18px 22px;background:#fff">'
          '<p style="font-size:13px;line-height:1.85;color:#333;margin-bottom:16px">' + aw['summary'] + '</p>'
          '<div style="display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px;margin-bottom:4px">'
            + info_divs +
          '</div>'
        '</div>'

        # Action strip
        '<div style="padding:14px 22px;display:flex;align-items:flex-start;justify-content:space-between;flex-wrap:wrap;gap:12px;background:' + strip_bg + ';border-top:1px solid #f0f0f0">'
          '<div>'
            '<div style="font-size:13px;font-weight:700;color:' + aw['bias_color'] + '">' + aw['action_main'] + '</div>'
            '<div style="font-size:11px;color:#888;margin-top:2px">' + aw['action_sub'] + '</div>'
          '</div>'
          '<div style="display:flex;gap:14px;flex-wrap:wrap">'
            '<div style="text-align:center"><span style="font-size:9px;font-weight:700;text-transform:uppercase;letter-spacing:.8px;color:#aaa;display:block;margin-bottom:2px">' + entry_lbl + '</span><span style="font-size:12px;font-weight:700;color:#111">' + entry_p + '</span></div>'
            '<div style="text-align:center"><span style="font-size:9px;font-weight:700;text-transform:uppercase;letter-spacing:.8px;color:#aaa;display:block;margin-bottom:2px">Target 1</span><span style="font-size:12px;font-weight:700;color:' + tp_color + '">' + tp1_p + '</span></div>'
            '<div style="text-align:center"><span style="font-size:9px;font-weight:700;text-transform:uppercase;letter-spacing:.8px;color:#aaa;display:block;margin-bottom:2px">Target 2</span><span style="font-size:12px;font-weight:700;color:' + tp_color + '">' + tp2_p + '</span></div>'
            '<div style="text-align:center"><span style="font-size:9px;font-weight:700;text-transform:uppercase;letter-spacing:.8px;color:#aaa;display:block;margin-bottom:2px">Stop Loss</span><span style="font-size:12px;font-weight:700;color:' + sl_color + '">' + sl_p + '</span></div>'
          '</div>'
        '</div>'

        # Disclaimer
        '<div style="padding:9px 22px;background:#f9f9f9;border-top:1px solid #f0f0f0">'
          '<span style="font-size:10px;color:#bbb;line-height:1.5">Informasi ini bersifat edukatif dan bukan saran investasi. '
          'Keputusan trading sepenuhnya ada di tangan Anda. Pasar kripto sangat volatil dan nilai investasi dapat turun secara signifikan.</span>'
        '</div>'

        '</div>'
    )

    st.html(awam_html)

# ── VPVR Panel (30 hari dan 90 hari saja)
if show_vpvr and days in [30, 90]:
    st.markdown("---")
    st.markdown("##### Volume Profile Visible Range (VPVR)")
    st.caption(
        f"Peta likuiditas pasar {coin_label} berdasarkan distribusi volume {days_label} terakhir. "
        "Sinyal beli/jual murni dari struktur volume — independen dari indikator teknikal lainnya. "
        "Aktif hanya untuk periode 30 hari dan 90 hari."
    )

    with st.spinner("Mengambil data volume harian dari CoinGecko..."):
        try:
            df_vol = fetch_volume_chart(coin_id, days)
            vpvr   = calc_vpvr(df_vol, n_buckets=24)
            vsig   = get_vpvr_signals(vpvr, cur_price)
        except Exception as e:
            st.warning(f"Gagal memuat data VPVR: {e}")
            df_vol = None

    if df_vol is not None:
        poc  = vpvr["poc"]
        vah  = vpvr["vah"]
        val  = vpvr["val"]
        bkts = vpvr["buckets"]
        mxv  = vpvr["max_vol"]

        fig_vp = make_subplots(
            rows=1, cols=2,
            column_widths=[0.72, 0.28],
            shared_yaxes=True,
            horizontal_spacing=0.01,
            subplot_titles=["Harga + Volume Profile", "Distribusi Volume per Level Harga"]
        )

        # Harga
        fig_vp.add_trace(go.Scatter(
            x=df_vol["date"].astype(str), y=df_vol["close"],
            name="Harga", line=dict(color="#185fa5", width=2),
            hovertemplate="%{x}<br>$%{y:,.2f}<extra></extra>"
        ), row=1, col=1)

        # Horizontal lines
        for price_level, color, label in [
            (vah, "#a32d2d", f"VAH {fmt_price(vah)}"),
            (poc, "#534ab7", f"POC {fmt_price(poc)}"),
            (val, "#3b6d11", f"VAL {fmt_price(val)}"),
        ]:
            fig_vp.add_hline(
                y=price_level, line_color=color, line_dash="dot", line_width=1.5,
                annotation_text=label, annotation_position="right",
                annotation_font_size=9, annotation_font_color=color,
                row=1, col=1
            )

        # HVN / LVN zones
        for h in vpvr["hvn_list"][:3]:
            fig_vp.add_hrect(y0=h["lo"], y1=h["hi"],
                fillcolor="rgba(24,95,165,0.08)",
                line_color="rgba(24,95,165,0.3)", line_width=0.5, row=1, col=1)
        for l in vpvr["lvn_list"][:3]:
            fig_vp.add_hrect(y0=l["lo"], y1=l["hi"],
                fillcolor="rgba(136,135,128,0.06)",
                line_color="rgba(136,135,128,0.2)", line_width=0.5, row=1, col=1)

        # VPVR histogram (horizontal bars)
        bar_colors = []
        for b in bkts:
            if abs(b["price"] - poc) < vpvr["bucket_size"]:
                bar_colors.append("rgba(83,74,183,0.75)")
            elif b["price"] > poc:
                bar_colors.append("rgba(163,45,45,0.55)")
            else:
                bar_colors.append("rgba(59,109,17,0.55)")

        vol_pcts = [b["vol_pct"] * 100 for b in bkts]
        prices_mid = [b["price"] for b in bkts]

        fig_vp.add_trace(go.Bar(
            x=vol_pcts,
            y=prices_mid,
            orientation="h",
            name="Volume %",
            marker_color=bar_colors,
            hovertemplate="$%{y:,.0f}<br>Volume: %{x:.1f}%<extra></extra>",
            width=[vpvr["bucket_size"] * 0.85] * len(bkts),
        ), row=1, col=2)

        fig_vp.update_layout(
            height=420,
            margin=dict(l=10, r=90, t=30, b=10),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(248,249,250,0.5)",
            legend=dict(orientation="h", y=1.05, x=0, font=dict(size=10)),
            showlegend=False,
            hovermode="y unified",
        )
        fig_vp.update_xaxes(gridcolor="rgba(128,128,128,0.08)", tickfont=dict(size=9))
        fig_vp.update_yaxes(
            gridcolor="rgba(128,128,128,0.08)", tickfont=dict(size=9),
            tickformat="$,.0f"
        )
        fig_vp.update_xaxes(ticksuffix="%", row=1, col=2)
        st.plotly_chart(fig_vp, use_container_width=True)

        # ── Zona tabel
        dp = 2 if cur_price < 100 else 0
        zone_rows = []
        zone_rows.append({"Zona": "VAH (Value Area High)", "Harga": fmt_price(vah),
                           "Volume": "Tinggi", "Fungsi": "Resistance kuat",
                           "Sinyal": "Jual / ambil profit"})
        for i, l in enumerate(sorted(vpvr["lvn_list"], key=lambda x: -x["price"])[:2]):
            zone_rows.append({"Zona": f"LVN {i+1}", "Harga": fmt_price(l["price"]),
                               "Volume": "Sangat rendah", "Fungsi": "Zona breakout cepat",
                               "Sinyal": "Waspadai pergerakan cepat"})
        zone_rows.append({"Zona": "POC (Point of Control)", "Harga": fmt_price(poc),
                           "Volume": "Tertinggi", "Fungsi": "Titik keseimbangan",
                           "Sinyal": "Beli saat retest dari atas"})
        for i, h in enumerate(sorted(vpvr["hvn_list"], key=lambda x: -x["price"])[:2]):
            zone_rows.append({"Zona": f"HVN {i+1}", "Harga": fmt_price(h["price"]),
                               "Volume": "Tinggi", "Fungsi": "Support kuat",
                               "Sinyal": "Beli di zona ini"})
        zone_rows.append({"Zona": "VAL (Value Area Low)", "Harga": fmt_price(val),
                           "Volume": "Tinggi", "Fungsi": "Support sangat kuat",
                           "Sinyal": "Beli agresif / pertahanan terakhir"})
        st.dataframe(pd.DataFrame(zone_rows), use_container_width=True, hide_index=True)

        # ── Posisi harga + narasi
        st.markdown("---")
        pos_color = "#27500a" if vsig["above_poc"] else "#791f1f"
        st.markdown(f"""
<div style="background:#f8f9fa;border-radius:8px;padding:12px 16px;margin-bottom:10px;border-left:3px solid {pos_color};font-family:sans-serif">
  <div style="font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.8px;color:#888;margin-bottom:6px">Posisi harga saat ini</div>
  <div style="font-size:12px;color:#111;line-height:1.7;margin-bottom:8px"><strong>Teknikal:</strong> {vsig['pos_tech']}</div>
  <div style="font-size:12px;color:#555;line-height:1.7"><strong>Untuk awam:</strong> {vsig['pos_awam']}</div>
</div>
""", unsafe_allow_html=True)

        # ── Sinyal beli/jual
        sc1, sc2 = st.columns(2)

        with sc1:
            buy_pct_tp1 = f"{(vsig['buy_tp1'] - vsig['buy_entry']) / vsig['buy_entry'] * 100:+.1f}%"
            buy_pct_tp2 = f"{(vsig['buy_tp2'] - vsig['buy_entry']) / vsig['buy_entry'] * 100:+.1f}%"
            buy_pct_sl  = f"{(vsig['buy_sl']  - vsig['buy_entry']) / vsig['buy_entry'] * 100:+.1f}%"
            st.markdown(f"""
<div style="background:#eaf3de;border:1px solid #3b6d11;border-radius:10px;padding:16px;font-family:sans-serif">
  <div style="font-size:10px;font-weight:700;color:#27500a;letter-spacing:.5px;margin-bottom:8px">SINYAL BELI — VPVR</div>
  <div style="font-size:20px;font-weight:800;color:#27500a;letter-spacing:-0.5px;margin-bottom:2px">{fmt_price(vsig['buy_entry'])}</div>
  <div style="font-size:11px;color:#5f5e5a;margin-bottom:10px">{vsig['buy_reason']}</div>
  <div style="font-size:11px;color:#3b6d11;line-height:1.6;margin-bottom:10px;padding:8px;background:rgba(59,109,17,0.08);border-radius:6px"><em>{vsig['buy_reason_awam']}</em></div>
  <div style="font-size:11px">
    <div style="display:flex;justify-content:space-between;padding:4px 0;border-top:0.5px solid rgba(59,109,17,0.2)"><span style="color:#888">Target 1 (VAH)</span><span style="font-weight:700;color:#27500a">{fmt_price(vsig['buy_tp1'])} &nbsp;<span style="font-size:10px;background:#c0dd97;color:#27500a;padding:1px 5px;border-radius:3px">{buy_pct_tp1}</span></span></div>
    <div style="display:flex;justify-content:space-between;padding:4px 0;border-top:0.5px solid rgba(59,109,17,0.2)"><span style="color:#888">Target 2 (HVN atas)</span><span style="font-weight:700;color:#27500a">{fmt_price(vsig['buy_tp2'])} &nbsp;<span style="font-size:10px;background:#c0dd97;color:#27500a;padding:1px 5px;border-radius:3px">{buy_pct_tp2}</span></span></div>
    <div style="display:flex;justify-content:space-between;padding:4px 0;border-top:0.5px solid rgba(59,109,17,0.2)"><span style="color:#a32d2d">Stop Loss</span><span style="font-weight:700;color:#a32d2d">{fmt_price(vsig['buy_sl'])} &nbsp;<span style="font-size:10px;background:#f09595;color:#501313;padding:1px 5px;border-radius:3px">{buy_pct_sl}</span></span></div>
    <div style="display:flex;justify-content:space-between;padding:4px 0;border-top:0.5px solid rgba(59,109,17,0.2)"><span style="color:#888">R/R (TP1)</span><span style="font-weight:700;color:#111">{vsig['buy_rr']} : 1</span></div>
  </div>
</div>
""", unsafe_allow_html=True)

        with sc2:
            sell_pct_tp1 = f"{(vsig['sell_tp1'] - vsig['sell_entry']) / vsig['sell_entry'] * 100:+.1f}%"
            sell_pct_tp2 = f"{(vsig['sell_tp2'] - vsig['sell_entry']) / vsig['sell_entry'] * 100:+.1f}%"
            sell_pct_sl  = f"{(vsig['sell_sl']  - vsig['sell_entry']) / vsig['sell_entry'] * 100:+.1f}%"
            st.markdown(f"""
<div style="background:#fcebeb;border:1px solid #a32d2d;border-radius:10px;padding:16px;font-family:sans-serif">
  <div style="font-size:10px;font-weight:700;color:#791f1f;letter-spacing:.5px;margin-bottom:8px">SINYAL JUAL — VPVR</div>
  <div style="font-size:20px;font-weight:800;color:#791f1f;letter-spacing:-0.5px;margin-bottom:2px">{fmt_price(vsig['sell_entry'])}</div>
  <div style="font-size:11px;color:#5f5e5a;margin-bottom:10px">{vsig['sell_reason']}</div>
  <div style="font-size:11px;color:#a32d2d;line-height:1.6;margin-bottom:10px;padding:8px;background:rgba(163,45,45,0.08);border-radius:6px"><em>{vsig['sell_reason_awam']}</em></div>
  <div style="font-size:11px">
    <div style="display:flex;justify-content:space-between;padding:4px 0;border-top:0.5px solid rgba(163,45,45,0.2)"><span style="color:#888">Target 1 (POC)</span><span style="font-weight:700;color:#27500a">{fmt_price(vsig['sell_tp1'])} &nbsp;<span style="font-size:10px;background:#c0dd97;color:#27500a;padding:1px 5px;border-radius:3px">{sell_pct_tp1}</span></span></div>
    <div style="display:flex;justify-content:space-between;padding:4px 0;border-top:0.5px solid rgba(163,45,45,0.2)"><span style="color:#888">Target 2 (VAL)</span><span style="font-weight:700;color:#27500a">{fmt_price(vsig['sell_tp2'])} &nbsp;<span style="font-size:10px;background:#c0dd97;color:#27500a;padding:1px 5px;border-radius:3px">{sell_pct_tp2}</span></span></div>
    <div style="display:flex;justify-content:space-between;padding:4px 0;border-top:0.5px solid rgba(163,45,45,0.2)"><span style="color:#3b6d11">Stop Loss</span><span style="font-weight:700;color:#3b6d11">{fmt_price(vsig['sell_sl'])} &nbsp;<span style="font-size:10px;background:#c0dd97;color:#27500a;padding:1px 5px;border-radius:3px">{sell_pct_sl}</span></span></div>
    <div style="display:flex;justify-content:space-between;padding:4px 0;border-top:0.5px solid rgba(163,45,45,0.2)"><span style="color:#888">R/R (TP1)</span><span style="font-weight:700;color:#111">{vsig['sell_rr']} : 1</span></div>
  </div>
</div>
""", unsafe_allow_html=True)

elif show_vpvr and days not in [30, 90]:
    st.markdown("---")
    st.info("VPVR aktif hanya untuk periode **30 hari** dan **90 hari**. Pilih periode tersebut di sidebar untuk melihat Volume Profile.")

if auto_refresh:
    time.sleep(60)
    st.cache_data.clear()
    st.rerun()
