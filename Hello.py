import streamlit as st
import pandas as pd
import plotly.express as px
import datetime
import numpy as np
from pyecharts.charts import Pie
from pyecharts import options as opts

# Judul aplikasi
st.title('Data Covid Pada Tahun 2020')

# Baca data dari file CSV
data = pd.read_csv("data_infeksi_covid19_indonesia.csv")

# Konversi kolom "tanggal" ke tipe data datetime jika belum
data['tanggal'] = pd.to_datetime(data['tanggal'])

fig_size = (800, 600)

# Menampilkan data awal
st.write("Tabel Data:")
st.write(data)

# Formulir tanggal awal
tanggal_awal = st.date_input("Pilih tanggal batas awal", datetime.date(2020, 2, 18))
tanggal_awal = datetime.datetime.combine(tanggal_awal, datetime.datetime.min.time())

# Formulir tanggal akhir
tanggal_akhir = st.date_input("Pilih tanggal batas akhir", datetime.date(2020, 6, 1))
tanggal_akhir = datetime.datetime.combine(tanggal_akhir, datetime.datetime.min.time())

# Membuat subset data berdasarkan tanggal yang dipilih
data_subset = data[(data["tanggal"] >= tanggal_awal) & (data["tanggal"] <= tanggal_akhir)]

# Pilihan kolom yang akan digunakan untuk membuat grafik
kolom_pilihan = st.selectbox("Pilih kolom untuk membuat grafik", ["konfirmasi", "sembuh", "meninggal", "negatif", "proses_periksa", "kasus_perawatan"])

# Membuat grafik berdasarkan kolom yang dipilih
fig = px.line(data_subset, x="tanggal", y=kolom_pilihan, title=f"Grafik {kolom_pilihan} antara {tanggal_awal.date()} dan {tanggal_akhir.date()}") 
st.plotly_chart(fig)

# Mengelompokkan data berdasarkan bulan dan menghitung total "kolom yang dipilih pada selectbox" per bulan
data_subset['bulan'] = data_subset['tanggal'].dt.strftime('%Y-%m')
total_setiap_kolom = data_subset.groupby('bulan')[kolom_pilihan].sum()

# Membuat chart batang dengan bulan-bulan yang diurutkan
total_setiap_kolom = total_setiap_kolom.reset_index()
total_setiap_kolom['bulan'] = pd.to_datetime(total_setiap_kolom['bulan'])
total_setiap_kolom = total_setiap_kolom.sort_values(by='bulan')

fig_setiap_kolom = px.bar(total_setiap_kolom, x='bulan', y=kolom_pilihan, labels={'y': f'Total {kolom_pilihan}'})
fig_setiap_kolom.update_xaxes(
    title_text='Bulan',
    tickvals=total_setiap_kolom['bulan'],
    ticktext=total_setiap_kolom['bulan'].dt.strftime('%b %Y')
)
fig_setiap_kolom.update_layout(title=f"Total {kolom_pilihan} per Bulan ({tanggal_awal.strftime('%B %Y')} - {tanggal_akhir.strftime('%B %Y')})")
st.plotly_chart(fig_setiap_kolom)

# Pie Chart
st.markdown('**Pie Chart**')
# Misalnya, di sini kita mengambil total dari setiap kolom yang Anda pilih
total_kolom = data_subset[["konfirmasi", "sembuh", "meninggal", "negatif"]].sum()
# Mengonversi total menjadi DataFrame
total_kolom_df = total_kolom.reset_index()
total_kolom_df.columns = ["Category", "Total"]
# Gunakan total ini untuk membuat chart Pie
fig_pie = px.pie(total_kolom_df, names="Category", values="Total")
fig_pie.update_layout(height=fig_size[1], width=fig_size[0])
st.plotly_chart(fig_pie)
