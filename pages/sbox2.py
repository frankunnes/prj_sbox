import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import io
import csv
import time

# ─── PAGE CONFIG ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="S-Box Evaluator · GF(2⁸)",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── CUSTOM CSS (same style as sbox1.py) ──────────────────────────────────────
st.markdown("""
<style>
@import url('https://api.fontshare.com/v2/css?f[]=satoshi@300,400,500,700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&display=swap');

:root {
    --primary: #01696f;
    --primary-light: #4f98a3;
    --bg-dark: #0f1117;
    --surface: #1a1d27;
    --surface2: #1f2235;
    --border: #2a2d3e;
    --text: #e2e8f0;
    --text-muted: #8892a4;
}

html, body, [class*="css"] { font-family: 'Satoshi', sans-serif !important; }
.stApp { background: linear-gradient(135deg, #0a0e1a 0%, #0f1117 50%, #0d1520 100%); }
/* Hide Streamlit branding */
#MainMenu {visibility: hidden;} footer {visibility: hidden;} 
/* header {visibility: hidden;} <- dinonaktifkan agar tombol collapse sidebar muncul */

/* Menyembunyikan navigasi halaman multipage bawaan */
[data-testid="stSidebarNav"] {display: none !important;}

[data-testid="stSidebar"] {
    background: #111420 !important;
    border-right: 1px solid #1e2235;
}

.crypto-card {
    background: linear-gradient(135deg, #1a1d2e 0%, #1e2235 100%);
    border: 1px solid #2a2d3e;
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    box-shadow: 0 4px 24px rgba(0,0,0,0.4);
    transition: border-color 0.2s ease;
}
.crypto-card:hover { border-color: #01696f; }

.metric-card {
    background: linear-gradient(135deg, #161925 0%, #1c2035 100%);
    border: 1px solid #252840;
    border-radius: 10px;
    padding: 1.2rem 1.5rem;
    text-align: center;
    transition: all 0.2s ease;
    height: 100%;
}
.metric-card:hover {
    border-color: #01696f;
    box-shadow: 0 0 20px rgba(1,105,111,0.15);
}
.metric-value {
    font-size: 1.5rem;
    font-weight: 700;
    color: #4f98a3;
    font-family: 'JetBrains Mono', monospace;
    line-height: 1.2;
    white-space: nowrap;
    letter-spacing: -0.03em;
}
.metric-value-good { color: #6daa45; }
.metric-value-warn { color: #da7101; }
.metric-label {
    font-size: 0.75rem;
    color: #8892a4;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-top: 0.3rem;
}
.metric-ref {
    font-size: 0.72rem;
    color: #4a5568;
    margin-top: 0.25rem;
    font-family: 'JetBrains Mono', monospace;
}
.metric-status { font-size: 0.82rem; margin-top: 0.4rem; font-weight: 500; }
.status-ok { color: #6daa45; }
.status-warn { color: #da7101; }
.status-bad { color: #a12c7b; }

.hero-section {
    background: linear-gradient(135deg, #0d1520 0%, #111a28 50%, #0f1825 100%);
    border: 1px solid #1e2d3d;
    border-radius: 16px;
    padding: 2.5rem 3rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero-section::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 200px; height: 200px;
    background: radial-gradient(circle, rgba(1,105,111,0.12) 0%, transparent 70%);
    pointer-events: none;
}
.hero-title {
    font-size: 2.2rem;
    font-weight: 700;
    background: linear-gradient(135deg, #4f98a3 0%, #6db8c0 50%, #a8d8dc 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.2;
    margin-bottom: 0.5rem;
}
.hero-subtitle { color: #8892a4; font-size: 1rem; line-height: 1.6; }

.step-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    background: rgba(1,105,111,0.15);
    border: 1px solid rgba(79,152,163,0.3);
    border-radius: 20px;
    padding: 0.3rem 0.9rem;
    font-size: 0.8rem;
    color: #4f98a3;
    font-weight: 600;
    letter-spacing: 0.05em;
    margin-bottom: 1rem;
    text-transform: uppercase;
}

.info-box {
    background: rgba(1,105,111,0.08);
    border-left: 3px solid #01696f;
    border-radius: 0 8px 8px 0;
    padding: 0.8rem 1rem;
    margin: 0.8rem 0;
    font-size: 0.9rem;
    color: #a0aec0;
    line-height: 1.6;
}

.param-section {
    background: linear-gradient(135deg, #151825 0%, #1a1e30 100%);
    border: 1px solid #252840;
    border-radius: 14px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
}
.param-title {
    font-size: 1rem;
    font-weight: 600;
    color: #4f98a3;
    margin-bottom: 0.5rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.param-formula {
    background: rgba(0,0,0,0.3);
    border-radius: 6px;
    padding: 0.5rem 0.8rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
    color: #a8d8dc;
    margin: 0.5rem 0;
}
.param-desc { font-size: 0.85rem; color: #8892a4; line-height: 1.6; }

.stDownloadButton button {
    background: linear-gradient(135deg, #01696f, #0c4e54) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
}
.stDownloadButton button:hover {
    background: linear-gradient(135deg, #0c4e54, #0f3638) !important;
    box-shadow: 0 4px 12px rgba(1,105,111,0.4) !important;
}

hr { border-color: #1e2235 !important; margin: 1.5rem 0 !important; }

.compare-row {
    display: flex;
    justify-content: space-between;
    padding: 0.5rem 0.8rem;
    border-radius: 6px;
    margin-bottom: 0.3rem;
    background: rgba(255,255,255,0.02);
    border: 1px solid #1e2235;
    font-size: 0.88rem;
}
.compare-label { color: #8892a4; }
.compare-val { font-family: 'JetBrains Mono', monospace; color: #4f98a3; font-weight: 600; }
.compare-aes { font-family: 'JetBrains Mono', monospace; color: #6daa45; }
</style>
""", unsafe_allow_html=True)


