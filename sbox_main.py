import streamlit as st
import subprocess
import sys
import os

# ─── PAGE CONFIG ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="S-Box Studio · GF(2⁸)",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://api.fontshare.com/v2/css?f[]=satoshi@300,400,500,700,900&display=swap');
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&display=swap');

html, body, [class*="css"] { font-family: 'Satoshi', sans-serif !important; }

.stApp {
    background: linear-gradient(135deg, #080c16 0%, #0a0e1a 40%, #0c1220 100%);
    min-height: 100vh;
}

MainMenu {visibility: hidden;} /* three dots on top right */
footer {visibility: hidden;} /* bottom */
header {visibility: hidden;} /* top bar */

/* Menyembunyikan sidebar bawaan Multipage App di halaman utama */
[data-testid="stSidebar"] { display: none !important; }
[data-testid="collapsedControl"] { display: none !important; }

/* Hero */
.hero-wrap {
    text-align: center;
    padding: 4rem 2rem 3rem;
    position: relative;
}
.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    background: rgba(1,105,111,0.15);
    border: 1px solid rgba(79,152,163,0.35);
    border-radius: 999px;
    padding: 0.35rem 1.1rem;
    font-size: 0.78rem;
    color: #4f98a3;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 1.5rem;
}
.hero-title {
    font-size: clamp(2.8rem, 6vw, 5rem);
    font-weight: 900;
    line-height: 1.05;
    margin-bottom: 1rem;
    background: linear-gradient(135deg, #ffffff 0%, #a8d8dc 40%, #4f98a3 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: -0.02em;
}
.hero-subtitle {
    font-size: 1.1rem;
    color: #6b7a8f;
    max-width: 560px;
    margin: 0 auto 0.8rem;
    line-height: 1.7;
}
.hero-mono {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.82rem;
    color: #7ab8c4;
    margin-top: 0.5rem;
}

/* Glow orb */
.glow-orb {
    position: fixed;
    top: -100px; left: 50%;
    transform: translateX(-50%);
    width: 600px; height: 400px;
    background: radial-gradient(ellipse, rgba(1,105,111,0.07) 0%, transparent 70%);
    pointer-events: none;
    z-index: 0;
}

/* Card grid */
.card-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1.5rem;
    max-width: 1100px;
    margin: 0 auto;
    padding: 0 2rem 4rem;
}

