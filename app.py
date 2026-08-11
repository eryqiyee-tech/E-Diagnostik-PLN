import streamlit as st

st.set_page_config(page_title="E-Diagnostik PLN UP3", page_icon="⚡")

st.title("⚡ E-Diagnostik kWh Meter PLN")
st.caption("Aplikasi Edukasi & Diagnostik Kelistrikan Mandiri - PLN UP3")
st.markdown("---")

menu = st.sidebar.radio(
    "Pilih Fitur Diagnostik:",
    ["1. Cek Beban & Status MCB", "2. Deteksi Kebocoran Arus", "3. Kamus Kode Meteran"]
)

if menu == "1. Cek Beban & Status MCB":
    st.header("🔍 Cek Beban Listrik Real-Time")
    daya_kontrak = st.selectbox("Pilih Daya Terpasang (VA):", [450, 900, 1300, 2200, 3500])
    
    col1, col2 = st.columns(2)
    with col1:
        v_input = st.number_input("Tegangan / Voltase (Volt) [Kode 41#]:", value=220.0)
    with col2:
        i_input = st.number_input("Arus Listrik (Ampere) [Kode 44#]:", value=2.5)

    daya_terpakai = v_input * i_input
    persen_beban = (daya_terpakai / daya_kontrak) * 100

    st.markdown("---")
    st.metric(label="Daya Terpakai (Watt)", value=f"{daya_terpakai:.1f} W")
    st.metric(label="Persentase Beban", value=f"{persen_beban:.1f} %")

    if persen_beban > 100:
        st.error("🚨 STATUS: OVERLOAD! Pemakaian melebihi kapasitas MCB.")
    else:
        st.success("✅ STATUS: AMAN. Beban listrik dalam batas normal.")

elif menu == "2. Deteksi Kebocoran Arus":
    st.header("🕵️‍♂️ Deteksi Kebocoran Arus")
    st.write("Matikan semua sakelar MCB di dalam rumah, lalu masukkan angka arus dari kode 44#:")
    arus_bocor = st.number_input("Arus Terbaca (Ampere):", value=0.0)

    if st.button("Analisa Kondisi"):
        if arus_bocor > 0.05:
            st.error(f"🚨 Terdeteksi kebocoran arus sebesar {arus_bocor} A!")
        else:
            st.success("✅ Instalasi Aman dari kebocoran arus tanah.")

elif menu == "3. Kamus Kode Meteran":
    st.header("📖 Kamus Kode Meteran")
    st.table({
        "Kode": ["41#", "44#", "47#"],
        "Fungsi": ["Cek Voltase (V)", "Cek Arus (A)", "Cek Daya (W)"]
    })