# ─── GF FUNCTIONS ──────────────────────────────────────────────────────────────
FIELD_SIZE = 256

def gf_multiply(a, b, poly=0x11B):
    result = 0
    for _ in range(8):
        if b & 1: result ^= a
        hi = a & 0x80
        a = (a << 1) & 0xFF
        if hi: a ^= (poly & 0xFF)
        b >>= 1
    return result

def build_inverse_table(poly=0x11B):
    inv = [0]*256
    for x in range(1, 256):
        for b in range(1, 256):
            if gf_multiply(x, b, poly) == 1:
                inv[x] = b; break
    return inv

def affine_transform(byte, const=0x63):
    result = 0
    for i in range(8):
        b = (byte >> i) & 1
        b ^= (byte >> ((i+4)%8)) & 1
        b ^= (byte >> ((i+5)%8)) & 1
        b ^= (byte >> ((i+6)%8)) & 1
        b ^= (byte >> ((i+7)%8)) & 1
        b ^= (const >> i) & 1
        result |= (b << i)
    return result

@st.cache_data
def build_default_sbox():
    inv = build_inverse_table(0x11B)
    return [affine_transform(inv[x]) for x in range(256)]

# ─── EVALUATION FUNCTIONS ──────────────────────────────────────────────────────
def bit_dot(a, x):
    return bin(a & x).count("1") % 2

def walsh_transform_component(sbox, a, b):
    total = 0
    for x in range(256):
        exp = bit_dot(a, x) ^ bit_dot(b, sbox[x])
        total += (-1)**exp
    return total

@st.cache_data
def compute_nl(sbox_tuple):
    sbox = list(sbox_tuple)
    min_nl = float('inf')
    for b in range(1, 256):
        max_w = 0
        for a in range(256):
            w = abs(walsh_transform_component(sbox, a, b))
            if w > max_w: max_w = w
        nl = 2**7 - max_w // 2
        if nl < min_nl: min_nl = nl
    return min_nl

@st.cache_data
def compute_sac(sbox_tuple):
    sbox = list(sbox_tuple)
    n = 8
    total = 0.0
    count = 0
    for i in range(n):           # flip bit ke-i
        ei = 1 << i
        for j in range(n):       # bit output ke-j
            ones = sum(1 for x in range(256) if ((sbox[x] >> j) & 1) != ((sbox[x ^ ei] >> j) & 1))
            total += ones / 256
            count += 1
    return total / count