/* Module card */
.module-card {
    background: linear-gradient(145deg, #111520 0%, #161b2e 50%, #12182a 100%);
    border: 1px solid #1e2540;
    border-radius: 20px;
    padding: 2rem;
    position: relative;
    overflow: hidden;
    transition: all 0.3s cubic-bezier(0.16,1,0.3,1);
    cursor: pointer;
    text-decoration: none;
    display: block;
}
.module-card::before {
    content: '';
    position: absolute;
    inset: 0;
    border-radius: 20px;
    padding: 1px;
    background: linear-gradient(135deg, rgba(79,152,163,0.2), transparent 60%);
    -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
    mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
    -webkit-mask-composite: xor;
    mask-composite: exclude;
    pointer-events: none;
}
.module-card:hover {
    transform: translateY(-6px);
    border-color: transparent;
    box-shadow: 0 20px 60px rgba(0,0,0,0.5), 0 0 0 1px rgba(79,152,163,0.3);
}

/* Card accent glow per card */
.card-glow {
    position: absolute;
    top: -40px; right: -40px;
    width: 160px; height: 160px;
    border-radius: 50%;
    pointer-events: none;
    opacity: 0.6;
}
.glow-teal   { background: radial-gradient(circle, rgba(1,105,111,0.25) 0%, transparent 70%); }
.glow-purple { background: radial-gradient(circle, rgba(122,57,187,0.2) 0%, transparent 70%); }
.glow-gold   { background: radial-gradient(circle, rgba(209,153,0,0.2) 0%, transparent 70%); }

/* Card number */
.card-number {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    color: #4a6a7a;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 1.2rem;
}

/* Card icon */
.card-icon {
    font-size: 2.8rem;
    margin-bottom: 1rem;
    display: block;
    line-height: 1;
}

/* Card title */
.card-title {
    font-size: 1.4rem;
    font-weight: 700;
    color: #e2e8f0;
    margin-bottom: 0.5rem;
    line-height: 1.2;
}

/* Card desc */
.card-desc {
    font-size: 0.88rem;
    color: #5a6a7e;
    line-height: 1.65;
    margin-bottom: 1.5rem;
}

/* Card features */
.card-features {
    display: flex;
    flex-direction: column;
    gap: 0.35rem;
    margin-bottom: 1.5rem;
}
.card-feat {
    font-size: 0.78rem;
    color: #4a5a6e;
    display: flex;
    align-items: center;
    gap: 0.4rem;
}
.feat-dot {
    width: 5px; height: 5px;
    border-radius: 50%;
    flex-shrink: 0;
}
.dot-teal   { background: #4f98a3; }
.dot-purple { background: #9b6fd4; }
.dot-gold   { background: #d4a017; }

/* Card CTA */
.card-cta {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding-top: 1.2rem;
    border-top: 1px solid #1e2540;
}
.cta-label {
    font-size: 0.82rem;
    font-weight: 600;
    letter-spacing: 0.05em;
}
.cta-teal   { color: #4f98a3; }
.cta-purple { color: #9b6fd4; }
.cta-gold   { color: #d4a017; }
.cta-arrow {
    font-size: 1.1rem;
    transition: transform 0.2s ease;
}
.module-card:hover .cta-arrow { transform: translateX(4px); }

/* Stats bar */
.stats-bar {
    display: flex;
    justify-content: center;
    gap: 3rem;
    padding: 1.5rem 2rem;
    margin: 0 auto 3rem;
    max-width: 600px;
    background: rgba(255,255,255,0.02);
    border: 1px solid #1a2030;
    border-radius: 14px;
}
.stat-item { text-align: center; }
.stat-val {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.4rem;
    font-weight: 700;
    color: #4f98a3;
}
.stat-lbl {
    font-size: 0.72rem;
    color: #4a6a7a;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-top: 0.2rem;
}

/* Divider */
.section-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, #1e2540 30%, #1e2540 70%, transparent);
    margin: 0 auto 3rem;
    max-width: 900px;
}

/* Info strip */
.info-strip {
    max-width: 900px;
    margin: 0 auto 3rem;
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
    padding: 0 2rem;
}
.info-chip {
    background: rgba(255,255,255,0.02);
    border: 1px solid #1a2030;
    border-radius: 10px;
    padding: 0.9rem 1.2rem;
    font-size: 0.82rem;
    color: #4a5a6e;
    line-height: 1.5;
}
.info-chip strong { color: #6b8fa3; font-weight: 600; }

/* Flow section */
.flow-wrap {
    max-width: 800px;
    margin: 0 auto 4rem;
    padding: 0 2rem;
    text-align: center;
}
.flow-title {
    font-size: 0.78rem;
    color: #4a6a7a;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin-bottom: 1.2rem;
}
.flow-steps {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    flex-wrap: wrap;
}
.flow-step {
    background: rgba(1,105,111,0.08);
    border: 1px solid rgba(79,152,163,0.15);
    border-radius: 8px;
    padding: 0.5rem 1rem;
    font-size: 0.82rem;
    color: #4f98a3;
    font-family: 'JetBrains Mono', monospace;
}
.flow-arrow { color: #1e2d3e; font-size: 1rem; }
</style>
""", unsafe_allow_html=True)


# ─── GLOW ──────────────────────────────────────────────────────────────────────
st.markdown('<div class="glow-orb"></div>', unsafe_allow_html=True)


# ─── HERO ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-wrap">
    <div class="hero-badge">🔐 &nbsp; Cryptography · GF(2⁸) · S-Box Studio</div>
    <div class="hero-title">S-Box Studio</div>
    <div class="hero-subtitle">
        Platform lengkap untuk konstruksi, evaluasi, dan analisis komparatif
        S-Box berbasis Galois Field GF(2⁸) — metode aljabar AES.
    </div>
    <div class="hero-mono">m(x) = x⁸ + x⁴ + x³ + x + 1 &nbsp;·&nbsp; 256 elemen &nbsp;·&nbsp; 30 polinomial irreducible</div>
</div>
""", unsafe_allow_html=True)


# ─── STATS BAR ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="stats-bar">
    <div class="stat-item">
        <div class="stat-val">256</div>
        <div class="stat-lbl">Elemen S-Box</div>
    </div>
    <div class="stat-item">
        <div class="stat-val">6</div>
        <div class="stat-lbl">Parameter Uji</div>
    </div>
    <div class="stat-item">
        <div class="stat-val">30</div>
        <div class="stat-lbl">Poly Irreducible</div>
    </div>
    <div class="stat-item">
        <div class="stat-val">3840</div>
        <div class="stat-lbl">Variasi S-Box</div>
    </div>
</div>
""", unsafe_allow_html=True)


# ─── MODULE CARDS ──────────────────────────────────────────────────────────────
st.markdown('<div class="card-grid">', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3, gap="large")

with col1:
    st.markdown("""
    <a href="sbox1" target="_self" style="text-decoration: none; color: inherit;">
    <div class="module-card">
        <div class="card-glow glow-teal"></div>
        <div class="card-number">01 · Construction</div>
        <span class="card-icon">⚙️</span>
        <div class="card-title">Konstruksi<br>S-Box</div>
        <div class="card-desc">
            Bangun S-box GF(2⁸) dari nol menggunakan
            invers multiplikatif dan transformasi affine.
            Parameter bisa diubah secara interaktif.
        </div>
        <div class="card-features">
            <div class="card-feat">
                <div class="feat-dot dot-teal"></div>
                Pilih dari 30 polinomial irreducible
            </div>
            <div class="card-feat">
                <div class="feat-dot dot-teal"></div>
                Ubah konstanta affine transform
            </div>
            <div class="card-feat">
                <div class="feat-dot dot-teal"></div>
                Tabel hex 16×16 + heatmap + scatter
            </div>
            <div class="card-feat">
                <div class="feat-dot dot-teal"></div>
                Download CSV / Python / Binary
            </div>
        </div>
        <div class="card-cta">
            <span class="cta-label cta-teal">Buka Konstruksi</span>
            <span class="cta-arrow cta-teal">→</span>
        </div>
    </div>
    </a>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <a href="sbox2" target="_self" style="text-decoration: none; color: inherit;">
    <div class="module-card">
        <div class="card-glow glow-purple"></div>
        <div class="card-number">02 · Evaluation</div>
        <span class="card-icon">🔬</span>
        <div class="card-title">Evaluasi<br>6 Parameter</div>
        <div class="card-desc">
            Uji kualitas kriptografis S-box dengan
            6 parameter standar. Upload hasil dari
            modul konstruksi atau gunakan AES default.
        </div>
        <div class="card-features">
            <div class="card-feat">
                <div class="feat-dot dot-purple"></div>
                NL · SAC · BIC-NL · BIC-SAC
            </div>
            <div class="card-feat">
                <div class="feat-dot dot-purple"></div>
                LAP · DAP vs referensi AES
            </div>
            <div class="card-feat">
                <div class="feat-dot dot-purple"></div>
                Upload CSV / PY / BIN dari sbox1
            </div>
            <div class="card-feat">
                <div class="feat-dot dot-purple"></div>
                Radar chart + tabel perbandingan
            </div>
        </div>
        <div class="card-cta">
            <span class="cta-label cta-purple">Buka Evaluasi</span>
            <span class="cta-arrow cta-purple">→</span>
        </div>
    </div>
    </a>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <a href="sbox3" target="_self" style="text-decoration: none; color: inherit;">
    <div class="module-card">
        <div class="card-glow glow-gold"></div>
        <div class="card-number">03 · Comparison</div>
        <span class="card-icon">📊</span>
        <div class="card-title">Analisis<br>Komparatif</div>
        <div class="card-desc">
            Bandingkan semua 30 polinomial irreducible
            sekaligus. Temukan kombinasi terbaik
            berdasarkan ranking NL, SAC, LAP, dan DAP.
        </div>
        <div class="card-features">
            <div class="card-feat">
                <div class="feat-dot dot-gold"></div>
                Batch compute 30 S-box sekaligus
            </div>
            <div class="card-feat">
                <div class="feat-dot dot-gold"></div>
                Ranking otomatis by parameter
            </div>
            <div class="card-feat">
                <div class="feat-dot dot-gold"></div>
                Heatmap komparatif antar poly
            </div>
            <div class="card-feat">
                <div class="feat-dot dot-gold"></div>
                Export tabel ranking ke CSV
            </div>
        </div>
        <div class="card-cta">
            <span class="cta-label cta-gold">Buka Komparasi</span>
            <span class="cta-arrow cta-gold">→</span>
        </div>
    </div>
    </a>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)


# ─── DIVIDER ───────────────────────────────────────────────────────────────────
st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)


# ─── INFO STRIP ────────────────────────────────────────────────────────────────
st.markdown("""
<div class="info-strip">
    <div class="info-chip">
        <strong>Metode Konstruksi</strong><br>
        Invers multiplikatif di GF(2⁸) diikuti transformasi affine — metode yang sama digunakan AES (FIPS 197).
    </div>
    <div class="info-chip">
        <strong>Parameter Evaluasi</strong><br>
        NL, SAC, BIC-NL, BIC-SAC mengukur ketahanan linear. LAP & DAP mengukur ketahanan diferensial.
    </div>
    <div class="info-chip">
        <strong>Referensi</strong><br>
        AES S-box (poly <code>0x11B</code>, const <code>0x63</code>) digunakan sebagai baseline perbandingan terbaik.
    </div>
</div>
""", unsafe_allow_html=True)


# ─── PROFILE ───────────────────────────────────────────────────────────────────
import base64
import os

try:
    if os.path.exists('foto.png'):
        with open('foto.png', 'rb') as f:
            img_b64 = base64.b64encode(f.read()).decode()
        
        profile_html = f"""
        <div style="display: flex; justify-content: center; margin: 4rem 0 1rem 0;">
            <div style="background: linear-gradient(145deg, #0d1120, #161b2e); border: 1px solid #1a2030; border-radius: 20px; padding: 1.5rem 2.5rem; display: flex; align-items: center; gap: 1.8rem; box-shadow: 0 8px 32px rgba(0,0,0,0.4); position: relative; overflow: hidden; transition: transform 0.3s ease, box-shadow 0.3s ease;" onmouseover="this.style.transform='translateY(-5px)'; this.style.boxShadow='0 12px 40px rgba(79,152,163,0.3)';" onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 8px 32px rgba(0,0,0,0.4)';">
                <div style="position: absolute; top: -50%; left: -50%; width: 200%; height: 200%; background: radial-gradient(circle, rgba(79,152,163,0.06) 0%, transparent 60%); pointer-events: none;"></div>
                <div style="position: relative; z-index: 1;">
                    <div style="width: 75px; height: 100px; border-radius: 10%; padding: 3px; background: linear-gradient(135deg, #4f98a3, #9b6fd4); box-shadow: 0 0 20px rgba(79,152,163,0.3);">
                        <div style="width: 100%; height: 100%; border-radius: 10%; overflow: hidden; background: #080c16;">
                            <img src="data:image/png;base64,{img_b64}" style="width: 100%; height: 100%; object-fit: cover; transform: scale(1);">
                        </div>
                    </div>
                </div>
                <div style="position: relative; z-index: 1;">
                    <div style="display: inline-block; font-size: 0.68rem; color: #a8d8dc; background: rgba(79,152,163,0.15); padding: 0.2rem 0.7rem; border-radius: 999px; font-family: 'JetBrains Mono', monospace; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 0.5rem; font-weight: 700; border: 1px solid rgba(79,152,163,0.3);">
                        Mahasiswa
                    </div>
                    <div style="font-size: 1.5rem; font-weight: 800; color: #ffffff; margin-bottom: 0.25rem; letter-spacing: -0.01em;">Franki Setyo Wargo</div>
                    <div style="display: flex; align-items: center; gap: 0.5rem; font-size: 0.85rem; color: #7ab8c4; font-family: 'JetBrains Mono', monospace; font-weight: 500;">
                        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1 0-5H20"></path></svg>
                        NIM: <span style="color:#e2e8f0;">2504240005</span>
                    </div>
                    <div style="display: flex; align-items: center; gap: 0.5rem; font-size: 0.85rem; color: #7ab8c4; font-family: 'JetBrains Mono', monospace; font-weight: 500; margin-top: 0.4rem;">
                        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M22 10v6M2 10l10-5 10 5-10 5z"></path><path d="M6 12v5c3 3 9 3 12 0v-5"></path></svg>
                        <span style="color:#e2e8f0;">Universitas Negeri Semarang</span>
                    </div>
                </div>
            </div>
        </div>
        """
        st.markdown(profile_html, unsafe_allow_html=True)
except Exception as e:
    pass

# ─── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; padding-bottom:2rem;">
    <div style="font-family:'JetBrains Mono',monospace; font-size:0.7rem; color:#4a6a7a; letter-spacing:0.1em;">
        TUGAS MATKUL KRIPTOGRAFI LANJUT &nbsp;·&nbsp; KONSTRUKSI S-BOX GF(2⁸) &nbsp;·&nbsp; METODE ALJABAR
    </div>
</div>
""", unsafe_allow_html=True)


