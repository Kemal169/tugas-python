import streamlit as st
import pandas as pd

# Baca data dari file CSV
data = pd.read_csv("nama_file.csv")  # Ganti "nama_file.csv" dengan nama file CSV Anda

# Tampilkan data di aplikasi Streamlit
st.title("Aplikasi Streamlit untuk Data CSV")
st.write("Berikut adalah data dari file CSV:")
st.write(data)