@st.cache_data
def compute_bic_nl(sbox_tuple):
    sbox = list(sbox_tuple)
    nls = []
    for i in range(8):
        for j in range(i+1, 8):
            f = [((sbox[x] >> i) ^ (sbox[x] >> j)) & 1 for x in range(256)]
            max_w = 0
            for a in range(256):
                w = abs(sum((-1)**(f[x] ^ bit_dot(a, x)) for x in range(256)))
                if w > max_w: max_w = w
            nl = 2**7 - max_w // 2
            nls.append(nl)
    return min(nls), sum(nls)/len(nls)

@st.cache_data
def compute_bic_sac(sbox_tuple):
    sbox = list(sbox_tuple)
    vals = []
    for i in range(8):
        for j in range(i+1, 8):
            for k in range(8):
                ek = 1 << k
                ones = sum(1 for x in range(256)
                           if (((sbox[x] >> i) ^ (sbox[x] >> j)) & 1) !=
                              (((sbox[x ^ ek] >> i) ^ (sbox[x ^ ek] >> j)) & 1))
                vals.append(ones / 256)
    return sum(vals) / len(vals)

@st.cache_data
def compute_lap(sbox_tuple):
    sbox = list(sbox_tuple)
    max_bias = 0
    for a in range(1, 256):
        for b in range(1, 256):
            w = abs(walsh_transform_component(sbox, a, b))
            bias = w // 2
            if bias > max_bias: max_bias = bias
    return (max_bias / 128) ** 2

@st.cache_data
def compute_dap(sbox_tuple):
    sbox = list(sbox_tuple)
    max_count = 0
    for dx in range(1, 256):
        counts = {}
        for x in range(256):
            dy = sbox[x] ^ sbox[x ^ dx]
            counts[dy] = counts.get(dy, 0) + 1
        mc = max(counts.values())
        if mc > max_count: max_count = mc
    return max_count / 256

# ─── AES REFERENCE VALUES ──────────────────────────────────────────────────────
AES_SBOX = build_default_sbox()
AES_REF = {
    "NL": 112, "SAC": 0.504, "BIC-NL": 112,
    "BIC-SAC": 0.500, "LAP": 0.0625, "DAP": 0.015625
}

