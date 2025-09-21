# streamlit_app_excel.py
import streamlit as st
import pandas as pd

# ----- Load data dari Excel -----
DATA_PATH = "/root/prediksi_kesehatan/prediksiml.xlsx"

try:
    df = pd.read_excel(DATA_PATH)
except Exception as e:
    st.error(f"Gagal membaca data Excel: {e}")
    st.stop()

st.title("Prediksi dan Deteksi Kesehatan Janin")
st.markdown("""
Masukkan **data awal** dan **data akhir** pasien. 
Aplikasi akan mendeteksi pertumbuhan abnormal/anomali dan menampilkan rekomendasi serta artikel terkait.
""")

# ----- Input Data Awal -----
st.subheader("Data Awal Pasien")
col1, col2 = st.columns(2)

with col1:
    start_week = st.number_input("Minggu Awal", min_value=1, max_value=40, value=1)
    start_weight = st.number_input("Berat Janin Awal (gram)", min_value=0, value=32)
    
with col2:
    start_height = st.number_input("Panjang Janin Awal (cm)", min_value=0, value=12)
    start_hr = st.number_input("Denyut Jantung Janin Awal", min_value=0, value=105)

# ----- Input Data Akhir -----
st.subheader("Data Akhir Pasien")
col3, col4 = st.columns(2)

with col3:
    end_week = st.number_input("Minggu Akhir", min_value=1, max_value=40, value=3)
    end_weight = st.number_input("Berat Janin Akhir (gram)", min_value=0, value=37)
    
with col4:
    end_height = st.number_input("Panjang Janin Akhir (cm)", min_value=0, value=15)
    end_hr = st.number_input("Denyut Jantung Janin Akhir", min_value=0, value=112)

# ----- Deteksi Anomali -----
if st.button("Cek Perkembangan"):
    if end_week < start_week:
        st.warning("Minggu akhir harus lebih besar atau sama dengan minggu awal!")
    else:
        # Ambil row data dari minggu akhir
        end_row = df[df['week'] == end_week].iloc[0]

        anomalies = []

        # Cek berat janin
        if not (end_row['weight_min'] <= end_weight <= end_row['weight_max']):
            anomalies.append(f"Berat janin ({end_weight} g) di luar range normal [{end_row['weight_min']}-{end_row['weight_max']}] g")

        # Cek panjang janin
        if not (end_row['height_min'] <= end_height <= end_row['height_max']):
            anomalies.append(f"Panjang janin ({end_height} cm) di luar range normal [{end_row['height_min']}-{end_row['height_max']}] cm")

        # Cek denyut jantung
        if not (end_row['heart_rate_min'] <= end_hr <= end_row['heart_rate_max']):
            anomalies.append(f"Denyut jantung ({end_hr}) di luar range normal [{end_row['heart_rate_min']}-{end_row['heart_rate_max']}]")

        # Hasil
        st.subheader("Hasil Deteksi")
        if anomalies:
            st.error("⚠️ Terdeteksi anomali:")
            for a in anomalies:
                st.write("- " + a)
            st.info(f"Rekomendasi: {end_row['recommendation']}")
            st.info(f"Artikel terkait: {end_row['articles']}")
        else:
            st.success("✅ Perkembangan janin normal sesuai data referensi.")
            st.info(f"Rekomendasi: {end_row['recommendation']}")
            st.info(f"Artikel terkait: {end_row['articles']}")
