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
    .block-container { padding-top: 1rem; padding-bottom: 0rem; }
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
    "BTC / USD": "bitcoin",
    "ETH / USD": "ethereum",
    "BNB / USD": "binancecoin",
    "SOL / USD": "solana",
    "XRP / USD": "ripple",
    "ADA / USD": "cardano",
    "DOGE / USD": "dogecoin",
    "AVAX / USD": "avalanche-2",
}

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

    buy_entry = round(price * 0.999, 2 if price < 100 else 0)
    buy_tp1   = round(buy_entry + atr * 2,   2 if price < 100 else 0)
    buy_tp2   = round(buy_entry + atr * 3.5, 2 if price < 100 else 0)
    buy_sl    = round(buy_entry - atr * 1.2, 2 if price < 100 else 0)
    buy_rr    = round((buy_tp1 - buy_entry) / (buy_entry - buy_sl), 2) if (buy_entry - buy_sl) != 0 else 0

    sell_entry = round(price * 1.001, 2 if price < 100 else 0)
    sell_tp1   = round(sell_entry - atr * 2,   2 if price < 100 else 0)
    sell_tp2   = round(sell_entry - atr * 3.5, 2 if price < 100 else 0)
    sell_sl    = round(sell_entry + atr * 1.2, 2 if price < 100 else 0)
    sell_rr    = round((sell_entry - sell_tp1) / (sell_sl - sell_entry), 2) if (sell_sl - sell_entry) != 0 else 0

    MAX_SCORE = 12
    bs = "STRONG" if buy_score >= 6 else "MODERATE" if buy_score >= 3 else "WEAK"
    ss = "STRONG" if sell_score >= 6 else "MODERATE" if sell_score >= 3 else "WEAK"

    # Full indicator breakdown for display
    dp = 2 if price < 100 else 0
    buy_pct  = lambda p: f"{(p - buy_entry)  / buy_entry  * 100:+.2f}%"
    sell_pct = lambda p: f"{(p - sell_entry) / sell_entry * 100:+.2f}%"

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
        "buy_entry": buy_entry, "buy_tp1": buy_tp1, "buy_tp2": buy_tp2,
        "buy_sl": buy_sl, "buy_rr": buy_rr,
        "buy_tp1_pct": buy_pct(buy_tp1), "buy_tp2_pct": buy_pct(buy_tp2),
        "buy_sl_pct":  f"{(buy_sl - buy_entry) / buy_entry * 100:+.2f}%",
        "buy_entry_pct": f"{(buy_entry - price) / price * 100:+.2f}%",
        "sell_entry": sell_entry, "sell_tp1": sell_tp1, "sell_tp2": sell_tp2,
        "sell_sl": sell_sl, "sell_rr": sell_rr,
        "sell_tp1_pct": sell_pct(sell_tp1), "sell_tp2_pct": sell_pct(sell_tp2),
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

    # Candles: Heikin-Ashi or regular line
    if show_ha:
        candle_color = ["#3b6d11" if ha["ha_close"].iloc[i] >= ha["ha_open"].iloc[i] else "#a32d2d"
                        for i in range(len(ha))]
        fig.add_trace(go.Candlestick(
            x=ha["time"], open=ha["ha_open"], high=ha["ha_high"],
            low=ha["ha_low"], close=ha["ha_close"],
            name="Heikin-Ashi",
            increasing_line_color="#3b6d11", increasing_fillcolor="rgba(59,109,17,0.7)",
            decreasing_line_color="#a32d2d", decreasing_fillcolor="rgba(163,45,45,0.7)",
        ), row=1, col=1)
    else:
        fig.add_trace(go.Scatter(
            x=df["time"], y=df["close"], name="Price",
            line=dict(color="#185fa5", width=2),
            hovertemplate="%{x}<br>$%{y:,.4f}<extra></extra>"
        ), row=1, col=1)

    fig.add_trace(go.Scatter(x=df["time"], y=ema20, name="EMA 20",
                             line=dict(color="#ef9f27", width=1.2)), row=1, col=1)
    fig.add_trace(go.Scatter(x=df["time"], y=ema50, name="EMA 50",
                             line=dict(color="#d85a30", width=1, dash="dash")), row=1, col=1)

    buy_mask  = (rsi < 38) | ((macd_hist > 0) & (macd_hist.shift(1) <= 0)) | ((stoch_k < 20) & (stoch_k > stoch_d))
    sell_mask = (rsi > 62) | ((macd_hist < 0) & (macd_hist.shift(1) >= 0)) | ((stoch_k > 80) & (stoch_k < stoch_d))
    fig.add_trace(go.Scatter(x=df["time"][buy_mask], y=df["close"][buy_mask], mode="markers",
                             name="Buy", marker=dict(symbol="triangle-up", size=9, color="#3b6d11")), row=1, col=1)
    fig.add_trace(go.Scatter(x=df["time"][sell_mask], y=df["close"][sell_mask], mode="markers",
                             name="Sell", marker=dict(symbol="triangle-down", size=9, color="#a32d2d")), row=1, col=1)

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