# ─── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; margin-top:-3.5rem; padding-bottom:1rem;">
        <div style="font-size:2.5rem; margin-bottom:0rem;">🔬</div>
        <div style="font-size:1.1rem; font-weight:700; color:#4f98a3;">S-Box Evaluator</div>
        <div style="font-size:0.78rem; color:#8892a4; margin-top:0.2rem;">6 Parameter Kriptografis</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 📂 Sumber S-Box")
    st.markdown("---")

    source_mode = st.radio(
        "Pilih sumber S-box:",
        ["🔧 Generate baru (AES default)", "📁 Upload dari file (hasil sbox1.py)"],
        index=None
    )

    sbox_input = None

    if source_mode == "📁 Upload dari file (hasil sbox1.py)":
        uploaded = st.file_uploader(
            "Upload sbox_result.csv atau sbox_result.py",
            type=["csv", "py", "bin"],
            help="File hasil download dari sbox1.py"
        )
        if uploaded is not None:
            try:
                if uploaded.name.endswith(".csv"):
                    content = uploaded.read().decode("utf-8")
                    lines = content.strip().split("\n")
                    vals = []
                    for line in lines[1:]:  # skip header
                        parts = line.split(",")
                        if len(parts) > 16:
                            parts = parts[1:]  # skip row index
                        for p in parts:
                            p = p.strip().strip('"')
                            if p.startswith("0x") or p.startswith("0X"):
                                vals.append(int(p, 16))
                            elif p.isdigit():
                                vals.append(int(p))
                    if len(vals) == 256:
                        sbox_input = vals
                        st.success(f"✅ CSV berhasil dibaca ({len(vals)} nilai)")
                    else:
                        st.error(f"❌ Ditemukan {len(vals)} nilai, butuh 256")

                elif uploaded.name.endswith(".py"):
                    content = uploaded.read().decode("utf-8")
                    # Extract SBOX = [...]
                    import re
                    match = re.search(r"SBOX\s*=\s*(\[.*?\])", content, re.DOTALL)
                    if match:
                        sbox_input = eval(match.group(1))
                        st.success(f"✅ Python file berhasil dibaca ({len(sbox_input)} nilai)")
                    else:
                        st.error("❌ Tidak ditemukan variabel SBOX di file")

                elif uploaded.name.endswith(".bin"):
                    raw = uploaded.read()
                    if len(raw) == 256:
                        sbox_input = list(raw)
                        st.success(f"✅ Binary file berhasil dibaca (256 bytes)")
                    else:
                        st.error(f"❌ File binary harus 256 bytes, ditemukan {len(raw)}")

            except Exception as e:
                st.error(f"❌ Error membaca file: {e}")

    st.markdown("---")
    st.markdown("### ⚙️ Opsi Evaluasi")
    show_charts = st.toggle("Tampilkan Charts", value=True)
    show_theory  = st.toggle("Tampilkan Teori & Rumus", value=True)
    compare_aes  = st.toggle("Bandingkan dengan AES", value=True)

    st.markdown("---")
    st.markdown("""
    <div style="text-align:center; font-size:0.82rem; padding: 0.6rem; background: rgba(1,105,111,0.05); border-radius: 8px; border: 1px solid rgba(79,152,163,0.2);">
        <div style="margin-bottom: 0.4rem;">
            <a href="./" target="_self" style="color:#a8d8dc; text-decoration:none; font-weight:600; transition:color 0.2s;">🏠 Home</a> 
        </div>
        <div>
            <a href="sbox1" target="_self" style="color:#a8d8dc; text-decoration:none; font-weight:600; transition:color 0.2s;">Konstruksi</a> 
            <span style="color:#2a2d3e; margin: 0 0.3rem;">|</span> 
            <a href="sbox2" target="_self" style="color:#4f98a3; text-decoration:none; font-weight:700;">Evaluasi</a> 
            <span style="color:#2a2d3e; margin: 0 0.3rem;">|</span> 
            <a href="sbox3" target="_self" style="color:#a8d8dc; text-decoration:none; font-weight:600; transition:color 0.2s;">Komparasi</a>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ─── RESOLVE SBOX ──────────────────────────────────────────────────────────────
if source_mode == "🔧 Generate baru (AES default)":
    sbox = AES_SBOX
    sbox_label = "AES Default (poly=0x11B, c=0x63)"
elif sbox_input is not None:
    sbox = sbox_input
    sbox_label = f"Upload: {uploaded.name}"
else:
    sbox = None

# ─── HERO ──────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="hero-section">
    <div class="hero-title"><span style="-webkit-text-fill-color: initial; background: none;">🔬</span> Evaluasi S-Box · 6 Parameter Kriptografis</div>
    <div class="hero-subtitle">
        Nonlinearity · SAC · BIC-NL · BIC-SAC · LAP · DAP<br>
        <span style="color:#4f98a3; font-family:'JetBrains Mono',monospace; font-size:0.9rem;">
            {'S-Box: ' + sbox_label if sbox is not None else 'Menunggu input S-Box...'}
        </span>
    </div>
</div>
""", unsafe_allow_html=True)

