import streamlit as st
import pandas as pd

# Baca data dari file CSV
data = pd.read_csv("data_infeksi_covid19_indonesia.csv")  # Ganti "nama_file.csv" dengan nama file CSV Anda

# Tampilkan data di aplikasi Streamlit
st.title("Data infeksi Covid 19 Pada Tahun 20200")
st.write("Berikut adalah data dari file :")
st.write(data)
