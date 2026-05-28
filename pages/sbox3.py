import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import io
import time

# ─── PAGE CONFIG ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="S-Box Comparator · GF(2⁸)",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://api.fontshare.com/v2/css?f[]=satoshi@300,400,500,700,900&display=swap');
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&display=swap');

html, body, [class*="css"] { font-family: 'Satoshi', sans-serif !important; }
.stApp { background: linear-gradient(135deg, #080c16 0%, #0a0e1a 40%, #0c1220 100%); min-height: 100vh; }
#MainMenu, footer, header { visibility: hidden; }

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d1120 0%, #0a0e1a 100%) !important;
    border-right: 1px solid #1a2030 !important;
}
section[data-testid="stSidebar"] * { color: #c8d4e0 !important; }
section[data-testid="stSidebar"] .stSelectbox label,
section[data-testid="stSidebar"] .stMultiSelect label,
section[data-testid="stSidebar"] .stCheckbox label { color: #7ab8c4 !important; font-size:0.82rem !important; font-weight:600 !important; letter-spacing:0.05em !important; }

.page-header {
    padding: 2rem 0 1.5rem;
    border-bottom: 1px solid #1a2030;
    margin-bottom: 2rem;
}
.page-title {
    font-size: clamp(1.8rem, 3vw, 2.8rem);
    font-weight: 900;
    background: linear-gradient(135deg, #ffffff 0%, #a8d8dc 40%, #4f98a3 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: -0.02em;
    line-height: 1.1;
}
.page-subtitle {
    font-size: 0.92rem;
    color: #4a6a7a;
    margin-top: 0.4rem;
    font-family: 'JetBrains Mono', monospace;
}

/* Metric cards */
.metric-row { display: flex; gap: 1rem; margin-bottom: 1.5rem; flex-wrap: wrap; }
.metric-card {
    flex: 1; min-width: 140px;
    background: linear-gradient(145deg, #111520, #161b2e);
    border: 1px solid #1e2540;
    border-radius: 14px;
    padding: 1.1rem 1.3rem;
    position: relative; overflow: hidden;
}
.metric-card::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px;
    border-radius: 14px 14px 0 0;
}
.mc-teal::before   { background: linear-gradient(90deg, #4f98a3, transparent); }
.mc-purple::before { background: linear-gradient(90deg, #9b6fd4, transparent); }
.mc-gold::before   { background: linear-gradient(90deg, #d4a017, transparent); }
.mc-green::before  { background: linear-gradient(90deg, #6daa45, transparent); }
.mc-red::before    { background: linear-gradient(90deg, #dd6974, transparent); }
.metric-label { font-size: 0.68rem; color: #4a6a7a; text-transform: uppercase; letter-spacing: 0.1em; font-weight: 600; margin-bottom: 0.3rem; font-family: 'JetBrains Mono', monospace; }
.metric-value { font-size: 1.6rem; font-weight: 800; color: #e2e8f0; line-height: 1; font-family: 'JetBrains Mono', monospace; }
.metric-sub { font-size: 0.72rem; color: #3a4a5a; margin-top: 0.3rem; }

/* Section headers */
.section-hdr {
    font-size: 0.72rem;
    color: #4f98a3;
    font-family: 'JetBrains Mono', monospace;
    font-weight: 700;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin: 2rem 0 1rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid #1a2030;
    display: flex; align-items: center; gap: 0.6rem;
}

/* Rank badge */
.rank-badge {
    display: inline-flex; align-items: center; justify-content: center;
    width: 28px; height: 28px; border-radius: 50%;
    font-size: 0.72rem; font-weight: 800; font-family: 'JetBrains Mono', monospace;
}
.rank-1 { background: rgba(212,160,23,0.15); color: #d4a017; border: 1px solid rgba(212,160,23,0.3); }
.rank-2 { background: rgba(180,180,180,0.1); color: #a8b8c4; border: 1px solid rgba(180,180,180,0.2); }
.rank-3 { background: rgba(180,100,60,0.1); color: #c87040; border: 1px solid rgba(180,100,60,0.2); }
.rank-n { background: rgba(30,37,64,0.5); color: #4a6a7a; border: 1px solid #1e2540; }

/* Progress bar */
.prog-wrap { background: #111520; border-radius: 999px; height: 6px; overflow: hidden; margin-top: 0.3rem; }
.prog-fill { height: 100%; border-radius: 999px; transition: width 0.5s ease; }

/* AES badge */
.aes-badge {
    display: inline-flex; align-items: center; gap: 0.3rem;
    background: rgba(1,105,111,0.12); border: 1px solid rgba(79,152,163,0.25);
    border-radius: 999px; padding: 0.15rem 0.6rem;
    font-size: 0.68rem; color: #4f98a3; font-weight: 700;
    font-family: 'JetBrains Mono', monospace; letter-spacing: 0.05em;
}

/* Score pill */
.score-pill {
    display: inline-block;
    padding: 0.2rem 0.7rem; border-radius: 999px;
    font-size: 0.72rem; font-weight: 700;
    font-family: 'JetBrains Mono', monospace;
}
.score-high { background: rgba(109,170,69,0.12); color: #6daa45; border: 1px solid rgba(109,170,69,0.2); }
.score-mid  { background: rgba(212,160,23,0.12); color: #d4a017; border: 1px solid rgba(212,160,23,0.2); }
.score-low  { background: rgba(221,105,116,0.12); color: #dd6974; border: 1px solid rgba(221,105,116,0.2); }
</style>
""", unsafe_allow_html=True)

# ─── GF(2^8) CORE ──────────────────────────────────────────────────────────────
def gf_mul(a, b, poly):
    result = 0
    for _ in range(8):
        if b & 1:
            result ^= a
        hi = a & 0x80
        a = (a << 1) & 0xFF
        if hi:
            a ^= (poly & 0xFF)
        b >>= 1
    return result

def build_inverse_table(poly):
    inv = [0] * 256
    for i in range(1, 256):
        for j in range(1, 256):
            if gf_mul(i, j, poly) == 1:
                inv[i] = j
                break
    return inv

def affine_transform(b, const):
    result = 0
    for i in range(8):
        bit = ((b >> i) & 1) ^ ((b >> ((i+4)%8)) & 1) ^ ((b >> ((i+5)%8)) & 1) ^ \
              ((b >> ((i+6)%8)) & 1) ^ ((b >> ((i+7)%8)) & 1) ^ ((const >> i) & 1)
        result |= (bit << i)
    return result

def build_sbox(poly, const=0x63):
    inv = build_inverse_table(poly)
    return [affine_transform(inv[i], const) for i in range(256)]

# ─── METRICS ───────────────────────────────────────────────────────────────────
def compute_nl(sbox):
    n = 256
    nls = []
    for b in range(1, 256):
        min_wht = n
        for a in range(256):
            wht = sum(1 for x in range(n) if bin(sbox[x] & b).count('1') % 2 != bin(x & a).count('1') % 2)
            bias = abs(wht - n//2)
            if bias < min_wht: min_wht = bias
        nls.append(n//2 - min_wht)
    return min(nls)

def compute_sac(sbox):
    n, total = 8, 0
    for i in range(n):
        for j in range(n):
            cnt = sum(1 for x in range(256) if ((sbox[x] >> j) & 1) != ((sbox[x ^ (1<<i)] >> j) & 1))
            total += cnt / 256
    return total / (n * n)

def compute_bic_nl(sbox):
    nls = []
    for i in range(8):
        for j in range(i+1, 8):
            combined = [((sbox[x] >> i) & 1) ^ ((sbox[x] >> j) & 1) for x in range(256)]
            nl = 128
            for a in range(256):
                wht = sum(1 for x in range(256) if combined[x] != bin(x & a).count('1') % 2)
                nl = min(nl, min(wht, 256 - wht))
            nls.append(nl)
    return sum(nls) / len(nls)

def compute_bic_sac(sbox):
    vals = []
    for k in range(8):
        for i in range(8):
            for j in range(i+1, 8):
                cnt = sum(1 for x in range(256)
                    if (((sbox[x] >> i) & 1) ^ ((sbox[x] >> j) & 1)) !=
                       (((sbox[x ^ (1<<k)] >> i) & 1) ^ ((sbox[x ^ (1<<k)] >> j) & 1)))
                vals.append(cnt / 256)
    return sum(vals) / len(vals)

def compute_lap(sbox):
    best = 0
    for a in range(1, 256):
        for b in range(1, 256):
            cnt = sum(1 for x in range(256) if bin(x & a).count('1') % 2 == bin(sbox[x] & b).count('1') % 2)
            bias = abs(cnt - 128) / 256
            if bias > best: best = bias
    return best ** 2

def compute_dap(sbox):
    best = 0
    for dx in range(1, 256):
        counts = {}
        for x in range(256):
            dy = sbox[x] ^ sbox[x ^ dx]
            counts[dy] = counts.get(dy, 0) + 1
        m = max(counts.values())
        if m > best: best = m
    return best / 256

# ─── 30 IRREDUCIBLE POLYNOMIALS ────────────────────────────────────────────────
POLYS = {
    "0x11B (AES)": 0x11B, "0x11D": 0x11D, "0x12B": 0x12B, "0x12D": 0x12D,
    "0x139": 0x139, "0x13F": 0x13F, "0x14D": 0x14D, "0x15F": 0x15F,
    "0x163": 0x163, "0x165": 0x165, "0x169": 0x169, "0x171": 0x171,
    "0x177": 0x177, "0x17B": 0x17B, "0x187": 0x187, "0x18B": 0x18B,
    "0x18D": 0x18D, "0x19F": 0x19F, "0x1A3": 0x1A3, "0x1A9": 0x1A9,
    "0x1B1": 0x1B1, "0x1BD": 0x1BD, "0x1C3": 0x1C3, "0x1CF": 0x1CF,
    "0x1D7": 0x1D7, "0x1DD": 0x1DD, "0x1E7": 0x1E7, "0x1F3": 0x1F3,
    "0x1F5": 0x1F5, "0x1F9": 0x1F9,
}

AES_REF = {"NL": 112, "SAC": 0.504, "BIC-NL": 112.0, "BIC-SAC": 0.5, "LAP": 0.0625, "DAP": 0.015625}

# ─── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 📊 Komparasi S-Box")
    st.markdown("---")

    st.markdown("**Pilih Polinomial**")
    select_mode = st.radio("Mode", ["Semua 30 Poly", "Pilih Manual"], label_visibility="collapsed")

    if select_mode == "Pilih Manual":
        selected_keys = st.multiselect("Pilih poly:", list(POLYS.keys()), default=list(POLYS.keys())[:6])
    else:
        selected_keys = list(POLYS.keys())

    st.markdown("---")
    st.markdown("**Konstanta Affine**")
    const_hex = st.selectbox("Konstanta:", ["0x63 (AES)", "0x00", "0x1F", "0x52", "0xAB", "Custom"])
    if const_hex == "Custom":
        const_val = st.number_input("Nilai hex (0-255):", min_value=0, max_value=255, value=0x63)
    else:
        const_val = int(const_hex.split()[0], 16)

    st.markdown("---")
    st.markdown("**Tampilan**")
    sort_by = st.selectbox("Urutkan by:", ["NL", "SAC", "BIC-NL", "BIC-SAC", "LAP", "DAP", "Score"])
    show_heatmap = st.checkbox("Heatmap komparatif", value=True)
    show_radar = st.checkbox("Radar chart top-5", value=True)
    show_detail = st.checkbox("Detail per poly", value=False)

    st.markdown("---")
    run_btn = st.button("🚀 Jalankan Komparasi", use_container_width=True, type="primary")

    st.markdown("---")
    st.markdown("""
    <div style="text-align:center; font-size:0.82rem; padding: 0.6rem; background: rgba(1,105,111,0.05); border-radius: 8px; border: 1px solid rgba(79,152,163,0.2);">
        <div style="margin-bottom: 0.4rem;">
            <a href="./" target="_self" style="color:#a8d8dc; text-decoration:none; font-weight:600; transition:color 0.2s;">🏠 Home</a> 
        </div>
        <div>
            <a href="sbox1" target="_self" style="color:#a8d8dc; text-decoration:none; font-weight:600; transition:color 0.2s;">Konstruksi</a> 
            <span style="color:#2a2d3e; margin: 0 0.3rem;">|</span> 
            <a href="sbox2" target="_self" style="color:#a8d8dc; text-decoration:none; font-weight:600; transition:color 0.2s;">Evaluasi</a> 
            <span style="color:#2a2d3e; margin: 0 0.3rem;">|</span> 
            <a href="sbox3" target="_self" style="color:#4f98a3; text-decoration:none; font-weight:700;">Komparasi</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ─── PAGE HEADER ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="page-header">
    <div class="page-title"><span style="-webkit-text-fill-color: initial; background: none;">📊</span> Analisis Komparatif S-Box</div>
    <div class="page-subtitle">Batch compute · 30 polinomial irreducible GF(2⁸) · 6 parameter kriptografis</div>
</div>
""", unsafe_allow_html=True)

# ─── MAIN LOGIC ────────────────────────────────────────────────────────────────
if "results_df" not in st.session_state:
    st.session_state.results_df = None

if run_btn:
    if not selected_keys:
        st.warning("Pilih minimal 1 polinomial.")
        st.stop()

    # Progress
    prog_bar = st.progress(0, text="Mempersiapkan...")
    status = st.empty()
    results = []
    
    start_time = time.time()
    
    def fmt_time(sec):
        return f"{sec:.1f} detik" if sec < 60 else f"{int(sec//60)}m {sec%60:.0f}s"

    for idx, key in enumerate(selected_keys):
        poly = POLYS[key]
        
        elapsed = time.time() - start_time
        if idx > 0:
            avg_time = elapsed / idx
            etr = avg_time * (len(selected_keys) - idx)
            time_str = f"| Estimasi sisa waktu: {fmt_time(etr)}"
        else:
            time_str = ""
            
        status.markdown(f"<small style='color:#a8d8dc'>⚙️ Menghitung **{key}** ({idx+1}/{len(selected_keys)}) {time_str}</small>", unsafe_allow_html=True)
        prog_bar.progress((idx) / len(selected_keys), text=f"Computing {key}...")

        sbox = build_sbox(poly, const_val)
        nl   = compute_nl(sbox)
        sac  = compute_sac(sbox)
        bicnl = compute_bic_nl(sbox)
        bicsac = compute_bic_sac(sbox)
        lap  = compute_lap(sbox)
        dap  = compute_dap(sbox)

        # Composite score (higher=better, normalized vs AES)
        nl_score    = min(nl / 112, 1.0)
        sac_score   = 1 - abs(sac - 0.5) * 4
        bic_score   = min(bicnl / 112, 1.0)
        bicsac_score = 1 - abs(bicsac - 0.5) * 4
        lap_score   = 1 - min(lap / 0.0625, 1.0)
        dap_score   = 1 - min(dap / 0.015625, 1.0)
        score = round((nl_score + sac_score + bic_score + bicsac_score + lap_score + dap_score) / 6 * 100, 2)

        is_aes = "✓" if key == "0x11B (AES)" else ""
        results.append({
            "Poly": key, "Hex": hex(poly), "AES": is_aes,
            "NL": nl, "SAC": round(sac, 4),
            "BIC-NL": round(bicnl, 2), "BIC-SAC": round(bicsac, 4),
            "LAP": round(lap, 6), "DAP": round(dap, 6),
            "Score": score
        })

    total_time = time.time() - start_time
    prog_bar.progress(1.0, text=f"✅ Selesai dalam {fmt_time(total_time)}!")
    status.empty()
    time.sleep(0.5)
    prog_bar.empty()

    df = pd.DataFrame(results)
    # Sort
    ascending = sort_by in ["LAP", "DAP"]
    if sort_by == "Score":
        df = df.sort_values("Score", ascending=False)
    else:
        df = df.sort_values(sort_by, ascending=ascending)
    df.insert(0, "Rank", range(1, len(df)+1))
    st.session_state.results_df = df
    st.session_state.const_val = const_val

# ─── DISPLAY RESULTS ───────────────────────────────────────────────────────────
if st.session_state.results_df is not None:
    df = st.session_state.results_df

    # ── Summary metrics
    best_nl  = df["NL"].max()
    best_sac = df.loc[(df["SAC"] - 0.5).abs().idxmin(), "SAC"]
    best_lap = df["LAP"].min()
    best_dap = df["DAP"].min()
    best_score = df["Score"].max()
    top_poly = df.iloc[0]["Poly"]

    st.markdown('<div class="metric-row">', unsafe_allow_html=True)
    c1,c2,c3,c4,c5 = st.columns(5)
    with c1:
        st.markdown(f'<div class="metric-card mc-teal"><div class="metric-label">Best NL</div><div class="metric-value">{best_nl}</div><div class="metric-sub">AES ref: 112</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="metric-card mc-purple"><div class="metric-label">Best SAC</div><div class="metric-value">{best_sac:.4f}</div><div class="metric-sub">ideal: 0.5000</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="metric-card mc-gold"><div class="metric-label">Best LAP</div><div class="metric-value">{best_lap:.5f}</div><div class="metric-sub">AES: 0.06250</div></div>', unsafe_allow_html=True)
    with c4:
        st.markdown(f'<div class="metric-card mc-green"><div class="metric-label">Best DAP</div><div class="metric-value">{best_dap:.5f}</div><div class="metric-sub">AES: 0.01563</div></div>', unsafe_allow_html=True)
    with c5:
        st.markdown(f'<div class="metric-card mc-red"><div class="metric-label">Top Poly</div><div class="metric-value" style="font-size:1rem">{top_poly}</div><div class="metric-sub">Score: {best_score:.1f}/100</div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Ranking Table
    st.markdown('<div class="section-hdr">🏆 Ranking Table</div>', unsafe_allow_html=True)

    def style_table(df_in):
        def color_nl(val):
            if val >= 112: return 'color: #6daa45; font-weight:700'
            elif val >= 100: return 'color: #d4a017'
            return 'color: #dd6974'
        def color_lap(val):
            if val <= 0.0625: return 'color: #6daa45; font-weight:700'
            elif val <= 0.1: return 'color: #d4a017'
            return 'color: #dd6974'
        def color_dap(val):
            if val <= 0.015625: return 'color: #6daa45; font-weight:700'
            elif val <= 0.03: return 'color: #d4a017'
            return 'color: #dd6974'
        def color_sac(val):
            if abs(val - 0.5) <= 0.01: return 'color: #6daa45; font-weight:700'
            elif abs(val - 0.5) <= 0.03: return 'color: #d4a017'
            return 'color: #dd6974'
        def color_score(val):
            if val >= 90: return 'color: #6daa45; font-weight:800'
            elif val >= 70: return 'color: #d4a017; font-weight:700'
            return 'color: #dd6974'
        return (df_in.style
            .map(color_nl, subset=["NL"])
            .map(color_lap, subset=["LAP"])
            .map(color_dap, subset=["DAP"])
            .map(color_sac, subset=["SAC", "BIC-SAC"])
            .map(color_score, subset=["Score"])
            .set_properties(**{
                'background-color': '#0d1120',
                'color': '#c8d4e0',
                'border': '1px solid #1a2030',
                'font-family': 'JetBrains Mono, monospace',
                'font-size': '0.8rem',
                'padding': '0.4rem 0.8rem',
            })
            .set_table_styles([{
                'selector': 'th',
                'props': [
                    ('background-color', '#111520'),
                    ('color', '#4f98a3'),
                    ('font-family', 'JetBrains Mono, monospace'),
                    ('font-size', '0.72rem'),
                    ('letter-spacing', '0.08em'),
                    ('padding', '0.6rem 0.8rem'),
                    ('border', '1px solid #1a2030'),
                ]
            }])
        )

    display_df = df[["Rank","Poly","AES","NL","SAC","BIC-NL","BIC-SAC","LAP","DAP","Score"]]
    st.dataframe(style_table(display_df), use_container_width=True, height=400)

    # ── Heatmap
    if show_heatmap:
        st.markdown('<div class="section-hdr">🌡️ Heatmap Komparatif</div>', unsafe_allow_html=True)

        params = ["NL","SAC","BIC-NL","BIC-SAC","LAP","DAP"]
        heat_df = df.set_index("Poly")[params].copy()

        # Normalize 0-1 (higher = better for all, invert LAP/DAP)
        norm = heat_df.copy()
        for p in ["NL","SAC","BIC-NL","BIC-SAC"]:
            mn, mx = heat_df[p].min(), heat_df[p].max()
            if mx > mn: norm[p] = (heat_df[p] - mn) / (mx - mn)
            else: norm[p] = 1.0
        for p in ["LAP","DAP"]:
            mn, mx = heat_df[p].min(), heat_df[p].max()
            if mx > mn: norm[p] = 1 - (heat_df[p] - mn) / (mx - mn)
            else: norm[p] = 1.0

        fig, ax = plt.subplots(figsize=(12, max(6, len(df)*0.38)))
        fig.patch.set_facecolor('#080c16')
        ax.set_facecolor('#0a0e1a')

        cmap = mcolors.LinearSegmentedColormap.from_list("teal_dark",
            ["#0a0e1a", "#1a3040", "#1e5060", "#2a7888", "#4f98a3", "#7ab8c4", "#a8d8dc"])
        im = ax.imshow(norm.values.T, cmap=cmap, aspect='auto', vmin=0, vmax=1)

        ax.set_xticks(range(len(df)))
        ax.set_xticklabels(df["Poly"].tolist(), rotation=45, ha='right',
                          fontsize=7.5, color='#7ab8c4', fontfamily='monospace')
        ax.set_yticks(range(len(params)))
        ax.set_yticklabels(params, fontsize=9, color='#a8d8dc', fontfamily='monospace', fontweight='bold')

        # Add values
        for i in range(len(df)):
            for j, p in enumerate(params):
                val = heat_df.iloc[i][p]
                txt = f"{val:.0f}" if p in ["NL","BIC-NL"] else f"{val:.4f}"
                text_color = '#080c16' if norm.values[i,j] > 0.55 else '#ffffff'
                ax.text(i, j, txt, ha='center', va='center',
                       fontsize=6.5, color=text_color,
                       fontfamily='monospace', fontweight='bold')

        # Highlight AES column
        aes_idx = df[df["AES"] == "✓"].index
        if len(aes_idx) > 0:
            aes_pos = df.index.get_loc(aes_idx[0])
            for j in range(len(params)):
                ax.add_patch(plt.Rectangle((aes_pos-0.5, j-0.5), 1, 1,
                    fill=False, edgecolor='#d4a017', linewidth=1.5, alpha=0.8))

        cbar = plt.colorbar(im, ax=ax, pad=0.01, shrink=0.8)
        cbar.ax.tick_params(colors='#4a6a7a', labelsize=7)
        cbar.set_label('Normalized Score', color='#4a6a7a', fontsize=8)

        ax.set_title("Perbandingan 6 Parameter — Semua Polinomial Irreducible",
                    color='#a8d8dc', pad=12, fontsize=11, fontfamily='monospace')
        ax.tick_params(colors='#4a6a7a', length=0)
        for sp in ax.spines.values(): sp.set_edgecolor('#1a2030')
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    # ── Radar top 5
    if show_radar:
        st.markdown('<div class="section-hdr">🕸️ Radar Chart — Top 5 Terbaik</div>', unsafe_allow_html=True)

        top5 = df.head(5)
        categories = ["NL","SAC","BIC-NL","BIC-SAC","LAP","DAP"]
        N = len(categories)
        angles = [n / float(N) * 2 * np.pi for n in range(N)]
        angles += angles[:1]

        fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
        fig.patch.set_facecolor('#080c16')
        ax.set_facecolor('#0a0e1a')

        colors = ['#4f98a3','#9b6fd4','#d4a017','#6daa45','#dd6974']

        # Normalize values 0-1
        ref = {"NL":112,"SAC":0.5,"BIC-NL":112,"BIC-SAC":0.5,"LAP":0.0625,"DAP":0.015625}
        for i, (_, row) in enumerate(top5.iterrows()):
            vals = []
            for p in categories:
                v = row[p]
                if p in ["LAP","DAP"]:
                    vals.append(max(0, 1 - v/ref[p]))
                elif p == "SAC":
                    vals.append(max(0, 1 - abs(v-0.5)*10))
                elif p == "BIC-SAC":
                    vals.append(max(0, 1 - abs(v-0.5)*10))
                else:
                    vals.append(min(1, v/ref[p]))
            vals += vals[:1]
            col = colors[i % len(colors)]
            ax.plot(angles, vals, 'o-', linewidth=2, color=col, alpha=0.9, markersize=4)
            ax.fill(angles, vals, alpha=0.07, color=col)

        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories, color='#a8d8dc', fontsize=10, fontfamily='monospace', fontweight='bold')
        ax.set_ylim(0, 1)
        ax.set_yticks([0.25, 0.5, 0.75, 1.0])
        ax.set_yticklabels(["0.25","0.5","0.75","1.0"], color='#7ab8c4', fontsize=7)
        ax.grid(color='#1a2540', linewidth=0.7, alpha=0.6)
        ax.spines['polar'].set_edgecolor('#1a2540')

        legend_labels = [f"#{row['Rank']} {row['Poly']}" for _, row in top5.iterrows()]
        legend = ax.legend(legend_labels, loc='upper right', bbox_to_anchor=(1.35, 1.15),
                          fontsize=8, framealpha=0, labelcolor='#c8d4e0')
        for i, text in enumerate(legend.get_texts()):
            text.set_color(colors[i % len(colors)])

        ax.set_title("Profil Kriptografis Top 5 Polinomial", color='#a8d8dc',
                    pad=20, fontsize=11, fontfamily='monospace')
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    # ── Bar Charts NL & Score
    st.markdown('<div class="section-hdr">📈 Distribusi NL & Composite Score</div>', unsafe_allow_html=True)
    bc1, bc2 = st.columns(2)

    with bc1:
        fig, ax = plt.subplots(figsize=(7, 4))
        fig.patch.set_facecolor('#080c16')
        ax.set_facecolor('#0a0e1a')
        colors_nl = ['#d4a017' if r["AES"]=="✓" else '#4f98a3' for _,r in df.iterrows()]
        bars = ax.barh(df["Poly"].tolist(), df["NL"].tolist(), color=colors_nl, alpha=0.85, height=0.65)
        ax.axvline(x=112, color='#fb542b', linestyle='--', linewidth=1.2, alpha=0.7, label='AES (112)')
        ax.set_xlabel("Nonlinearity (NL)", color='#4a6a7a', fontsize=8, fontfamily='monospace')
        ax.tick_params(colors='#a8d8dc', labelsize=7.5)
        for sp in ax.spines.values(): sp.set_edgecolor('#1a2030')
        ax.set_facecolor('#0a0e1a')
        ax.legend(fontsize=7, framealpha=0, labelcolor='#fb542b')
        ax.set_title("NL per Polinomial", color='#a8d8dc', fontsize=9, fontfamily='monospace')
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    with bc2:
        fig, ax = plt.subplots(figsize=(7, 4))
        fig.patch.set_facecolor('#080c16')
        ax.set_facecolor('#0a0e1a')
        score_colors = ['#6daa45' if s>=90 else '#d4a017' if s>=70 else '#dd6974' for s in df["Score"]]
        ax.barh(df["Poly"].tolist(), df["Score"].tolist(), color=score_colors, alpha=0.85, height=0.65)
        ax.axvline(x=100, color='#6daa45', linestyle='--', linewidth=1, alpha=0.5)
        ax.set_xlabel("Composite Score (/100)", color='#4a6a7a', fontsize=8, fontfamily='monospace')
        ax.set_xlim(0, 105)
        ax.tick_params(colors='#a8d8dc', labelsize=7.5)
        for sp in ax.spines.values(): sp.set_edgecolor('#1a2030')
        ax.set_title("Composite Score per Polinomial", color='#a8d8dc', fontsize=9, fontfamily='monospace')
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    # ── LAP & DAP
    st.markdown('<div class="section-hdr">⚡ LAP & DAP — Ketahanan Diferensial & Linear</div>', unsafe_allow_html=True)
    dc1, dc2 = st.columns(2)
    with dc1:
        fig, ax = plt.subplots(figsize=(7,4))
        fig.patch.set_facecolor('#080c16')
        ax.set_facecolor('#0a0e1a')
        lap_colors = ['#6daa45' if v<=0.0625 else '#d4a017' if v<=0.1 else '#dd6974' for v in df["LAP"]]
        ax.barh(df["Poly"].tolist(), df["LAP"].tolist(), color=lap_colors, alpha=0.85, height=0.65)
        ax.axvline(x=0.0625, color='#fb542b', linestyle='--', lw=1.2, alpha=0.7, label='AES (0.0625)')
        ax.set_xlabel("LAP (↓ lebih baik)", color='#4a6a7a', fontsize=8, fontfamily='monospace')
        ax.tick_params(colors='#a8d8dc', labelsize=7.5)
        for sp in ax.spines.values(): sp.set_edgecolor('#1a2030')
        ax.legend(fontsize=7, framealpha=0, labelcolor='#fb542b')
        ax.set_title("Linear Approximation Probability", color='#a8d8dc', fontsize=9, fontfamily='monospace')
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    with dc2:
        fig, ax = plt.subplots(figsize=(7,4))
        fig.patch.set_facecolor('#080c16')
        ax.set_facecolor('#0a0e1a')
        dap_colors = ['#6daa45' if v<=0.015625 else '#d4a017' if v<=0.03 else '#dd6974' for v in df["DAP"]]
        ax.barh(df["Poly"].tolist(), df["DAP"].tolist(), color=dap_colors, alpha=0.85, height=0.65)
        ax.axvline(x=0.015625, color='#fb542b', linestyle='--', lw=1.2, alpha=0.7, label='AES (0.0156)')
        ax.set_xlabel("DAP (↓ lebih baik)", color='#4a6a7a', fontsize=8, fontfamily='monospace')
        ax.tick_params(colors='#a8d8dc', labelsize=7.5)
        for sp in ax.spines.values(): sp.set_edgecolor('#1a2030')
        ax.legend(fontsize=7, framealpha=0, labelcolor='#fb542b')
        ax.set_title("Differential Approximation Probability", color='#a8d8dc', fontsize=9, fontfamily='monospace')
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    # ── Detail per poly
    if show_detail:
        st.markdown('<div class="section-hdr">🔍 Detail Per Polinomial</div>', unsafe_allow_html=True)
        for _, row in df.iterrows():
            with st.expander(f"#{int(row['Rank'])} — {row['Poly']} {'⭐ AES' if row['AES']=='✓' else ''}"):
                d1, d2, d3, d4, d5, d6 = st.columns(6)
                for col, param, ref_val, better in [
                    (d1,"NL",112,"high"), (d2,"SAC",0.5,"mid"),
                    (d3,"BIC-NL",112,"high"), (d4,"BIC-SAC",0.5,"mid"),
                    (d5,"LAP",0.0625,"low"), (d6,"DAP",0.015625,"low")
                ]:
                    v = row[param]
                    if better == "high": cls = "score-high" if v >= ref_val else ("score-mid" if v >= ref_val*0.9 else "score-low")
                    elif better == "mid": cls = "score-high" if abs(v-ref_val)<0.01 else ("score-mid" if abs(v-ref_val)<0.03 else "score-low")
                    else: cls = "score-high" if v <= ref_val else ("score-mid" if v <= ref_val*1.5 else "score-low")
                    fmt = f"{v:.0f}" if param in ["NL","BIC-NL"] else f"{v:.6f}"
                    col.markdown(f'<div style="text-align:center"><div style="font-size:0.68rem;color:#4a6a7a;font-family:monospace;text-transform:uppercase">{param}</div><span class="score-pill {cls}">{fmt}</span><div style="font-size:0.65rem;color:#2a3a4a;margin-top:0.2rem">ref: {ref_val}</div></div>', unsafe_allow_html=True)

    # ── DOWNLOAD ───────────────────────────────────────────────────────────────
    st.markdown('<div class="section-hdr">💾 Export Hasil</div>', unsafe_allow_html=True)
    exp1, exp2, exp3 = st.columns(3)

    export_df = df[["Rank","Poly","Hex","AES","NL","SAC","BIC-NL","BIC-SAC","LAP","DAP","Score"]]

    with exp1:
        csv = export_df.to_csv(index=False).encode('utf-8')
        st.download_button("⬇️ Download CSV", csv, "sbox_comparison.csv", "text/csv", use_container_width=True)

    with exp2:
        buf = io.BytesIO()
        with pd.ExcelWriter(buf, engine='openpyxl') as writer:
            export_df.to_excel(writer, index=False, sheet_name='Comparison')
            top5_exp = df.head(5)[["Rank","Poly","NL","SAC","BIC-NL","BIC-SAC","LAP","DAP","Score"]]
            top5_exp.to_excel(writer, index=False, sheet_name='Top5')
        st.download_button("⬇️ Download Excel", buf.getvalue(), "sbox_comparison.xlsx",
                          "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                          use_container_width=True)

    with exp3:
        report = f"""S-BOX COMPARATIVE ANALYSIS REPORT
GF(2^8) · Algebraic Method · {len(df)} Polynomials
Affine Constant: {hex(st.session_state.get('const_val', 0x63))}
{'='*55}

TOP 5 RANKING (sorted by {sort_by}):
"""
        for _, row in df.head(5).iterrows():
            report += f"\n#{int(row['Rank'])} {row['Poly']}"
            if row['AES'] == '✓': report += " [AES Standard]"
            report += f"\n   NL={row['NL']} | SAC={row['SAC']:.4f} | BIC-NL={row['BIC-NL']:.2f}"
            report += f"\n   BIC-SAC={row['BIC-SAC']:.4f} | LAP={row['LAP']:.6f} | DAP={row['DAP']:.6f}"
            report += f"\n   Score={row['Score']:.2f}/100\n"

        report += f"""
{'='*55}
AES REFERENCE VALUES:
   NL=112 | SAC=0.5040 | BIC-NL=112.0
   BIC-SAC=0.5000 | LAP=0.062500 | DAP=0.015625
"""
        st.download_button("⬇️ Download Report TXT", report.encode(), "sbox_report.txt",
                          "text/plain", use_container_width=True)

else:
    # Empty state
    st.markdown("""
    <div style="text-align:center; padding: 5rem 2rem; color:#2a3a4a;">
        <div style="font-size:4rem; margin-bottom:1rem;">📊</div>
        <div style="font-size:1.2rem; color:#4a6a7a; font-weight:600; margin-bottom:0.5rem;">Belum ada data</div>
        <div style="font-size:0.88rem; color:#4f98a3; font-family:'JetBrains Mono',monospace;">
            Pilih polinomial di sidebar, lalu klik <strong style="color:#4f98a3">🚀 Jalankan Komparasi</strong>
        </div>
        <div style="margin-top:2rem; font-size:0.78rem; color:#4a6a7a; font-family:monospace;">
            ⚠️ Komputasi penuh 30 poly ≈ 8–15 menit · Pilih subset untuk hasil lebih cepat
        </div>
    </div>
    """, unsafe_allow_html=True)

# ─── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; padding: 2rem 0 1rem; border-top: 1px solid #1a2030; margin-top:2rem;">
    <div style="font-family:'JetBrains Mono',monospace; font-size:0.7rem; color:#4a6a7a; letter-spacing:0.1em;">
        TUGAS MATKUL KRIPTOGRAFI LANJUT &nbsp;·&nbsp; KONSTRUKSI S-BOX GF(2⁸) &nbsp;·&nbsp; METODE ALJABAR
    </div>
</div>
""", unsafe_allow_html=True)