if sbox is None:
    st.markdown("""
    <div class="info-box" style="font-size:1rem; text-align:center; padding:2rem;">
        📁 Silakan upload file S-Box dari sidebar, atau pilih mode "Generate baru"
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ─── COMPUTE ALL PARAMS ────────────────────────────────────────────────────────
sbox_tuple = tuple(sbox)

with st.spinner("⏳ Menghitung 6 parameter kriptografis... (mohon tunggu)"):
    progress = st.progress(0, text="Menghitung NL...")
    nl   = compute_nl(sbox_tuple);      progress.progress(17, "Menghitung SAC...")
    sac  = compute_sac(sbox_tuple);     progress.progress(33, "Menghitung BIC-NL...")
    bic_nl_min, bic_nl_avg = compute_bic_nl(sbox_tuple); progress.progress(50, "Menghitung BIC-SAC...")
    bic_sac = compute_bic_sac(sbox_tuple); progress.progress(67, "Menghitung LAP...")
    lap  = compute_lap(sbox_tuple);     progress.progress(83, "Menghitung DAP...")
    dap  = compute_dap(sbox_tuple);     progress.progress(100, "✅ Selesai!")
    time.sleep(0.3)
    progress.empty()

results = {
    "NL":      {"val": nl,      "ref": AES_REF["NL"],      "better": "higher", "fmt": ".0f"},
    "SAC":     {"val": sac,     "ref": AES_REF["SAC"],     "better": "~0.5",   "fmt": ".4f"},
    "BIC-NL":  {"val": bic_nl_min, "ref": AES_REF["BIC-NL"], "better": "higher","fmt": ".0f"},
    "BIC-SAC": {"val": bic_sac, "ref": AES_REF["BIC-SAC"], "better": "~0.5",   "fmt": ".4f"},
    "LAP":     {"val": lap,     "ref": AES_REF["LAP"],     "better": "lower",  "fmt": ".6f"},
    "DAP":     {"val": dap,     "ref": AES_REF["DAP"],     "better": "lower",  "fmt": ".6f"},
}

def get_status(name, val, ref):
    if name == "NL" or name == "BIC-NL":
        if val >= ref: return "status-ok", "✅ Optimal"
        elif val >= ref * 0.9: return "status-warn", "⚠️ Cukup Baik"
        else: return "status-bad", "❌ Kurang"
    elif name in ("SAC", "BIC-SAC"):
        dev = abs(val - 0.5)
        if dev <= 0.01: return "status-ok", "✅ Ideal"
        elif dev <= 0.03: return "status-warn", "⚠️ Mendekati"
        else: return "status-bad", "❌ Jauh dari 0.5"
    else:  # LAP, DAP lower is better
        if val <= ref: return "status-ok", "✅ Optimal"
        elif val <= ref * 1.5: return "status-warn", "⚠️ Cukup"
        else: return "status-bad", "❌ Kurang Baik"

# ─── 6 METRIC CARDS ────────────────────────────────────────────────────────────
st.markdown('<div class="step-badge">📊 Hasil 6 Parameter Kriptografis</div>', unsafe_allow_html=True)

cols = st.columns(6)
param_names = ["NL", "SAC", "BIC-NL", "BIC-SAC", "LAP", "DAP"]
icons = ["🛡️", "⚖️", "🔗", "🔗", "📉", "📉"]

for idx, (name, icon) in enumerate(zip(param_names, icons)):
    with cols[idx]:
        r = results[name]
        val = r["val"]
        ref = r["ref"]
        fmt = r["fmt"]
        css_class, status_text = get_status(name, val, ref)
        val_display = f"{val:{fmt}}"
        ref_display = f"{ref:{fmt}}"
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size:1.4rem; margin-bottom:0.3rem;">{icon}</div>
            <div class="metric-value">{val_display}</div>
            <div class="metric-label">{name}</div>
            <div class="metric-ref">AES: {ref_display}</div>
            <div class="metric-status {css_class}">{status_text}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─── THEORY + DETAIL SECTIONS ──────────────────────────────────────────────────
param_theory = {
    "NL": {
        "icon": "🛡️", "name": "Nonlinearity (NL)",
        "formula": "NL(S) = min_{b≠0} [ 2^(n-1) - ½ · max_a |W_{f_b}(a)| ]",
        "desc": "Mengukur jarak minimum S-box dari semua fungsi affine. Semakin tinggi NL, semakin tahan terhadap **linear cryptanalysis**. Nilai maksimum teoritis untuk 8-bit S-box adalah 120, AES mencapai 112.",
        "ideal": "Semakin tinggi semakin baik (maks teoritis = 120, AES = 112)"
    },
    "SAC": {
        "icon": "⚖️", "name": "Strict Avalanche Criterion (SAC)",
        "formula": "SAC = (1/n·m) Σ_i Σ_j Pr[S(x)_j ≠ S(x⊕e_i)_j]",
        "desc": "Mengukur efek avalanche: apakah membalik 1 bit input menyebabkan tepat 50% bit output berubah. Nilai ideal = 0.5 (persis setengah bit berubah). Ini syarat penting untuk difusi yang baik.",
        "ideal": "Semakin mendekati 0.5 semakin baik"
    },
    "BIC-NL": {
        "icon": "🔗", "name": "Bit Independence Criterion - NL",
        "formula": "BIC-NL = min_{i≠j} NL(S_i ⊕ S_j)",
        "desc": "Mengukur nonlinearity dari setiap pasangan komponen bit output (XOR antar dua bit). Memastikan tidak ada dua bit output yang saling bergantung secara linear. Nilai sama dengan NL standar pada AES.",
        "ideal": "Semakin tinggi semakin baik (AES = 112)"
    },
    "BIC-SAC": {
        "icon": "🔗", "name": "Bit Independence Criterion - SAC",
        "formula": "BIC-SAC = avg_{i≠j,k} Pr[(S_i⊕S_j)(x) ≠ (S_i⊕S_j)(x⊕e_k)]",
        "desc": "Versi SAC untuk pasangan bit output. Mengukur apakah perubahan 1 bit input mempengaruhi setiap pasangan bit output secara independen dan seimbang. Nilai ideal = 0.5.",
        "ideal": "Semakin mendekati 0.5 semakin baik (AES ≈ 0.5)"
    },
    "LAP": {
        "icon": "📉", "name": "Linear Approximation Probability (LAP)",
        "formula": "LAP = max_{a≠0,b≠0} (|W_{f_b}(a)| / 2^n)²",
        "desc": "Probabilitas maksimum aproksimasi linear. Mengukur seberapa mudah S-box bisa didekati dengan fungsi linear. Semakin kecil, semakin tahan terhadap linear cryptanalysis.",
        "ideal": "Semakin kecil (mendekati 0) semakin baik (AES = 0.0625)"
    },
    "DAP": {
        "icon": "📉", "name": "Differential Approximation Probability (DAP)",
        "formula": "DAP = max_{Δx≠0,Δy} |{x: S(x)⊕S(x⊕Δx)=Δy}| / 2^n",
        "desc": "Probabilitas maksimum diferensial dari DDT (Difference Distribution Table). Mengukur ketahanan terhadap differential cryptanalysis. Semakin kecil, semakin aman.",
        "ideal": "Semakin kecil (mendekati 0) semakin baik (AES = 0.015625)"
    }
}

if show_theory:
    st.markdown("---")
    st.markdown('<div class="step-badge">📖 Teori & Penjelasan Parameter</div>', unsafe_allow_html=True)

    t1, t2 = st.columns(2)
    param_list = list(param_theory.items())
    for idx, (name, info) in enumerate(param_list):
        col = t1 if idx % 2 == 0 else t2
        r = results[name]
        val = r["val"]
        fmt = r["fmt"]
        css_class, status_text = get_status(name, val, r["ref"])
        with col:
            st.markdown(f"""
            <div class="param-section">
                <div class="param-title">{info['icon']} {info['name']}</div>
                <div class="param-formula">{info['formula']}</div>
                <div class="param-desc">{info['desc']}</div>
                <div style="margin-top:0.8rem; padding-top:0.8rem; border-top:1px solid #252840;">
                    <span style="color:#8892a4; font-size:0.78rem;">Hasil: </span>
                    <span style="font-family:'JetBrains Mono',monospace; color:#4f98a3; font-weight:700;">
                        {val:{fmt}}
                    </span>
                    &nbsp;&nbsp;
                    <span style="font-size:0.78rem; color:#4a5568;">— {info['ideal']}</span>
                    <br>
                    <span class="metric-status {css_class}" style="font-size:0.82rem;">{status_text}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ─── CHARTS ────────────────────────────────────────────────────────────────────
if show_charts:
    st.markdown("---")
    st.markdown('<div class="step-badge">📈 Visualisasi Hasil</div>', unsafe_allow_html=True)

    ch1, ch2 = st.columns(2)

    with ch1:
        # Bar chart: NL, BIC-NL comparison
        fig, ax = plt.subplots(figsize=(6, 4))
        fig.patch.set_facecolor('#1a1d2e')
        ax.set_facecolor('#1a1d2e')

        labels = ['NL', 'BIC-NL']
        vals_bar = [nl, bic_nl_min]
        refs_bar = [AES_REF["NL"], AES_REF["BIC-NL"]]

        x = np.arange(len(labels))
        w = 0.35
        ax.bar(x - w/2, vals_bar, w, label='S-Box Kita', color='#4f98a3', alpha=0.9)
        ax.bar(x + w/2, refs_bar, w, label='AES Referensi', color='#6daa45', alpha=0.7)

        ax.set_xticks(x); ax.set_xticklabels(labels, color='#8892a4', fontsize=11)
        ax.tick_params(colors='#8892a4')
        ax.set_ylim(0, 130)
        ax.set_title('NL & BIC-NL vs AES', color='#4f98a3', fontsize=11, pad=10)
        ax.legend(fontsize=8, facecolor='#1a1d2e', labelcolor='#8892a4', framealpha=0.8)
        ax.axhline(y=112, color='#da7101', linestyle='--', alpha=0.4, linewidth=1)
        for spine in ax.spines.values(): spine.set_edgecolor('#2a2d3e')
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True); plt.close()

    with ch2:
        # Radar / spider chart for all 6
        fig, ax = plt.subplots(figsize=(6, 4), subplot_kw=dict(polar=True))
        fig.patch.set_facecolor('#1a1d2e')
        ax.set_facecolor('#1a1d2e')

        # Normalize: NL/120, SAC/0.5 (closeness), BIC-NL/112...
        def normalize(name, val):
            if name in ("NL", "BIC-NL"):
                return val / 120
            elif name in ("SAC", "BIC-SAC"):
                return 1 - abs(val - 0.5) / 0.5
            else:  # LAP, DAP (lower better)
                return 1 - min(val / 0.25, 1.0)

        param_names_r = ["NL", "SAC", "BIC-NL", "BIC-SAC", "LAP", "DAP"]
        vals_r = [normalize(n, results[n]["val"]) for n in param_names_r]
        refs_r = [normalize(n, results[n]["ref"]) for n in param_names_r]

        angles = np.linspace(0, 2*np.pi, len(param_names_r), endpoint=False).tolist()
        vals_r += vals_r[:1]; refs_r += refs_r[:1]; angles += angles[:1]

        ax.plot(angles, vals_r, 'o-', linewidth=2, color='#4f98a3', label='S-Box Kita')
        ax.fill(angles, vals_r, alpha=0.2, color='#4f98a3')
        ax.plot(angles, refs_r, 'o--', linewidth=1.5, color='#6daa45', alpha=0.7, label='AES Ref')
        ax.fill(angles, refs_r, alpha=0.07, color='#6daa45')

        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(param_names_r, color='#8892a4', fontsize=9)
        ax.set_yticks([0.25, 0.5, 0.75, 1.0])
        ax.set_yticklabels(['25%','50%','75%','100%'], color='#4a5568', fontsize=7)
        ax.tick_params(colors='#4a5568')
        ax.set_title('Radar 6 Parameter (normalized)', color='#4f98a3', fontsize=10, pad=15)
        ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), fontsize=8,
                  facecolor='#1a1d2e', labelcolor='#8892a4', framealpha=0.8)
        ax.spines['polar'].set_color('#2a2d3e')
        ax.grid(color='#2a2d3e', linewidth=0.8)
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True); plt.close()

    # LAP & DAP bar
    ch3, ch4 = st.columns(2)
    with ch3:
        fig, ax = plt.subplots(figsize=(5, 3.5))
        fig.patch.set_facecolor('#1a1d2e')
        ax.set_facecolor('#1a1d2e')
        bars = ax.bar(['LAP (kita)', 'LAP (AES)'], [lap, AES_REF["LAP"]],
                      color=['#4f98a3','#6daa45'], alpha=0.9, width=0.5)
        ax.set_title('Linear Approx. Probability', color='#4f98a3', fontsize=10)
        ax.tick_params(colors='#8892a4')
        for spine in ax.spines.values(): spine.set_edgecolor('#2a2d3e')
        for bar in bars:
            ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.001,
                    f'{bar.get_height():.5f}', ha='center', color='#8892a4', fontsize=8)
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True); plt.close()

    with ch4:
        fig, ax = plt.subplots(figsize=(5, 3.5))
        fig.patch.set_facecolor('#1a1d2e')
        ax.set_facecolor('#1a1d2e')
        bars = ax.bar(['DAP (kita)', 'DAP (AES)'], [dap, AES_REF["DAP"]],
                      color=['#4f98a3','#6daa45'], alpha=0.9, width=0.5)
        ax.set_title('Differential Approx. Probability', color='#4f98a3', fontsize=10)
        ax.tick_params(colors='#8892a4')
        for spine in ax.spines.values(): spine.set_edgecolor('#2a2d3e')
        for bar in bars:
            ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.0002,
                    f'{bar.get_height():.6f}', ha='center', color='#8892a4', fontsize=8)
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True); plt.close()

