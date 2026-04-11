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
    .metric-card {
        background: #f8f9fa;
        border-radius: 8px;
        padding: 12px 16px;
        text-align: center;
    }
    .signal-buy {
        background: #eaf3de;
        border: 1px solid #3b6d11;
        border-radius: 10px;
        padding: 14px;
    }
    .signal-sell {
        background: #fcebeb;
        border: 1px solid #a32d2d;
        border-radius: 10px;
        padding: 14px;
    }
    .sig-title-buy { color: #3b6d11; font-weight: 600; font-size: 13px; }
    .sig-title-sell { color: #a32d2d; font-weight: 600; font-size: 13px; }
    .indicator-box {
        background: #f8f9fa;
        border-radius: 8px;
        padding: 10px 14px;
        margin-bottom: 6px;
    }
    div[data-testid="stMetric"] {
        background: #f8f9fa;
        border-radius: 8px;
        padding: 10px 14px;
    }
    h1 { font-size: 1.4rem !important; }
    h2 { font-size: 1.1rem !important; }
    h3 { font-size: 1rem !important; }
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


@st.cache_data(ttl=60)
def fetch_ohlc(coin_id: str, days: int):
    url = f"{CG_BASE}/coins/{coin_id}/ohlc"
    r = requests.get(url, params={"vs_currency": "usd", "days": days}, timeout=15)
    r.raise_for_status()
    data = r.json()
    df = pd.DataFrame(data, columns=["timestamp", "open", "high", "low", "close"])
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


def calc_ema(series: pd.Series, period: int) -> pd.Series:
    return series.ewm(span=period, adjust=False).mean()


def calc_rsi(series: pd.Series, period: int = 14) -> pd.Series:
    delta = series.diff()
    gain = delta.clip(lower=0).rolling(period).mean()
    loss = -delta.clip(upper=0).rolling(period).mean()
    rs = gain / loss.replace(0, np.nan)
    return 100 - (100 / (1 + rs))


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


def calc_sr_channels(df: pd.DataFrame, channel_pct: float = 0.5):
    highs = df["high"].values
    lows = df["low"].values
    closes = df["close"].values
    n = len(highs)
    highest = np.max(highs[-min(200, n):])
    lowest = np.min(lows[-min(200, n):])
    cwidth = (highest - lowest) * channel_pct / 100
    prd = max(3, n // 20)
    pivots = []
    for i in range(prd, n - prd):
        if highs[i] == np.max(highs[i - prd:i + prd + 1]):
            pivots.append(highs[i])
        if lows[i] == np.min(lows[i - prd:i + prd + 1]):
            pivots.append(lows[i])
    channels = []
    used = set()
    for i, p in enumerate(pivots):
        if i in used:
            continue
        lo = hi = p
        count = 20
        for j, q in enumerate(pivots):
            if j == i or j in used:
                continue
            w = hi - q if q <= hi else q - lo
            if w <= cwidth:
                lo = min(lo, q)
                hi = max(hi, q)
                count += 20
                used.add(j)
        touch = sum(1 for k in range(max(0, n - 100), n)
                    if (highs[k] <= hi and highs[k] >= lo) or
                       (lows[k] <= hi and lows[k] >= lo))
        channels.append({"hi": hi, "lo": lo, "strength": count + touch})
        used.add(i)
    channels.sort(key=lambda x: -x["strength"])
    return channels[:8]


def calc_fibonacci(df: pd.DataFrame, lookback: int = 60):
    sl = df.tail(min(lookback, len(df)))
    swing_h = sl["high"].max()
    swing_l = sl["low"].min()
    diff = swing_h - swing_l
    ratios = [0, 0.236, 0.382, 0.5, 0.618, 0.786, 1.0]
    colors = ["#e24b4a", "#d85a30", "#ef9f27", "#639922", "#185fa5", "#534ab7", "#3b6d11"]
    return [{"ratio": r, "price": swing_h - diff * r,
             "label": f"{r*100:.1f}%", "color": colors[i]}
            for i, r in enumerate(ratios)]


def get_signals(df: pd.DataFrame, rsi, macd_hist, ema20, ema50, sr_channels):
    price = df["close"].iloc[-1]
    rsi_val = rsi.iloc[-1] if not pd.isna(rsi.iloc[-1]) else 50
    hist_val = macd_hist.iloc[-1] if not pd.isna(macd_hist.iloc[-1]) else 0
    prev_hist = macd_hist.iloc[-2] if len(macd_hist) > 1 else 0
    e20 = ema20.iloc[-1]
    e50 = ema50.iloc[-1]

    buy_score, sell_score = 0, 0
    buy_reasons, sell_reasons = [], []

    if rsi_val < 35:
        buy_score += 2; buy_reasons.append("RSI oversold")
    elif rsi_val < 45:
        buy_score += 1; buy_reasons.append("RSI low")
    if rsi_val > 65:
        sell_score += 2; sell_reasons.append("RSI overbought")
    elif rsi_val > 55:
        sell_score += 1; sell_reasons.append("RSI high")

    if hist_val > 0 and prev_hist <= 0:
        buy_score += 2; buy_reasons.append("MACD cross up")
    elif hist_val > 0:
        buy_score += 1
    if hist_val < 0 and prev_hist >= 0:
        sell_score += 2; sell_reasons.append("MACD cross down")
    elif hist_val < 0:
        sell_score += 1

    if e20 > e50:
        buy_score += 1; buy_reasons.append("EMA bullish")
    else:
        sell_score += 1; sell_reasons.append("EMA bearish")

    for ch in sr_channels:
        if abs(price - ch["lo"]) / price < 0.008:
            buy_score += 2; buy_reasons.append("At support"); break
        if abs(price - ch["hi"]) / price < 0.008:
            sell_score += 2; sell_reasons.append("At resistance"); break

    closes = df["close"].values
    atr_vals = [abs(closes[i] - closes[i-1]) for i in range(max(1, len(closes)-14), len(closes))]
    atr = np.mean(atr_vals) if atr_vals else price * 0.01

    buy_entry = round(price * 0.999, 2 if price < 100 else 0)
    buy_tp1 = round(buy_entry + atr * 2, 2 if price < 100 else 0)
    buy_tp2 = round(buy_entry + atr * 3.5, 2 if price < 100 else 0)
    buy_sl = round(buy_entry - atr * 1.2, 2 if price < 100 else 0)
    buy_rr = round((buy_tp1 - buy_entry) / (buy_entry - buy_sl), 2) if (buy_entry - buy_sl) != 0 else 0

    sell_entry = round(price * 1.001, 2 if price < 100 else 0)
    sell_tp1 = round(sell_entry - atr * 2, 2 if price < 100 else 0)
    sell_tp2 = round(sell_entry - atr * 3.5, 2 if price < 100 else 0)
    sell_sl = round(sell_entry + atr * 1.2, 2 if price < 100 else 0)
    sell_rr = round((sell_entry - sell_tp1) / (sell_sl - sell_entry), 2) if (sell_sl - sell_entry) != 0 else 0

    bs = "STRONG" if buy_score >= 5 else "MODERATE" if buy_score >= 3 else "WEAK"
    ss = "STRONG" if sell_score >= 5 else "MODERATE" if sell_score >= 3 else "WEAK"

    return {
        "price": price, "rsi": rsi_val, "hist": hist_val,
        "e20": e20, "e50": e50, "buy_score": buy_score, "sell_score": sell_score,
        "buy_strength": bs, "sell_strength": ss,
        "buy_reason": " + ".join(buy_reasons[:2]) or "Mixed signals",
        "sell_reason": " + ".join(sell_reasons[:2]) or "Mixed signals",
        "buy_entry": buy_entry, "buy_tp1": buy_tp1, "buy_tp2": buy_tp2,
        "buy_sl": buy_sl, "buy_rr": buy_rr,
        "sell_entry": sell_entry, "sell_tp1": sell_tp1, "sell_tp2": sell_tp2,
        "sell_sl": sell_sl, "sell_rr": sell_rr,
    }


def build_main_chart(df, ema20, ema50, sr_channels, fib_levels, rsi, macd_hist):
    fig = make_subplots(
        rows=3, cols=1,
        shared_xaxes=True,
        row_heights=[0.60, 0.20, 0.20],
        vertical_spacing=0.03,
        subplot_titles=("Price + S/R + Fibonacci", "RSI (14)", "MACD (12,26,9)")
    )

    price = df["close"].iloc[-1]

    for fib in fib_levels:
        fig.add_hline(
            y=fib["price"], line_color=fib["color"],
            line_dash="dot", line_width=0.8,
            annotation_text=f"Fib {fib['label']} ${fib['price']:,.2f}",
            annotation_position="right",
            annotation_font_size=9,
            annotation_font_color=fib["color"],
            row=1, col=1
        )

    for i, ch in enumerate(sr_channels[:6]):
        mid = (ch["hi"] + ch["lo"]) / 2
        is_res = ch["hi"] > price and ch["lo"] > price
        is_sup = ch["hi"] < price
        color = "rgba(163,45,45,0.35)" if is_res else "rgba(59,109,17,0.35)" if is_sup else "rgba(136,135,128,0.3)"
        label = "R" if is_res else "S" if is_sup else "IN"
        fig.add_hrect(
            y0=ch["lo"], y1=ch["hi"],
            fillcolor=color, line_color=color.replace("0.35", "0.7").replace("0.3", "0.5"),
            line_width=0.8,
            annotation_text=f"{label}{i+1}",
            annotation_position="right",
            annotation_font_size=8,
            row=1, col=1
        )

    fig.add_trace(go.Scatter(
        x=df["time"], y=df["close"],
        name="Price", line=dict(color="#185fa5", width=2),
        hovertemplate="%{x}<br>$%{y:,.4f}<extra></extra>"
    ), row=1, col=1)

    fig.add_trace(go.Scatter(
        x=df["time"], y=ema20,
        name="EMA 20", line=dict(color="#ef9f27", width=1.2),
    ), row=1, col=1)

    fig.add_trace(go.Scatter(
        x=df["time"], y=ema50,
        name="EMA 50", line=dict(color="#d85a30", width=1, dash="dash"),
    ), row=1, col=1)

    buy_mask = (rsi < 38) | ((macd_hist > 0) & (macd_hist.shift(1) <= 0))
    sell_mask = (rsi > 62) | ((macd_hist < 0) & (macd_hist.shift(1) >= 0))

    fig.add_trace(go.Scatter(
        x=df["time"][buy_mask], y=df["close"][buy_mask],
        mode="markers", name="Buy Signal",
        marker=dict(symbol="triangle-up", size=10, color="#3b6d11"),
    ), row=1, col=1)

    fig.add_trace(go.Scatter(
        x=df["time"][sell_mask], y=df["close"][sell_mask],
        mode="markers", name="Sell Signal",
        marker=dict(symbol="triangle-down", size=10, color="#a32d2d"),
    ), row=1, col=1)

    fig.add_trace(go.Scatter(
        x=df["time"], y=rsi,
        name="RSI", line=dict(color="#534ab7", width=1.5),
        hovertemplate="RSI: %{y:.1f}<extra></extra>"
    ), row=2, col=1)
    fig.add_hline(y=70, line_color="rgba(163,45,45,0.5)", line_dash="dot", line_width=1, row=2, col=1)
    fig.add_hline(y=30, line_color="rgba(59,109,17,0.5)", line_dash="dot", line_width=1, row=2, col=1)
    fig.add_hrect(y0=70, y1=100, fillcolor="rgba(163,45,45,0.06)", line_width=0, row=2, col=1)
    fig.add_hrect(y0=0, y1=30, fillcolor="rgba(59,109,17,0.06)", line_width=0, row=2, col=1)

    colors_hist = ["rgba(59,109,17,0.7)" if v >= 0 else "rgba(163,45,45,0.7)"
                   for v in macd_hist.fillna(0)]
    fig.add_trace(go.Bar(
        x=df["time"], y=macd_hist,
        name="MACD Hist", marker_color=colors_hist,
    ), row=3, col=1)

    macd_line, signal_line, _ = calc_macd(df["close"])
    fig.add_trace(go.Scatter(
        x=df["time"], y=macd_line,
        name="MACD", line=dict(color="#185fa5", width=1),
    ), row=3, col=1)
    fig.add_trace(go.Scatter(
        x=df["time"], y=signal_line,
        name="Signal", line=dict(color="#ef9f27", width=1, dash="dot"),
    ), row=3, col=1)

    fig.update_layout(
        height=680,
        margin=dict(l=10, r=120, t=30, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(248,249,250,0.5)",
        legend=dict(
            orientation="h", yanchor="bottom", y=1.02,
            xanchor="left", x=0, font=dict(size=10)
        ),
        hovermode="x unified",
        xaxis3=dict(showticklabels=True),
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
        colors.append(
            "rgba(163,45,45,0.75)" if is_res else
            "rgba(59,109,17,0.75)" if is_sup else
            "rgba(136,135,128,0.65)"
        )
    fig = go.Figure(go.Bar(
        x=strengths, y=labels,
        orientation="h",
        marker_color=colors,
        text=[f"  {s}" for s in strengths],
        textposition="outside",
        textfont=dict(size=10),
    ))
    fig.update_layout(
        height=220,
        margin=dict(l=10, r=40, t=10, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(248,249,250,0.5)",
        xaxis=dict(title="Strength", tickfont=dict(size=10), gridcolor="rgba(128,128,128,0.1)"),
        yaxis=dict(tickfont=dict(size=10), gridcolor="rgba(0,0,0,0)"),
    )
    return fig


def fmt_price(p):
    if p is None:
        return "—"
    if p >= 10000:
        return f"${p:,.0f}"
    if p >= 100:
        return f"${p:,.2f}"
    if p >= 1:
        return f"${p:.4f}"
    return f"${p:.6f}"


def fmt_large(n):
    if n >= 1e12:
        return f"${n/1e12:.2f}T"
    if n >= 1e9:
        return f"${n/1e9:.2f}B"
    if n >= 1e6:
        return f"${n/1e6:.2f}M"
    return f"${n:,.0f}"


# ── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ Settings")
    coin_label = st.selectbox("Pair", list(COINS.keys()), index=0)
    coin_id = COINS[coin_label]
    days_label = st.selectbox("Periode", list(DAYS_MAP.keys()), index=0)
    days = DAYS_MAP[days_label]

    st.markdown("---")
    st.markdown("**Indikator aktif**")
    show_ema = st.checkbox("EMA 20 / 50", value=True)
    show_fib = st.checkbox("Fibonacci Retracement", value=True)
    show_sr = st.checkbox("Support / Resistance", value=True)
    show_signals = st.checkbox("Sinyal Beli / Jual", value=True)

    st.markdown("---")
    auto_refresh = st.checkbox("Auto-refresh (60 dtk)", value=False)
    if st.button("🔄 Refresh sekarang"):
        st.cache_data.clear()
        st.rerun()

    st.markdown("---")
    st.caption("Data: CoinGecko Free API\nAuto-refresh: 60 detik\nv2.0 — Streamlit Cloud")

# ── MAIN ─────────────────────────────────────────────────────────────────────
st.markdown(f"## 📈 Crypto Technical Dashboard — {coin_label}")

with st.spinner("Mengambil data dari CoinGecko..."):
    try:
        df = fetch_ohlc(coin_id, days)
        market = fetch_market(coin_id)
    except requests.exceptions.HTTPError as e:
        if "429" in str(e):
            st.warning("⚠️ CoinGecko rate limit tercapai. Tunggu 60 detik lalu refresh.")
        else:
            st.error(f"Error API: {e}")
        st.stop()
    except Exception as e:
        st.error(f"Gagal mengambil data: {e}")
        st.stop()

md = market.get("market_data", {})
cur_price = md.get("current_price", {}).get("usd", df["close"].iloc[-1])
pct_24h = md.get("price_change_percentage_24h", 0) or 0
high_24h = md.get("high_24h", {}).get("usd", df["high"].max())
low_24h = md.get("low_24h", {}).get("usd", df["low"].min())
mkt_cap = md.get("market_cap", {}).get("usd", 0)
vol_24h = md.get("total_volume", {}).get("usd", 0)

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Harga", fmt_price(cur_price), f"{pct_24h:+.2f}%")
c2.metric("24h High", fmt_price(high_24h))
c3.metric("24h Low", fmt_price(low_24h))
c4.metric("Market Cap", fmt_large(mkt_cap))
c5.metric("Volume 24h", fmt_large(vol_24h))

st.markdown("---")

ema20 = calc_ema(df["close"], 20)
ema50 = calc_ema(df["close"], min(50, max(10, len(df) // 2)))
rsi = calc_rsi(df["close"])
_, _, macd_hist = calc_macd(df["close"])
sr_channels = calc_sr_channels(df) if show_sr else []
fib_levels = calc_fibonacci(df) if show_fib else []
sig = get_signals(df, rsi, macd_hist, ema20, ema50, sr_channels)

fig = build_main_chart(
    df,
    ema20 if show_ema else pd.Series([None]*len(df)),
    ema50 if show_ema else pd.Series([None]*len(df)),
    sr_channels if show_sr else [],
    fib_levels if show_fib else [],
    rsi, macd_hist
)
st.plotly_chart(fig, use_container_width=True)

col_sr, col_fib = st.columns([1, 1])

with col_sr:
    st.markdown("##### Support / Resistance Channels")
    if sr_channels:
        st.plotly_chart(build_sr_chart(sr_channels, cur_price), use_container_width=True)
        sr_data = []
        for i, ch in enumerate(sr_channels[:6]):
            is_res = ch["hi"] > cur_price and ch["lo"] > cur_price
            is_sup = ch["hi"] < cur_price
            t = "Resistance" if is_res else "Support" if is_sup else "Inside"
            sr_data.append({
                "Tipe": t,
                "Upper": fmt_price(ch["hi"]),
                "Lower": fmt_price(ch["lo"]),
                "Mid": fmt_price((ch["hi"]+ch["lo"])/2),
                "Strength": ch["strength"]
            })
        st.dataframe(pd.DataFrame(sr_data), use_container_width=True, hide_index=True)

with col_fib:
    st.markdown("##### Fibonacci Retracement")
    if fib_levels:
        fib_data = []
        for f in fib_levels:
            dist = (cur_price - f["price"]) / cur_price * 100
            zone = "AT LEVEL" if abs(dist) < 0.5 else ("above" if dist > 0 else "below")
            fib_data.append({
                "Level": f["label"],
                "Harga": fmt_price(f["price"]),
                "Jarak": f"{dist:+.2f}%",
                "Posisi": zone
            })
        df_fib = pd.DataFrame(fib_data)
        st.dataframe(df_fib, use_container_width=True, hide_index=True)

st.markdown("---")

if show_signals:
    st.markdown("##### Sinyal Beli & Jual")
    sc1, sc2 = st.columns(2)

    strength_color_buy = {"STRONG": "🟢", "MODERATE": "🟡", "WEAK": "⚪"}
    strength_color_sell = {"STRONG": "🔴", "MODERATE": "🟠", "WEAK": "⚪"}

    with sc1:
        st.markdown(f"""
        <div class="signal-buy">
          <div class="sig-title-buy">BUY SIGNAL &nbsp; {strength_color_buy[sig['buy_strength']]} {sig['buy_strength']}</div>
          <div style="font-size:22px;font-weight:600;margin:6px 0">{fmt_price(sig['buy_entry'])}</div>
          <div style="font-size:12px;color:#5f5e5a;margin-bottom:8px">{sig['buy_reason']}</div>
          <table style="width:100%;font-size:12px;border-collapse:collapse">
            <tr><td style="color:#888;padding:3px 0;border-top:1px solid #c0dd97">Target 1</td><td style="text-align:right;font-weight:500">{fmt_price(sig['buy_tp1'])}</td></tr>
            <tr><td style="color:#888;padding:3px 0;border-top:1px solid #c0dd97">Target 2</td><td style="text-align:right;font-weight:500">{fmt_price(sig['buy_tp2'])}</td></tr>
            <tr><td style="color:#888;padding:3px 0;border-top:1px solid #c0dd97">Stop Loss</td><td style="text-align:right;font-weight:500">{fmt_price(sig['buy_sl'])}</td></tr>
            <tr><td style="color:#888;padding:3px 0;border-top:1px solid #c0dd97">R/R Ratio</td><td style="text-align:right;font-weight:500">{sig['buy_rr']}:1</td></tr>
          </table>
        </div>
        """, unsafe_allow_html=True)

    with sc2:
        st.markdown(f"""
        <div class="signal-sell">
          <div class="sig-title-sell">SELL SIGNAL &nbsp; {strength_color_sell[sig['sell_strength']]} {sig['sell_strength']}</div>
          <div style="font-size:22px;font-weight:600;margin:6px 0">{fmt_price(sig['sell_entry'])}</div>
          <div style="font-size:12px;color:#5f5e5a;margin-bottom:8px">{sig['sell_reason']}</div>
          <table style="width:100%;font-size:12px;border-collapse:collapse">
            <tr><td style="color:#888;padding:3px 0;border-top:1px solid #f7c1c1">Target 1</td><td style="text-align:right;font-weight:500">{fmt_price(sig['sell_tp1'])}</td></tr>
            <tr><td style="color:#888;padding:3px 0;border-top:1px solid #f7c1c1">Target 2</td><td style="text-align:right;font-weight:500">{fmt_price(sig['sell_tp2'])}</td></tr>
            <tr><td style="color:#888;padding:3px 0;border-top:1px solid #f7c1c1">Stop Loss</td><td style="text-align:right;font-weight:500">{fmt_price(sig['sell_sl'])}</td></tr>
            <tr><td style="color:#888;padding:3px 0;border-top:1px solid #f7c1c1">R/R Ratio</td><td style="text-align:right;font-weight:500">{sig['sell_rr']}:1</td></tr>
          </table>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

st.markdown("##### Ringkasan Indikator")
i1, i2, i3, i4, i5, i6 = st.columns(6)

rsi_val = round(sig["rsi"], 1)
rsi_status = "Oversold" if rsi_val < 35 else "Overbought" if rsi_val > 65 else "Neutral"
rsi_delta = "🟢" if rsi_val < 35 else "🔴" if rsi_val > 65 else "⚪"
i1.metric("RSI (14)", f"{rsi_val}", rsi_status)

hist_v = round(sig["hist"], 2)
macd_status = "Bullish" if hist_v > 0 else "Bearish"
i2.metric("MACD Hist", f"{hist_v:+}", macd_status)

ema_gap = round((sig["e20"] - sig["e50"]) / sig["e50"] * 100, 3) if sig["e50"] else 0
ema_status = "Golden cross" if ema_gap > 0 else "Death cross"
i3.metric("EMA 20/50", f"{ema_gap:+.2f}%", ema_status)

sr_pos = "Free zone"
for ch in sr_channels:
    if cur_price >= ch["lo"] and cur_price <= ch["hi"]:
        sr_pos = "Inside channel"; break
    if abs(cur_price - ch["lo"]) / cur_price < 0.008:
        sr_pos = "Near support"; break
    if abs(cur_price - ch["hi"]) / cur_price < 0.008:
        sr_pos = "Near resistance"; break
i4.metric("S/R Position", sr_pos)

near_fib = min(fib_levels, key=lambda f: abs(cur_price - f["price"])) if fib_levels else None
fib_label = near_fib["label"] if near_fib else "—"
fib_dist = round((cur_price - near_fib["price"]) / cur_price * 100, 2) if near_fib else 0
i5.metric("Fib Nearest", fib_label, f"{fib_dist:+.2f}%")

total = sig["buy_score"] - sig["sell_score"]
trend = "Bullish" if total > 2 else "Bearish" if total < -2 else "Sideways"
i6.metric("Trend Bias", trend, f"score {total:+}")

st.markdown("---")
st.caption(
    f"Sumber: CoinGecko API · Terakhir diperbarui: {datetime.now().strftime('%H:%M:%S')} · "
    f"Data OHLC: {len(df)} candle · "
    "Disclaimer: bukan saran investasi."
)

if auto_refresh:
    time.sleep(60)
    st.cache_data.clear()
    st.rerun()
