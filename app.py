import streamlit as st

# 1. Konfigurasi Halaman
st.set_page_config(page_title="E-Diagnostik PLN UP3", page_icon="⚡", layout="centered")

# 2. CSS ADAPTIF (Mendukung Light & Dark Mode Otomatis)
st.markdown("""
    <style>
    /* Header Utama: Menggunakan transparansi agar serasi di Dark Mode */
    .main-header {
        background: linear-gradient(135deg, #005A9C 0%, #0088CC 100%);
        padding: 20px;
        border-radius: 15px;
        color: #FFFFFF !important;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        margin-bottom: 25px;
    }
    .main-header h2 {
        color: #FFD700 !important;
        margin: 0;
        font-weight: 700;
    }
    .main-header p {
        color: #F0F0F0 !important;
        margin-top: 5px;
        margin-bottom: 0;
        font-size: 14px;
    }
    
    /* Styling Tab Navigasi yang Mengikuti Tema Sistem */
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        background-color: var(--background-secondary-color);
        padding: 6px;
        border-radius: 20px !important;
    }
    .stTabs [data-baseweb="tab"] {
        height: 42px;
        border-radius: 20px !important;
        color: var(--text-color);
        font-weight: 600;
    }
    /* Tab yang sedang dipilih */
    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, #005A9C 0%, #0088CC 100%) !important;
        color: #FFFFFF !important;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
    }

    /* Custom Styling Tombol Utama (Aman di Dark & Light) */
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #005A9C 0%, #0088CC 100%);
        color: #FFFFFF !important;
        border: none;
        padding: 12px;
        border-radius: 10px;
        font-weight: bold;
        font-size: 16px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        color: #FFD700 !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. HEADER UTAMA
st.markdown("""
    <div class="main-header">
        <h2>⚡ E-DIAGNOSTIK kWh METER</h2>
        <p>Layanan Edukasi & Diagnostik Kelistrikan Mandiri — PLN UP3</p>
    </div>
""", unsafe_allow_html=True)

# 4. TAB NAVIGASI
tab1, tab2, tab3, tab4 = st.tabs([
    "🔍 Cek Beban", 
    "🕵️ Kebocoran Arus", 
    "📈 Tambah Daya", 
    "📖 Kode Meteran"
])

# --- TAB 1: CEK BEBAN ---
with tab1:
    st.subheader("🔍 Cek Beban Listrik Real-Time")
    st.info("Hitung persentase beban aktual rumah Anda berdasarkan parameter tegangan dan arus.")
    
    daya_kontrak = st.select_slider("Pilih Daya Terpasang Rumah (VA):", options=[450, 900, 1300, 2200, 3500, 4400, 5500, 6600], value=900)
    
    col1, col2 = st.columns(2)
    with col1:
        v_input = st.number_input("Tegangan (Volt) [Kode 41#]:", value=220.0, step=1.0)
    with col2:
        i_input = st.number_input("Arus (Ampere) [Kode 44#]:", value=2.5, step=0.1)
        
    daya_terpakai = v_input * i_input
    persen_beban = (daya_terpakai / daya_kontrak) * 100
    
    st.markdown("---")
    col_a, col_b = st.columns(2)
    col_a.metric("Daya Terpakai", f"{daya_terpakai:.1f} W")
    col_b.metric("Kapasitas Beban", f"{persen_beban:.1f} %")
    
    if persen_beban > 100:
        st.error("🚨 **STATUS: OVERLOAD!** Pemakaian melebihi batas MCB. Disarankan mengajukan Tambah Daya.")
    elif persen_beban > 80:
        st.warning("⚠️ **STATUS: BEBAN TINGGI!** Kurangi pemakaian alat berdaya besar secara bersamaan.")
    else:
        st.success("✅ **STATUS: AMAN.** Beban listrik dalam kapasitas normal.")

# --- TAB 2: KEBOCORAN ARUS ---
with tab2:
    st.subheader("🕵️‍♂️ Deteksi Kebocoran Arus Listrik")
    
    st.markdown("""
    **Panduan Mandiri Cek Kebocoran Kabel / Grounding:**
    1. Matikan (**OFF**-kan) seluruh sakelar MCB / sekring di dalam rumah.
    2. Ketik **`44#`** (atau **`44 Enter`**) pada tombol meteran PLN Anda.
    3. Lihat angka arus yang muncul di layar meteran, lalu masukkan di bawah:
    """)
    
    arus_bocor = st.number_input("Masukkan Angka Arus dari Meteran (Ampere):", value=0.00, step=0.01, format="%.2f")
    
    if st.button("🔍 Analisa Kebocoran Arus"):
        st.markdown("---")
        if arus_bocor <= 0.05:
            st.success(f"✅ **STATUS: INSTALASI AMAN** (Arus terbaca: {arus_bocor} A)")
            st.write("Tidak terdeteksi adanya kebocoran arus ke tanah. Kabel instalasi rumah Anda dalam kondisi baik.")
        else:
            st.error(f"🚨 **STATUS: TERDETEKSI KEBOCORAN ARUS!** (Arus terbaca: {arus_bocor} A)")
            st.warning("""
            **Dampak Kebocoran Arus:**
            * Pulsa listrik / token Anda akan **terus berkurang (boros)** meskipun semua alat elektronik sudah dimatikan.
            * Berpotensi menimbulkan ketersetruman pada dinding atau bodi peralatan rumah.
            
            **Tindakan yang Disarankan:**
            Segera panggil instalatur listrik terdekat untuk memeriksa pengkabelan dan sistem grounding di rumah Anda.
            """)

# --- TAB 3: SIMULASI TAMBAH DAYA ---
with tab3:
    st.subheader("📈 Kalkulator & Simulasi Tambah Daya")
    d_awal = st.selectbox("Daya Saat Ini (VA):", [450, 900, 1300, 2200])
    d_tujuan = st.selectbox("Daya Target (VA):", [1300, 2200, 3500, 4400, 5500])
    if d_tujuan > d_awal:
        st.success(f"Peningkatan kapasitas daya sebesar {d_tujuan - d_awal} VA akan membuat penggunaan alat elektronik lebih leluasa tanpa khawatir MCB anjlok.")
        st.info("💡 Buka aplikasi **PLN Mobile** untuk mengecek program diskon promo Tambah Daya terbaru!")

# --- TAB 4: KAMUS KODE METERAN ---
with tab4:
    st.subheader("📖 Kamus Short Code Meteran Prabayar")
    merek = st.radio("Pilih Merek Meteran Rumah Anda:", ["Itron", "Hexing", "Glomet / Sanxing"], horizontal=True)
    if merek == "Itron":
        st.table({"Kode": ["41", "44", "47", "09"], "Fungsi": ["Cek Voltase (V)", "Cek Arus (A)", "Cek Daya (W)", "Cek Daya Terakhir Anjlok"]})
    elif merek == "Hexing":
        st.table({"Kode": ["41#", "44#", "47#", "801#"], "Fungsi": ["Cek Voltase (V)", "Cek Arus (A)", "Cek Daya (W)", "Cek Sisa Token"]})
    else:
        st.table({"Kode": ["41", "44", "47"], "Fungsi": ["Cek Voltase (V)", "Cek Arus (A)", "Cek Daya (W)"]})
