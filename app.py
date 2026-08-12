import streamlit as st

# Config Halaman
st.set_page_config(page_title="E-Diagnostik PLN UP3", page_icon="⚡", layout="centered")

# Header & Logo PLN (Tampil Paling Atas di Layar HP)
col_logo, col_text = st.columns([1, 3])
with col_logo:
    st.image("https://upload.wikimedia.org/wikipedia/commons/2/20/LOGO_PLN.png", width=80)
with col_text:
    st.markdown("<h2 style='color: #005A9C; margin:0;'>⚡ E-Diagnostik PLN</h2>", unsafe_allow_html=True)
    st.caption("Layanan Edukasi & Diagnostik Kelistrikan Mandiri - PLN UP3")

st.markdown("---")

# Petunjuk Awal untuk Orang Awam
st.write("👇 **Pilih menu layanan yang Anda butuhkan di bawah ini:**")

# TAB NAVIGASI UTAMA (Langsung Terlihat & Mudah Di-tap dari HP)
tab1, tab2, tab3, tab4 = st.tabs([
    "🔍 Cek Beban", 
    "🕵️ Kebocoran Arus", 
    "📈 Tambah Daya", 
    "📖 Kode Meteran"
])

# --- TAB 1: CEK BEBAN ---
with tab1:
    st.subheader("🔍 Cek Beban Listrik Real-Time")
    st.info("Fitur ini menghitung persentase beban aktual rumah Anda menggunakan data dari kode meteran prabayar.")
    
    daya_kontrak = st.select_slider("Pilih Daya Terpasang Rumah (VA):", options=[450, 900, 1300, 2200, 3500, 4400, 5500, 6600], value=900)
    
    col1, col2 = st.columns(2)
    with col1:
        v_input = st.number_input("Tegangan (Volt) [Kode 41#]:", value=220.0, step=1.0)
    with col2:
        i_input = st.number_input("Arus (Ampere) [Kode 44#]:", value=2.5, step=0.1)
        
    daya_terpakai = v_input * i_input
    persen_beban = (daya_terpakai / daya_kontrak) * 100
    
    st.markdown("### 📊 Hasil Analisis:")
    col_a, col_b = st.columns(2)
    col_a.metric("Daya Terpakai", f"{daya_terpakai:.1f} W")
    col_b.metric("Kapasitas Beban", f"{persen_beban:.1f} %")
    
    if persen_beban > 100:
        st.error("🚨 STATUS: OVERLOAD! Pemakaian melebihi batas MCB. Disarankan mengajukan Tambah Daya.")
    elif persen_beban > 80:
        st.warning("⚠️ STATUS: BEBAN TINGGI! Kurangi pemakaian alat berdaya besar secara bersamaan.")
    else:
        st.success("✅ STATUS: AMAN. Beban listrik dalam kapasitas normal.")

# --- TAB 2: KEBOCORAN ARUS ---
with tab2:
    st.subheader("🕵️‍♂️ Detektif Kebocoran Arus Tanah")
    st.write("Ikuti petunjuk untuk mengecek adanya kebocoran instalasi internal rumah Anda:")
    st.markdown("1. Matikan seluruh sakelar MCB di dalam rumah.\n2. Ketik **44#** atau **44 Enter** pada meteran.\n3. Masukkan angka arus yang tertera di bawah ini:")
    
    arus_bocor = st.number_input("Arus Terbaca (Ampere):", value=0.0, step=0.01)
    if st.button("Jalankan Analisis Kebocoran"):
        if arus_bocor > 0.05:
            st.error(f"🚨 Terdeteksi Kebocoran Arus sebesar {arus_bocor} A! Segera periksa kabel instalasi rumah Anda.")
        else:
            st.success("✅ Instalasi Aman. Tidak ada arus yang bocor ke tanah.")

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