# ─── COMPARISON TABLE ──────────────────────────────────────────────────────────
if compare_aes:
    st.markdown("---")
    st.markdown('<div class="step-badge">⚖️ Tabel Komparasi: S-Box Kita vs AES</div>', unsafe_allow_html=True)

    table_data = []
    for name in param_names:
        r = results[name]
        val = r["val"]; ref = r["ref"]; fmt = r["fmt"]
        css, status = get_status(name, val, ref)
        table_data.append({
            "Parameter": name,
            "Nilai S-Box Kita": f"{val:{fmt}}",
            "Nilai AES Referensi": f"{ref:{fmt}}",
            "Lebih Baik Jika": r["better"],
            "Status": status.replace("✅","✅ ").replace("⚠️","⚠️ ").replace("❌","❌ ")
        })
    df_cmp = pd.DataFrame(table_data)
    st.dataframe(df_cmp, use_container_width=True, hide_index=True)

# ─── DOWNLOAD RESULTS ──────────────────────────────────────────────────────────
st.markdown("---")
st.markdown('<div class="step-badge">📥 Download Hasil Evaluasi</div>', unsafe_allow_html=True)

dl1, dl2 = st.columns(2)

with dl1:
    report_lines = ["Parameter,Nilai,AES Referensi,Status\n"]
    for name in param_names:
        r = results[name]
        _, status = get_status(name, r["val"], r["ref"])
        report_lines.append(f"{name},{r['val']:{r['fmt']}},{r['ref']:{r['fmt']}},{status}\n")
    report_csv = "".join(report_lines)
    st.download_button("⬇️ Download Hasil CSV",
                       data=report_csv, file_name="sbox_evaluation.csv",
                       mime="text/csv", use_container_width=True)

with dl2:
    report_txt = f"""LAPORAN EVALUASI S-BOX GF(2^8)
{'='*45}
Sumber: {sbox_label}

HASIL 6 PARAMETER:
{'='*45}
"""
    for name in param_names:
        r = results[name]
        _, status = get_status(name, r["val"], r["ref"])
        report_txt += f"  {name:<10}: {r['val']:{r['fmt']}}  (AES: {r['ref']:{r['fmt']}})  {status}\n"
    report_txt += f"""
INTERPRETASI:
{'='*45}
- NL        : Semakin tinggi = lebih tahan linear attack
- SAC       : Mendekati 0.5 = efek avalanche ideal
- BIC-NL    : Semakin tinggi = bit output independen
- BIC-SAC   : Mendekati 0.5 = independensi bit baik
- LAP       : Semakin kecil = tahan linear cryptanalysis
- DAP       : Semakin kecil = tahan differential cryptanalysis
"""
    st.download_button("⬇️ Download Laporan TXT",
                       data=report_txt, file_name="sbox_evaluation.txt",
                       mime="text/plain", use_container_width=True)
