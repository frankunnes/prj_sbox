import streamlit as st
import numpy as np
import pandas as pd

# -----------------------------------------------------------------------------
# KONSTANTA & FUNGSI DASAR GF(2^8)
# -----------------------------------------------------------------------------
FIELD_SIZE = 256
IRREDUCIBLE_POLY = 0x11B

def gf_add(a, b):
    return a ^ b

def gf_multiply(a, b, poly=IRREDUCIBLE_POLY):
    result = 0
    for _ in range(8):
        if b & 1:
            result ^= a
        hi_bit = a & 0x80
        a = (a << 1) & 0xFF
        if hi_bit:
            a ^= (poly & 0xFF)
        b >>= 1
    return result

@st.cache_data
def get_inverse_table():
    def gf_inverse(a, poly=IRREDUCIBLE_POLY):
        if a == 0:
            return 0
        for b in range(1, FIELD_SIZE):
            if gf_multiply(a, b, poly) == 1:
                return b
        return 0
    return [gf_inverse(x) for x in range(FIELD_SIZE)]

def affine_transform(byte):
    AFFINE_CONST = 0x63
    result = 0
    for i in range(8):
        b = (byte >> i) & 1
        b ^= (byte >> ((i + 4) % 8)) & 1
        b ^= (byte >> ((i + 5) % 8)) & 1
        b ^= (byte >> ((i + 6) % 8)) & 1
        b ^= (byte >> ((i + 7) % 8)) & 1
        b ^= (AFFINE_CONST >> i) & 1
        result |= (b << i)
    return result

@st.cache_data
def get_sbox():
    inv_table = get_inverse_table()
    return [affine_transform(inv_table[x]) for x in range(FIELD_SIZE)]

