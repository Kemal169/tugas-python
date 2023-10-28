import streamlit as st
import pandas as pd
import plotly.express as px
import datetime
import numpy as np

# Menambahkan gambar dengan Streamlit di sidebar
st.sidebar.image("images.png", width=250)

# Menggunakan CSS untuk menggeser gambar ke atas
st.markdown(
    """
    <style>
        .sidebar .sidebar-content {
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        .sidebar .sidebar-content .block-container {
            margin-top: -1220;
        }
    </style>
    """,
    unsafe_allow_html=True
)
# Tambahkan item-menu
st.sidebar.header("Menu Diagram")

# Tambahkan item-menu
selected_page = st.sidebar.radio(
    "Pilih Halaman",
    ("Data", "Grafik", "Charts Batang","Charts Pie")
)

# Tampilkan konten sesuai dengan halaman yang dipilih
if selected_page == "Data":
    st.title("Data Covid Pada Tahun 2020")
    
    data = pd.read_csv("data_infeksi_covid19_indonesia.csv")
    data['tanggal'] = pd.to_datetime(data['tanggal'])

    fig_size = (800, 600)
    
    st.write("Tabel Data:")
    st.write(data)

elif selected_page == "Grafik":
    st.title("Diagram Grafik")

    data = pd.read_csv("data_infeksi_covid19_indonesia.csv")
    data['tanggal'] = pd.to_datetime(data['tanggal'])

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
    
    st.write("Ini adalah Halam Diagram Grafik.")

elif selected_page == "Charts Batang":
    st.title("Halaman Charts Batang")

    data = pd.read_csv("data_infeksi_covid19_indonesia.csv")
    data['tanggal'] = pd.to_datetime(data['tanggal'])

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

    st.write("Ini adalah halaman Charts Batang.")

elif selected_page == "Charts Pie":
    st.title("Halaman Charts Pie")

    data = pd.read_csv("data_infeksi_covid19_indonesia.csv")
    data['tanggal'] = pd.to_datetime(data['tanggal'])

    fig_size = (800, 600)

    # Formulir tanggal awal
    tanggal_awal = st.date_input("Pilih tanggal batas awal", datetime.date(2020, 2, 18))
    tanggal_awal = datetime.datetime.combine(tanggal_awal, datetime.datetime.min.time())

    # Formulir tanggal akhir
    tanggal_akhir = st.date_input("Pilih tanggal batas akhir", datetime.date(2020, 6, 1))
    tanggal_akhir = datetime.datetime.combine(tanggal_akhir, datetime.datetime.min.time())

    # Membuat subset data berdasarkan tanggal yang dipilih
    data_subset = data[(data["tanggal"] >= tanggal_awal) & (data["tanggal"] <= tanggal_akhir)]

    # Pilihan kolom yang akan digunakan untuk membuat grafik
    kolom_pilihan = st.selectbox("Pilih kolom untuk membuat grafik", ["konfirmasi", "sembuh", "meninggal", "negatif"])

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

    st.markdown('**Pie Chart**')

    # Misalnya, di sini kita mengambil total dari setiap kolom yang Anda pilih
    total_kolom = data_subset[["konfirmasi", "sembuh", "meninggal", "negatif"]].sum()

    # Mengonversi total menjadi DataFrame
    total_kolom_df = total_kolom.reset_index()
    total_kolom_df.columns = ["Category", "Total"]

    # Definisikan urutan warna yang Anda inginkan
    color_sequence = ["#FF5733", "#33FF57", "#3366FF", "#FFFF33"]

    # Gunakan total ini untuk membuat chart Pie
    fig_pie = px.pie(total_kolom_df, names="Category", values="Total")
    fig_pie.update_layout(height=fig_size[1], width=fig_size[0])

    # Atur urutan warna pada chart pie
    fig_pie.update_traces(marker=dict(colors=color_sequence))

    st.plotly_chart(fig_pie)

    st.markdown('**Doughnut Chart**')

    fig = px.pie(
    total_kolom_df,
    names="Category",
    values="Total",
    hole=0.5,  # Mengatur ukuran "doughnut hole"
    title="Doughnut Chart - Data COVID-19",
    color_discrete_sequence=color_sequence
    )
    st.plotly_chart(fig)