# ── SIDEBAR ───────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("## ⚙️ Settings")
    coin_label = st.selectbox("Pair", list(COINS.keys()), index=0)
    coin_id    = COINS[coin_label]
    days_label = st.selectbox("Periode", list(DAYS_MAP.keys()), index=0)
    days       = DAYS_MAP[days_label]

    st.markdown("---")
    st.markdown("**Tampilan chart**")
    show_ha       = st.checkbox("Heikin-Ashi candles", value=False)
    show_fib      = st.checkbox("Fibonacci Retracement", value=True)
    show_sr       = st.checkbox("Support / Resistance", value=True)
    show_ema      = st.checkbox("EMA 20 / 50", value=True)
    show_stochrsi = st.checkbox("Stochastic RSI", value=True)
    show_adx      = st.checkbox("ADX / DI", value=True)
    show_obv      = st.checkbox("OBV", value=True)
    show_signals  = st.checkbox("Sinyal Beli / Jual", value=True)
    show_fg       = st.checkbox("Fear & Greed Index", value=True)

    st.markdown("---")
    auto_refresh = st.checkbox("Auto-refresh (60 dtk)", value=False)
    if st.button("🔄 Refresh sekarang"):
        st.cache_data.clear()
        st.rerun()

    st.markdown("---")
    st.caption("Sumber data: CoinGecko API\nFear & Greed: alternative.me\nCache: 60 dtk · v3.0")


# ── MAIN ──────────────────────────────────────────────────────────────────────

st.markdown(f"## 📈 Crypto Technical Dashboard — {coin_label}")

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
            <span class="eb-lev-dot" style="background:#3b6d11"></span>
            <span class="eb-lev-key">Target 2</span>
            <div class="eb-lev-right">
              <span class="eb-lev-price">{fmt_price(sig["buy_tp2"])}</span>
              <span class="eb-badge eb-badge-tp-buy">{sig["buy_tp2_pct"]}</span>
            </div>
          </div>
          <div class="eb-lev-row">
            <span class="eb-lev-dot" style="background:#639922"></span>
            <span class="eb-lev-key">Target 1</span>
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
            <span class="eb-lev-key" style="color:#a32d2d">Stop Loss</span>
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
            <span class="eb-lev-key" style="color:#3b6d11">Stop Loss</span>
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
            <span class="eb-lev-key">Target 1</span>
            <div class="eb-lev-right">
              <span class="eb-lev-price">{fmt_price(sig["sell_tp1"])}</span>
              <span class="eb-badge eb-badge-tp-sell">{sig["sell_tp1_pct"]}</span>
            </div>
          </div>
          <div class="eb-lev-row">
            <span class="eb-lev-dot" style="background:#a32d2d"></span>
            <span class="eb-lev-key">Target 2</span>
            <div class="eb-lev-right">
              <span class="eb-lev-price">{fmt_price(sig["sell_tp2"])}</span>
              <span class="eb-badge eb-badge-tp-sell">{sig["sell_tp2_pct"]}</span>
            </div>
          </div>
        </div>'''

    buy_action_cls  = "eb-action-buy"  if sig["buy_strength"]  == "STRONG"   else "eb-action-warn"
    sell_action_cls = "eb-action-sell" if sig["sell_strength"] == "STRONG"   else "eb-action-warn"

    rr_buy_interp  = (f"Profit {sig['buy_rr']}× lebih besar dari risiko"
                      if sig["buy_rr"] >= 1 else "R/R kurang ideal — pertimbangkan ulang")
    rr_sell_interp = (f"Profit {sig['sell_rr']}× lebih besar dari risiko"
                      if sig["sell_rr"] >= 1 else "R/R kurang ideal — pertimbangkan ulang")

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

if auto_refresh:
    time.sleep(60)
    st.cache_data.clear()
    st.rerun()
