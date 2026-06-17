import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import io
import csv

# ─── PAGE CONFIG ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="S-Box Constructor · GF(2⁸)",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── CUSTOM CSS ────────────────────────────────────────────────────────────────
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
    --accent-glow: rgba(1, 105, 111, 0.3);
}

html, body, [class*="css"] {
    font-family: 'Satoshi', sans-serif !important;
}

/* Main background */
.stApp {
    background: linear-gradient(135deg, #0a0e1a 0%, #0f1117 50%, #0d1520 100%);
}

/* Hide Streamlit branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
/* header {visibility: hidden;} <- Baris ini dinonaktifkan agar tombol sidebar tetap muncul */

/* Menyembunyikan navigasi halaman multipage bawaan yang jelek */
[data-testid="stSidebarNav"] {display: none !important;}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #111420 !important;
    border-right: 1px solid #1e2235;
}
[data-testid="stSidebar"] .stMarkdown h1,
[data-testid="stSidebar"] .stMarkdown h2,
[data-testid="stSidebar"] .stMarkdown h3 {
    color: #4f98a3 !important;
}

/* Cards */
.crypto-card {
    background: linear-gradient(135deg, #1a1d2e 0%, #1e2235 100%);
    border: 1px solid #2a2d3e;
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    box-shadow: 0 4px 24px rgba(0,0,0,0.4);
    transition: border-color 0.2s ease;
}
.crypto-card:hover {
    border-color: #01696f;
}

/* Metric cards */
.metric-card {
    background: linear-gradient(135deg, #161925 0%, #1c2035 100%);
    border: 1px solid #252840;
    border-radius: 10px;
    padding: 1.2rem 1.5rem;
    text-align: center;
    transition: all 0.2s ease;
}
.metric-card:hover {
    border-color: #01696f;
    box-shadow: 0 0 20px rgba(1,105,111,0.15);
}
.metric-value {
    font-size: 2rem;
    font-weight: 700;
    color: #4f98a3;
    font-family: 'JetBrains Mono', monospace;
    line-height: 1.2;
}
.metric-label {
    font-size: 0.78rem;
    color: #8892a4;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-top: 0.3rem;
}
.metric-status {
    font-size: 0.85rem;
    margin-top: 0.4rem;
    font-weight: 500;
}
.status-ok { color: #6daa45; }
.status-warn { color: #da7101; }

/* Hero section */
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
.hero-subtitle {
    color: #8892a4;
    font-size: 1rem;
    line-height: 1.6;
}

/* Step badge */
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

/* Section title */
.section-title {
    font-size: 1.15rem;
    font-weight: 600;
    color: #e2e8f0;
    margin-bottom: 0.8rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

/* Hex table */
.hex-table-wrapper {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    overflow-x: auto;
}

/* Tag pills */
.tag-pill {
    display: inline-block;
    background: rgba(1,105,111,0.18);
    border: 1px solid rgba(79,152,163,0.25);
    border-radius: 6px;
    padding: 0.15rem 0.6rem;
    font-size: 0.78rem;
    color: #4f98a3;
    font-family: 'JetBrains Mono', monospace;
    margin: 0.1rem;
}

/* Download button styling */
.stDownloadButton button {
    background: linear-gradient(135deg, #01696f, #0c4e54) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    transition: all 0.2s ease !important;
}
.stDownloadButton button:hover {
    background: linear-gradient(135deg, #0c4e54, #0f3638) !important;
    box-shadow: 0 4px 12px rgba(1,105,111,0.4) !important;
}

/* Slider styling */
.stSlider label { color: #8892a4 !important; font-size: 0.85rem !important; }

/* Info box */
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

/* Validation row */
.val-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.55rem 0.9rem;
    border-radius: 8px;
    margin-bottom: 0.4rem;
    background: rgba(255,255,255,0.02);
    font-size: 0.9rem;
    border: 1px solid #1e2235;
}
.val-name { color: #a0aec0; }
.val-ok { color: #6daa45; font-weight: 600; }
.val-fail { color: #a12c7b; font-weight: 600; }
.val-count { color: #4f98a3; font-family: 'JetBrains Mono', monospace; }

/* Divider */
hr { border-color: #1e2235 !important; margin: 1.5rem 0 !important; }

/* Dataframe */
[data-testid="stDataFrame"] { border-radius: 10px !important; }
</style>
""", unsafe_allow_html=True)


# ─── GF(2^8) CORE FUNCTIONS ────────────────────────────────────────────────────
FIELD_SIZE = 256
DEFAULT_POLY = 0x11B  # x^8 + x^4 + x^3 + x + 1 (AES)

NAMED_POLYS = {
    "0x11B — AES (x⁸+x⁴+x³+x+1)": 0x11B,
    "0x11D — (x⁸+x⁴+x³+x²+1)": 0x11D,
    "0x12B — (x⁸+x⁵+x³+x+1)": 0x12B,
    "0x14D — (x⁸+x⁶+x³+x²+1)": 0x14D,
}

def gf_multiply(a, b, poly):
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

def gf_inverse(a, poly):
    if a == 0:
        return 0
    for b in range(1, FIELD_SIZE):
        if gf_multiply(a, b, poly) == 1:
            return b
    return 0

@st.cache_data
def build_inverse_table(poly):
    return [gf_inverse(x, poly) for x in range(FIELD_SIZE)]

def affine_transform(byte, const=0x63):
    result = 0
    for i in range(8):
        b = (byte >> i) & 1
        b ^= (byte >> ((i + 4) % 8)) & 1
        b ^= (byte >> ((i + 5) % 8)) & 1
        b ^= (byte >> ((i + 6) % 8)) & 1
        b ^= (byte >> ((i + 7) % 8)) & 1
        b ^= (const >> i) & 1
        result |= (b << i)
    return result

@st.cache_data
def build_sbox(poly, affine_const):
    inv_table = build_inverse_table(poly)
    return [affine_transform(inv_table[x], affine_const) for x in range(FIELD_SIZE)]

def validate_sbox(sbox):
    is_bijective = len(set(sbox)) == FIELD_SIZE
    is_balanced  = is_bijective  # same for 8→8 bijection
    fixed_pts    = [x for x in range(FIELD_SIZE) if sbox[x] == x]
    opp_mask     = 0xFF
    opp_fixed    = [x for x in range(FIELD_SIZE) if sbox[x] == (x ^ opp_mask)]
    return {
        "bijective": is_bijective,
        "balanced":  is_balanced,
        "fixed_points": fixed_pts,
        "opp_fixed_points": opp_fixed,
    }

AES_SBOX = [
    0x63,0x7c,0x77,0x7b,0xf2,0x6b,0x6f,0xc5,0x30,0x01,0x67,0x2b,0xfe,0xd7,0xab,0x76,
    0xca,0x82,0xc9,0x7d,0xfa,0x59,0x47,0xf0,0xad,0xd4,0xa2,0xaf,0x9c,0xa4,0x72,0xc0,
    0xb7,0xfd,0x93,0x26,0x36,0x3f,0xf7,0xcc,0x34,0xa5,0xe5,0xf1,0x71,0xd8,0x31,0x15,
    0x04,0xc7,0x23,0xc3,0x18,0x96,0x05,0x9a,0x07,0x12,0x80,0xe2,0xeb,0x27,0xb2,0x75,
    0x09,0x83,0x2c,0x1a,0x1b,0x6e,0x5a,0xa0,0x52,0x3b,0xd6,0xb3,0x29,0xe3,0x2f,0x84,
    0x53,0xd1,0x00,0xed,0x20,0xfc,0xb1,0x5b,0x6a,0xcb,0xbe,0x39,0x4a,0x4c,0x58,0xcf,
    0xd0,0xef,0xaa,0xfb,0x43,0x4d,0x33,0x85,0x45,0xf9,0x02,0x7f,0x50,0x3c,0x9f,0xa8,
    0x51,0xa3,0x40,0x8f,0x92,0x9d,0x38,0xf5,0xbc,0xb6,0xda,0x21,0x10,0xff,0xf3,0xd2,
    0xcd,0x0c,0x13,0xec,0x5f,0x97,0x44,0x17,0xc4,0xa7,0x7e,0x3d,0x64,0x5d,0x19,0x73,
    0x60,0x81,0x4f,0xdc,0x22,0x2a,0x90,0x88,0x46,0xee,0xb8,0x14,0xde,0x5e,0x0b,0xdb,
    0xe0,0x32,0x3a,0x0a,0x49,0x06,0x24,0x5c,0xc2,0xd3,0xac,0x62,0x91,0x95,0xe4,0x79,
    0xe7,0xc8,0x37,0x6d,0x8d,0xd5,0x4e,0xa9,0x6c,0x56,0xf4,0xea,0x65,0x7a,0xae,0x08,
    0xba,0x78,0x25,0x2e,0x1c,0xa6,0xb4,0xc6,0xe8,0xdd,0x74,0x1f,0x4b,0xbd,0x8b,0x8a,
    0x70,0x3e,0xb5,0x66,0x48,0x03,0xf6,0x0e,0x61,0x35,0x57,0xb9,0x86,0xc1,0x1d,0x9e,
    0xe1,0xf8,0x98,0x11,0x69,0xd9,0x8e,0x94,0x9b,0x1e,0x87,0xe9,0xce,0x55,0x28,0xdf,
    0x8c,0xa1,0x89,0x0d,0xbf,0xe6,0x42,0x68,0x41,0x99,0x2d,0x0f,0xb0,0x54,0xbb,0x16
]

# ─── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; margin-top:-3.5rem; padding-bottom:1rem;">
        <div style="font-size:2.5rem; margin-bottom:0rem;">🔐</div>
        <div style="font-size:1.1rem; font-weight:700; color:#4f98a3;">S-Box Constructor</div>
        <div style="font-size:0.78rem; color:#8892a4; margin-top:0.2rem;">GF(2⁸) · Algebraic Method</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### ⚙️ Parameter Konstruksi")
    st.markdown("---")

    poly_choice = st.selectbox(
        "Polinomial Irreducible",
        options=list(NAMED_POLYS.keys()),
        index=0,
        help="Polinomial modulus untuk GF(2⁸). Default AES = 0x11B"
    )
    poly_val = NAMED_POLYS[poly_choice]

    st.markdown("<br>", unsafe_allow_html=True)
    affine_const = st.number_input(
        "Konstanta Affine Transform (hex)",
        min_value=0, max_value=255,
        value=0x63,
        format="%d",
        help="Konstanta c dalam transformasi affine. Default AES = 0x63 (99 desimal)"
    )
    st.caption(f"Nilai saat ini: `0x{affine_const:02X}` = `{affine_const}` desimal")

    st.markdown("<br>", unsafe_allow_html=True)
    compare_aes = st.toggle("Bandingkan dengan AES S-box", value=True)
    show_heatmap = st.toggle("Tampilkan Heatmap", value=True)
    show_scatter = st.toggle("Tampilkan Scatter Plot", value=True)

    st.markdown("---")
    st.markdown("""
    <div style="text-align:center; font-size:0.82rem; padding: 0.6rem; background: rgba(1,105,111,0.05); border-radius: 8px; border: 1px solid rgba(79,152,163,0.2);">
        <div style="margin-bottom: 0.4rem;">
            <a href="./" target="_self" style="color:#a8d8dc; text-decoration:none; font-weight:600; transition:color 0.2s;">🏠 Home</a> 
        </div>
        <div>
            <a href="sbox1" target="_self" style="color:#4f98a3; text-decoration:none; font-weight:700;">Konstruksi</a> 
            <span style="color:#2a2d3e; margin: 0 0.3rem;">|</span> 
            <a href="sbox2" target="_self" style="color:#a8d8dc; text-decoration:none; font-weight:600; transition:color 0.2s;">Evaluasi</a> 
            <span style="color:#2a2d3e; margin: 0 0.3rem;">|</span> 
            <a href="sbox3" target="_self" style="color:#a8d8dc; text-decoration:none; font-weight:600; transition:color 0.2s;">Komparasi</a>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ─── COMPUTE ───────────────────────────────────────────────────────────────────
with st.spinner("Menghitung S-box..."):
    sbox = build_sbox(poly_val, affine_const)
    validation = validate_sbox(sbox)
    is_aes_match = (sbox == AES_SBOX)


# ─── HERO ──────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="hero-section">
    <div class="hero-title"><span style="-webkit-text-fill-color: initial; background: none;">🔐</span> Konstruksi S-Box pada GF(2⁸)</div>
    <div class="hero-subtitle">
        Metode Aljabar: Invers Multiplikatif + Transformasi Affine<br>
        <span style="color:#4f98a3; font-family:'JetBrains Mono',monospace; font-size:0.9rem;">
            m(x) = {bin(poly_val)} &nbsp;·&nbsp; Poly: 0x{poly_val:03X} &nbsp;·&nbsp; Affine const: 0x{affine_const:02X}
        </span>
    </div>
</div>
""", unsafe_allow_html=True)


# ─── VALIDATION METRICS ────────────────────────────────────────────────────────
st.markdown('<div class="step-badge">📋 Validasi S-Box</div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
with col1:
    status = "✅ Valid" if validation["bijective"] else "❌ Gagal"
    color = "status-ok" if validation["bijective"] else "status-warn"
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{"256"}</div>
        <div class="metric-label">Nilai Unik</div>
        <div class="metric-status {color}">{status}</div>
    </div>""", unsafe_allow_html=True)

with col2:
    bal = "✅ Balanced" if validation["balanced"] else "❌ Tidak"
    bcolor = "status-ok" if validation["balanced"] else "status-warn"
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">8→8</div>
        <div class="metric-label">Bit Mapping</div>
        <div class="metric-status {bcolor}">{bal}</div>
    </div>""", unsafe_allow_html=True)

with col3:
    fp = len(validation["fixed_points"])
    fcolor = "status-ok" if fp == 0 else "status-warn"
    fstatus = "✅ Tidak ada" if fp == 0 else f"⚠️ {fp} titik"
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{fp}</div>
        <div class="metric-label">Fixed Points</div>
        <div class="metric-status {fcolor}">{fstatus}</div>
    </div>""", unsafe_allow_html=True)

with col4:
    aes_s = "✅ Identik" if is_aes_match else "⚠️ Berbeda"
    aes_c = "status-ok" if is_aes_match else "status-warn"
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{"AES"}</div>
        <div class="metric-label">Kompatibilitas</div>
        <div class="metric-status {aes_c}">{aes_s}</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# ─── MAIN COLUMNS ──────────────────────────────────────────────────────────────
left_col, right_col = st.columns([3, 2], gap="large")

with left_col:
    # ── S-BOX TABLE ────────────────────────────────────────────────────────────
    st.markdown('<div class="step-badge">🗺️ Tabel S-Box (Format Hex 16×16)</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="info-box">
        Setiap sel menunjukkan nilai <code>S(x)</code> dalam heksadesimal.
        Baris = nibble tinggi input, Kolom = nibble rendah input.
        Contoh: <code>S(0x53)</code> ada di baris <code>50</code>, kolom <code>3</code>.
    </div>
    """, unsafe_allow_html=True)

    sbox_matrix = np.array(sbox).reshape(16, 16)
    df_hex = pd.DataFrame(
        [[f"{v:02X}" for v in row] for row in sbox_matrix],
        index=[f"{i*16:02X}" for i in range(16)],
        columns=[f"+{j:X}" for j in range(16)]
    )
    st.dataframe(df_hex, use_container_width=True, height=380)

    # ── HEATMAP ────────────────────────────────────────────────────────────────
    if show_heatmap:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="step-badge">🌡️ Heatmap Distribusi Nilai</div>', unsafe_allow_html=True)

        fig, ax = plt.subplots(figsize=(10, 6))
        fig.patch.set_facecolor('#1a1d2e')
        ax.set_facecolor('#1a1d2e')

        cmap = 'viridis'
        im = ax.imshow(sbox_matrix, cmap=cmap, aspect='auto', interpolation='nearest')

        ax.set_xticks(range(16))
        ax.set_yticks(range(16))
        ax.set_xticklabels([f'+{i:X}' for i in range(16)], fontsize=8, color='#8892a4', fontfamily='monospace')
        ax.set_yticklabels([f'{i*16:02X}' for i in range(16)], fontsize=8, color='#8892a4', fontfamily='monospace')
        ax.tick_params(colors='#8892a4')

        cbar = plt.colorbar(im, ax=ax)
        cbar.ax.yaxis.set_tick_params(color='#8892a4')
        plt.setp(cbar.ax.yaxis.get_ticklabels(), color='#8892a4', fontsize=8)
        cbar.set_label('Nilai Output (0–255)', color='#8892a4', fontsize=9)

        ax.set_title('Distribusi Nilai S-Box', color='#4f98a3', fontsize=12, pad=12)
        ax.set_xlabel('Nibble Rendah Input', color='#8892a4', fontsize=9)
        ax.set_ylabel('Nibble Tinggi Input', color='#8892a4', fontsize=9)

        for spine in ax.spines.values():
            spine.set_edgecolor('#2a2d3e')

        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close()


with right_col:
    # ── INPUT LOOKUP ───────────────────────────────────────────────────────────
    st.markdown('<div class="step-badge">🔎 Lookup S(x)</div>', unsafe_allow_html=True)
    st.markdown("""<div class="info-box">Masukkan nilai input untuk melihat hasil <code>S(x)</code> secara instan.</div>""",
                unsafe_allow_html=True)

    lookup_val = st.slider("Input x (desimal)", 0, 255, 83,
                           help="Geser untuk pilih nilai input")
    lv = sbox[lookup_val]
    inv_lv = build_inverse_table(poly_val)[lookup_val]

    st.markdown(f"""
    <div class="crypto-card" style="text-align:center; padding:1.5rem;">
        <div style="font-size:0.78rem; color:#8892a4; text-transform:uppercase; letter-spacing:0.08em; margin-bottom:0.8rem;">
            Hasil Komputasi
        </div>
        <div style="display:flex; justify-content:space-around; gap:1rem;">
            <div>
                <div style="font-size:0.75rem; color:#8892a4; margin-bottom:0.3rem;">Input x</div>
                <div style="font-size:1.4rem; font-weight:700; color:#e2e8f0; font-family:'JetBrains Mono',monospace;">
                    0x{lookup_val:02X}
                </div>
                <div style="font-size:0.75rem; color:#4a5568;">= {lookup_val} desimal</div>
            </div>
            <div style="color:#2a2d3e; font-size:2rem; align-self:center;">→</div>
            <div>
                <div style="font-size:0.75rem; color:#8892a4; margin-bottom:0.3rem;">x⁻¹ di GF(2⁸)</div>
                <div style="font-size:1.4rem; font-weight:700; color:#a8d8dc; font-family:'JetBrains Mono',monospace;">
                    0x{inv_lv:02X}
                </div>
                <div style="font-size:0.75rem; color:#4a5568;">= {inv_lv} desimal</div>
            </div>
            <div style="color:#2a2d3e; font-size:2rem; align-self:center;">→</div>
            <div>
                <div style="font-size:0.75rem; color:#8892a4; margin-bottom:0.3rem;">S(x) output</div>
                <div style="font-size:1.8rem; font-weight:700; color:#4f98a3; font-family:'JetBrains Mono',monospace;">
                    0x{lv:02X}
                </div>
                <div style="font-size:0.75rem; color:#4a5568;">= {lv} desimal</div>
            </div>
        </div>
        <div style="margin-top:1rem; font-size:0.8rem; color:#4a5568;">
            S({lookup_val}) = affine(inv(0x{lookup_val:02X})) = affine(0x{inv_lv:02X}) = <strong style="color:#4f98a3;">0x{lv:02X}</strong>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── SCATTER PLOT ───────────────────────────────────────────────────────────
    if show_scatter:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="step-badge">📈 Scatter: Input vs Output</div>', unsafe_allow_html=True)

        fig2, ax2 = plt.subplots(figsize=(5.5, 5))
        fig2.patch.set_facecolor('#1a1d2e')
        ax2.set_facecolor('#1a1d2e')

        xs = list(range(256))
        ys = sbox

        scatter = ax2.scatter(xs, ys, c=ys, cmap='viridis', s=6, alpha=0.85, linewidths=0)
        ax2.set_xlabel('Input x', color='#8892a4', fontsize=9)
        ax2.set_ylabel('S(x) Output', color='#8892a4', fontsize=9)
        ax2.set_title('Pemetaan Input → Output', color='#4f98a3', fontsize=11, pad=10)
        ax2.tick_params(colors='#8892a4', labelsize=8)
        for spine in ax2.spines.values():
            spine.set_edgecolor('#2a2d3e')
        ax2.set_xlim(-5, 260)
        ax2.set_ylim(-5, 260)

        plt.tight_layout()
        st.pyplot(fig2, use_container_width=True)
        plt.close()

    # ── AES COMPARE ────────────────────────────────────────────────────────────
    if compare_aes and not is_aes_match:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="step-badge">⚖️ Perbedaan vs AES</div>', unsafe_allow_html=True)
        diffs = [(i, sbox[i], AES_SBOX[i]) for i in range(256) if sbox[i] != AES_SBOX[i]]
        st.caption(f"{len(diffs)} nilai berbeda dari AES S-box standar")
        if len(diffs) <= 50:
            df_diff = pd.DataFrame(diffs, columns=["x (dec)", "S(x) hex-gen", "S(x) AES"])
            df_diff["x (dec)"] = df_diff["x (dec)"].apply(lambda v: f"0x{v:02X}")
            df_diff["S(x) hex-gen"] = df_diff["S(x) hex-gen"].apply(lambda v: f"0x{v:02X}")
            df_diff["S(x) AES"] = df_diff["S(x) AES"].apply(lambda v: f"0x{v:02X}")
            st.dataframe(df_diff, use_container_width=True, height=200)


# ─── BOTTOM SECTION ────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown('<div class="step-badge">📥 Download S-Box</div>', unsafe_allow_html=True)

dl1, dl2, dl3 = st.columns(3)

with dl1:
    csv_buf = io.StringIO()
    writer = csv.writer(csv_buf)
    writer.writerow([""] + [f"+{j:X}" for j in range(16)])
    for i in range(16):
        writer.writerow([f"{i*16:02X}"] + [f"0x{sbox[i*16+j]:02X}" for j in range(16)])
    st.download_button(
        "⬇️ Download CSV (Tabel Hex)",
        data=csv_buf.getvalue(),
        file_name="sbox_result.csv",
        mime="text/csv",
        use_container_width=True
    )

with dl2:
    raw_bytes = bytes(sbox)
    st.download_button(
        "⬇️ Download Binary (.bin)",
        data=raw_bytes,
        file_name="sbox_result.bin",
        mime="application/octet-stream",
        use_container_width=True
    )

with dl3:
    py_code = f"""# S-Box GF(2^8) — Generated
# Poly: 0x{poly_val:03X} | Affine const: 0x{affine_const:02X}
SBOX = {sbox}

# Lookup: S(x)
def sbox_lookup(x):
    return SBOX[x & 0xFF]
"""
    st.download_button(
        "⬇️ Download Python (.py)",
        data=py_code,
        file_name="sbox_result.py",
        mime="text/plain",
        use_container_width=True
    )

# ── FULL ARRAY DISPLAY ─────────────────────────────────────────────────────────
with st.expander("🔢 Lihat Array Lengkap S-Box (Desimal)"):
    arr_str = "SBOX = [\n"
    for i in range(0, 256, 16):
        arr_str += "    " + ", ".join(f"{sbox[j]:3d}" for j in range(i, i+16)) + ",\n"
    arr_str += "]"
    st.code(arr_str, language="python")

with st.expander("🔢 Lihat Array Lengkap S-Box (Hex)"):
    arr_hex = "SBOX = [\n"
    for i in range(0, 256, 16):
        arr_hex += "    " + ", ".join(f"0x{sbox[j]:02X}" for j in range(i, i+16)) + ",\n"
    arr_hex += "]"
    st.code(arr_hex, language="python")

with st.expander("📖 Penjelasan Alur Konstruksi"):
    st.markdown(f"""
**Langkah 1 — GF(2⁸) Setup**
- Field terbatas dengan 256 elemen (0x00–0xFF)
- Polinomial irreducible: `0x{poly_val:03X}`
- Setiap elemen adalah polinomial derajat ≤7 dengan koefisien biner

**Langkah 2 — Invers Multiplikatif**
- Untuk setiap elemen `x`, cari `x⁻¹` sehingga `x · x⁻¹ ≡ 1 (mod m(x))`
- Konvensi: `invers(0) = 0`
- Invers inilah sumber **non-linearitas** utama S-box

**Langkah 3 — Transformasi Affine**
- Terapkan transformasi linear: `b_i = b'_i ⊕ b'_(i+4)%8 ⊕ b'_(i+5)%8 ⊕ b'_(i+6)%8 ⊕ b'_(i+7)%8 ⊕ c_i`
- Konstanta affine: `c = 0x{affine_const:02X}`
- Tujuan: menghilangkan fixed point dan meningkatkan SAC

**Hasil:**
- S-box bijektif ({'✅ Ya' if validation['bijective'] else '❌ Tidak'})
- Fixed point: {len(validation['fixed_points'])} titik
- {'✅ Identik dengan AES S-box standar' if is_aes_match else f'⚠️ Berbeda dari AES (poly atau affine const berbeda)'}
    """)