# -----------------------------------------------------------------------------
# KONFIGURASI HALAMAN
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="S-Box Konstruktor GF(2^8)",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# STYLING KUSTOM (CSS)
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    /* Styling elegan untuk dataframe */
    .stDataFrame {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Judul header lebih modern */
    h1, h2, h3 {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        color: #1f77b4;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# SIDEBAR
# -----------------------------------------------------------------------------
with st.sidebar:
    st.title("Tugas Kriptografi Lanjut")
    st.subheader("Proyek Konstruksi S-Box")
    st.success("👨‍🎓 **Franki SW** — `2504240005`")
    st.divider()
    
    st.header("🎯 Tujuan Aplikasi")
    st.markdown("""
    Aplikasi interaktif ini membahas cara membangun S-box 8×8 (256 elemen) menggunakan pendekatan aljabar pada **Galois Field GF(2⁸)**, 
    yaitu metode yang sama yang digunakan pada algoritma kriptografi **AES (Advanced Encryption Standard)**.
    """)
    
    st.header("📌 Alur Konstruksi")
    st.markdown("""
    1. Memahami struktur GF(2⁸)
    2. Implementasi operasi field: penjumlahan, perkalian, dan invers multiplikatif
    3. Menerapkan transformasi affine
    4. Menghasilkan S-box final dan memvalidasinya
    5. Menyimpan S-box untuk dievaluasi
    """)
    
    st.info("💡 **Petunjuk:** Silakan klik *Tab-Tab* navigasi di layar utama untuk mengikuti setiap alur konstruksi di atas secara interaktif!")

# -----------------------------------------------------------------------------
# HEADER UTAMA
# -----------------------------------------------------------------------------
st.title("🔐 Konstruksi S-box pada GF(2⁸)")
st.markdown("Aplikasi interaktif untuk membangun dan memvisualisasikan **S-box 8×8** menggunakan **Invers Multiplikatif** dan **Transformasi Affine**.")
st.divider()

# -----------------------------------------------------------------------------
# TABS NAVIGASI
# -----------------------------------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs(["📚 Teori GF(2⁸)", "🔄 Tabel Invers", "🧮 Transformasi Affine", "✨ S-box Final"])

with tab1:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("Teori Dasar GF(2⁸)")
        st.markdown("""
        **Galois Field GF(2⁸)** adalah himpunan terbatas dengan **256 elemen** (dari `0x00` hingga `0xFF`).
        Setiap elemen direpresentasikan sebagai **polinomial derajat ≤ 7** dengan koefisien 0 atau 1.
        
        Semua perkalian di GF(2⁸) dilakukan **modulo polinomial irreducible**:
        $$m(x) = x^8 + x^4 + x^3 + x + 1$$
        
        Dalam heksadesimal: `0x11B`
        """)

    with col2:
        st.subheader("Kalkulator GF(2⁸)")
        with st.container(border=True):
            val_a_str = st.text_input("Input A (Hex)", value="57", help="Masukkan nilai hex (00-FF)")
            val_b_str = st.text_input("Input B (Hex)", value="83", help="Masukkan nilai hex (00-FF)")
            
            try:
                val_a = int(val_a_str, 16)
                val_b = int(val_b_str, 16)
                
                res_add = gf_add(val_a, val_b)
                res_mul = gf_multiply(val_a, val_b)
                
                st.markdown(f"**Penjumlahan (+):** `0x{val_a:02X} + 0x{val_b:02X} = 0x{res_add:02X}` (XOR)")
                st.markdown(f"**Pengurangan (-):** `0x{val_a:02X} - 0x{val_b:02X} = 0x{res_add:02X}` (Sama persis dengan penjumlahan)")
                st.markdown(f"**Perkalian (×):** `0x{val_a:02X} * 0x{val_b:02X} = 0x{res_mul:02X}`")
            except ValueError:
                st.error("Harap masukkan format Hexadecimal yang valid (misal: 0A, 1F, FF).")

with tab2:
    st.header("Tabel Invers GF(2⁸)")
    st.markdown("""
    Sebelum membuat S-box, kita hitung terlebih dahulu **tabel invers** untuk semua 256 elemen. Tabel ini memetakan setiap nilai `x` ke invers multiplikatifnya `x⁻¹` di GF(2⁸).
    
    Tabel invers ini adalah **langkah pertama** konstruksi S-box (sebelum affine transform). Sebenarnya, kita bisa saja langsung menyebut tabel invers ini sebagai *raw S-box* sebelum affine.
    """)
    
    inv_table = get_inverse_table()
    inv_matrix = np.array(inv_table).reshape(16, 16)
    
    df_inv = pd.DataFrame(
        [[f"{inv_matrix[i, j]:02X}" for j in range(16)] for i in range(16)],
        index=[f'0x{i*16:02X}' for i in range(16)],
        columns=[f'+0x{j:X}' for j in range(16)]
    )
    
    st.dataframe(df_inv, use_container_width=True)
    
    st.subheader("Verifikasi Sifat Invers")
    st.markdown("Berikut adalah sampel pembuktian bahwa $x \\times x^{-1} = 1$ pada GF(2⁸):")
    
    sample_xs = [0x00, 0x01, 0x02, 0x53, 0xCA, 0xFF]
    verif_data = []
    for x in sample_xs:
        inv = inv_table[x]
        check = gf_multiply(x, inv) if x != 0 else 0
        status = '✅ Valid' if (check == 1 or x == 0) else '❌ Invalid'
        verif_data.append({
            "x": f"0x{x:02X}",
            "x⁻¹": f"0x{inv:02X}",
            "Pembuktian (x * x⁻¹)": f"0x{x:02X} * 0x{inv:02X} = 0x{check:02X}",
            "Status": status
        })
    st.table(pd.DataFrame(verif_data))
    
    col_v1, col_v2, col_v3 = st.columns(3)
    col_v1.metric("Total Elemen", len(inv_table))
    col_v2.metric("Elemen Unik", len(set(inv_table)))

with tab3:
    st.header("Transformasi Affine")
    st.markdown("Transformasi ini diaplikasikan pada hasil invers untuk menghilangkan fixed point (titik tetap) dan meningkatkan properti *Strict Avalanche Criterion* (SAC).")
    
    st.latex(r"b_i = b'_i \oplus b'_{(i+4)\bmod 8} \oplus b'_{(i+5)\bmod 8} \oplus b'_{(i+6)\bmod 8} \oplus b'_{(i+7)\bmod 8} \oplus c_i")
    st.markdown("Konstanta $c = \\texttt{0x63}$")
    
    with st.container(border=True):
        col_test1, col_test2 = st.columns(2)
        with col_test1:
            byte_input_str = st.text_input("Test Invers Byte (Hex)", value="CA")
        with col_test2:
            try:
                byte_input = int(byte_input_str, 16)
                res_affine = affine_transform(byte_input)
                st.metric("Hasil Affine Transform", f"0x{res_affine:02X}")
            except ValueError:
                st.error("Format Hex tidak valid!")

with tab4:
    st.header("✨ S-box Final (AES Standard)")
    st.markdown("S-box akhir dibangun dengan menggabungkan invers multiplikatif dan transformasi affine: $S(x) = \\text{affine}(x^{-1})$")
    
    sbox = get_sbox()
    sbox_matrix = np.array(sbox).reshape(16, 16)
    
    df_sbox = pd.DataFrame(
        [[f"{sbox_matrix[i, j]:02X}" for j in range(16)] for i in range(16)],
        index=[f'0x{i*16:02X}' for i in range(16)],
        columns=[f'+0x{j:X}' for j in range(16)]
    )
    
    # Menambahkan warna elegan pada tabel
    def color_sbox(val):
        return 'background-color: #f8f9fa; color: #333; font-family: monospace; font-weight: bold;'
        
    st.dataframe(df_sbox.style.map(color_sbox), use_container_width=True)
    
    st.subheader("Validasi S-box")
    is_bijective = len(set(sbox)) == FIELD_SIZE
    is_balanced = all(sbox.count(v) == 1 for v in range(FIELD_SIZE))
    fixed_pts = [x for x in range(FIELD_SIZE) if sbox[x] == x]
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Bijectivity (1-to-1)", "✅ Valid" if is_bijective else "❌ Invalid")
    c2.metric("Balancedness", "✅ Valid" if is_balanced else "❌ Invalid")
    c3.metric("Fixed Points", f"{len(fixed_pts)} titik")
    
    if is_bijective and is_balanced and len(fixed_pts) == 0:
        st.success("🎉 **S-box valid!** Konstruksi berhasil dan memenuhi kriteria dasar kriptografi.")
