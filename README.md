# 🔐 S-Box Constructor & Evaluator GF(2⁸)

Proyek ini adalah sebuah aplikasi web berbasis **Streamlit Multipage** yang dirancang untuk kebutuhan Tugas Mata Kuliah Kriptografi Lanjut. Aplikasi ini memfasilitasi pengguna untuk melakukan **Konstruksi**, **Evaluasi**, dan **Komparasi** S-Box (Substitution Box) menggunakan metode aljabar pada lapangan Galois GF(2⁸).

---

## 🌟 Fitur Utama (Multipage App)

Aplikasi ini dibagi menjadi 3 modul utama yang saling terintegrasi:

### 1. 🏠 Halaman Utama (`sbox_main.py`)
Sebagai *landing page* yang memberikan gambaran umum mengenai aplikasi, latar belakang, dan navigasi (berbentuk *card* responsif) menuju ketiga modul fungsional di bawah.

### 2. ⚙️ Modul 1: Konstruksi S-Box (`pages/sbox1.py`)
Membangun S-Box berdasarkan metode Aljabar GF(2⁸).
- Memungkinkan pemilihan dari **30 Polinomial Irreducible**.
- Opsi untuk mengubah **Konstanta Affine**.
- Verifikasi hasil konstruksi (Bijektif & Involutif).
- Fitur visualisasi **Heatmap** dan **Scatter Plot**.
- Export data ke dalam format `.csv`, `.py`, dan `.bin`.

### 3. 🔬 Modul 2: Evaluasi S-Box (`pages/sbox2.py`)
Mengevaluasi ketahanan S-Box berdasarkan 6 Parameter Kriptografis Kritis:
- **Nonlinearity (NL)**
- **Strict Avalanche Criterion (SAC)**
- **Bit Independence Criterion (BIC-NL & BIC-SAC)**
- **Linear Approximation Probability (LAP)**
- **Differential Approximation Probability (DAP)**
- Menyertakan perbandingan visual (*Bar Chart*, *Radar Chart*) dan komparasi dengan spesifikasi AES S-Box bawaan (Polinomial `0x11B`, Konstanta `0x63`).

### 4. 📊 Modul 3: Komparasi Polinomial (`pages/sbox3.py`)
Menganalisis dan membandingkan performa seluruh **30 Polinomial Irreducible** secara otomatis.
- Proses komputasi *batch* dengan *progress bar* dan estimasi waktu cerdas.
- Metrik **Composite Score** untuk mencari spesifikasi alternatif terbaik.
- Fitur visualisasi tinggi: **Heatmap Komparatif**, **Radar Chart Top 5**, **Distribusi Bar**.
- Export laporan ke bentuk **Excel** (`.xlsx`) dan CSV.

---

## 🛠️ Teknologi & Environment

- **Bahasa**: Python 3.12+
- **Framework Web**: [Streamlit](https://streamlit.io/)
- **Data & Komputasi**: `numpy`, `pandas`
- **Visualisasi Data**: `matplotlib`
- **Excel Engine**: `openpyxl`

---

## ⚙️ Panduan Instalasi & Menjalankan Aplikasi

Ikuti langkah-langkah di bawah ini untuk menjalankan aplikasi secara lokal. Disarankan menggunakan **Conda** (seperti yang digunakan pada environment `sbox_env`).

### 1. Persiapan Environment (Conda)
Buka Terminal/Anaconda Prompt, lalu aktifkan *environment* Anda:
```bash
conda activate sbox_env
```

### 2. Instalasi Dependensi
Pastikan Anda berada di direktori proyek (`d:\app\python\PrjSBox`), kemudian install paket Python yang dibutuhkan:
```bash
pip install streamlit pandas numpy matplotlib openpyxl
```

### 3. Menjalankan Aplikasi Streamlit
Jalankan environment:
```bash
conda activate sbox_env
```
Karena ini adalah **Multipage App**, titik masuknya (*entry point*) HANYA MELALUI Halaman Utama (`sbox_main.py`):
```bash
streamlit run sbox_main.py
```
> **Catatan Penting**: Jangan pernah menjalankan file yang ada di dalam folder `pages/` (seperti `streamlit run pages/sbox1.py`). Hal tersebut akan merusak sistem *routing* multipage dari Streamlit. Selalu eksekusi `sbox_main.py`.

Aplikasi akan otomatis terbuka di *browser* Anda pada alamat http://localhost:8501.

---

## 📁 Struktur Direktori

```text
PrjSBox/
│
├── sbox_main.py          # Entry point aplikasi (Halaman Utama)
├── README.md             # Dokumentasi proyek (File ini)
├── requirements.txt      # (Opsional) Daftar dependensi
│
├── .streamlit/           
│   └── config.toml       # Konfigurasi Streamlit (menyembunyikan sidebar nav bawaan)
│
└── pages/                # WAJIB dinamakan "pages" agar dikenali Streamlit
    ├── sbox1.py          # Halaman Modul 1 (Konstruksi)
    ├── sbox2.py          # Halaman Modul 2 (Evaluasi)
    └── sbox3.py          # Halaman Modul 3 (Komparasi Batch)
```

## 🎨 Modifikasi UI/UX Terapan (Streamlit Hacks)
Beberapa kustomisasi UI tingkat lanjut yang diterapkan pada aplikasi ini:
1. **Penghilangan Efek FOUC**: Melalui `.streamlit/config.toml` (`showSidebarNavigation = false`), daftar halaman asli bawaan Streamlit dimatikan sepenuhnya dari akar sehingga tidak terjadi efek "berkedip" saat halaman dimuat.
2. **Navigasi Kustom Interaktif**: Navigasi antar halaman dilakukan melalui perpaduan `st.page_link()` dan tag HTML berdesain *chip/pill* khusus di dalam *sidebar* demi efisiensi ruang dan estetika.
3. **CSS Injeksi (Premium Dark Theme)**: Pewarnaan komponen (*gradient background*, manipulasi *padding*, interaksi *hover*) dimanipulasi murni menggunakan tag `<style>` yang dilempar via fungsi `st.markdown(..., unsafe_allow_html=True)`.

---
*Dibuat untuk keperluan Eksplorasi Kriptografi Lanjut (S-Box Design).*
