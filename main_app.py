import streamlit as st
from datetime import date
from manajer_laporan import ManajerLaporan
from model import Laporan
from konfigurasi import TIPE_LAPORAN
import folium
from streamlit_folium import st_folium
import pandas as pd

st.set_page_config(page_title="Pelaporan Jalan Rusak & Infrastruktur Kota Semarang", layout="wide")

# Handle session-based rerun
if st.session_state.get("rerun_trigger"):
    st.session_state["rerun_trigger"] = False
    st.experimental_rerun()

# Header 
col_logo, col_title = st.columns([1, 5])
with col_logo:
    st.image("assets/logo.png", width=80)

with col_title:
    st.markdown("""
    # Sistem Pelaporan Jalan Rusak & Infrastruktur Kota Semarang
    """)

manajer = ManajerLaporan()
df = manajer.semua_laporan_df()
if not df.empty and 'tanggal' in df.columns:
    df['tanggal'] = pd.to_datetime(df['tanggal'])

# Menu utama
menu = st.sidebar.radio("📂 Menu", ["➕ Tambah", "📂 Riwayat", "📈 Ringkasan", "🗺️ Peta"])

# MENU: TAMBAH
if menu == "➕ Tambah":
    st.header("📝 Tambah Laporan Jalan Rusak & Infrastruktur Kota Semarang")

    with st.form("form_laporan"):
        nama = st.text_input("Nama Lokasi")
        deskripsi = st.text_area("Deskripsi Kerusakan")
        tipe = st.selectbox("Jenis Infrastruktur", TIPE_LAPORAN)
        lat = st.number_input("Latitude", format="%.6f")
        lon = st.number_input("Longitude", format="%.6f")
        tanggal = st.date_input("Tanggal", value=date.today())
        submitted = st.form_submit_button("Simpan")

        if submitted:
            laporan = Laporan(nama, deskripsi, tipe, lat, lon, tanggal)
            manajer.tambah_laporan(laporan)
            st.session_state["rerun_trigger"] = True
            st.success("✅ Laporan berhasil disimpan.")

# MENU: RIWAYAT
elif menu == "📂 Riwayat":
    st.header("📄 Riwayat Laporan Masuk")
    if df.empty:
        st.info("Belum ada laporan yang masuk.")
    else:
        df_display = df[['id', 'nama', 'deskripsi', 'tipe', 'latitude', 'longitude', 'tanggal']].copy()
        df_display['tanggal'] = df_display['tanggal'].dt.date
        df_display = df_display.reset_index(drop=True)
        st.dataframe(df_display, use_container_width=True)

        st.subheader("🗑️ Hapus Laporan")
        daftar_id = df['id'].tolist()
        id_dihapus = st.selectbox("Pilih ID laporan yang akan dihapus:", daftar_id)
        if st.button("Hapus Data"):
            if manajer.hapus_laporan(id_dihapus):
                st.session_state["rerun_trigger"] = True
                st.success(f"Laporan dengan ID {id_dihapus} berhasil dihapus.")
            else:
                st.error("Gagal menghapus laporan. Coba lagi.")

# MENU: RINGKASAN
elif menu == "📈 Ringkasan":
    st.header("📈 Ringkasan Laporan Infrastruktur")

    if df.empty:
        st.info("Belum ada data laporan yang tersedia.")
    else:
        today = pd.to_datetime(date.today())

        col_filter, col_metric = st.columns([2, 1])
        with col_filter:
            st.subheader("📆 Filter Periode Waktu")
            periode_opsi = ["Semua Waktu", "Hari Ini", "Pilih Tanggal"]
            pilihan_periode = st.selectbox("Pilih Periode:", periode_opsi, index=0, key="periode", label_visibility="visible")

        if pilihan_periode == "Hari Ini":
            df_filtered = df[df['tanggal'].dt.date == today.date()]
        elif pilihan_periode == "Pilih Tanggal":
            tanggal_pilihan = st.date_input("Pilih Tanggal:", value=df['tanggal'].min().date())
            df_filtered = df[df['tanggal'].dt.date == tanggal_pilihan]
        else:
            df_filtered = df

        with col_metric:
            st.subheader("📊 Total Laporan")
            st.metric("", f"{len(df_filtered)} laporan")

        st.markdown("---")
        st.subheader(f"📊 Laporan per Kategori ({pilihan_periode})")

        if df_filtered.empty:
            st.info("Tidak ada data untuk periode ini.")
        else:
            col3, col4 = st.columns([1, 2])

            with col3:
                st.dataframe(
                    df_filtered[['tipe']]
                    .value_counts()
                    .reset_index()
                    .rename(columns={0: 'Jumlah', 'tipe': 'Tipe'}),
                    use_container_width=True
                )

            with col4:
                st.bar_chart(df_filtered['tipe'].value_counts())

# MENU: PETA
elif menu == "🗺️ Peta":
    st.header("🗺️ Peta Laporan Jalan Rusak & Infrastruktur Kota Semarang")

    if df.empty:
        st.info("Belum ada data untuk ditampilkan.")
    else:
        peta = folium.Map(location=[-6.9900, 110.4200], zoom_start=12)
        for _, row in df.iterrows():
            folium.Marker(
                location=[row['latitude'], row['longitude']],
                popup=f"<b>{row['nama']}</b><br>{row['tipe']}<br>{row['deskripsi']}",
                tooltip=row['tipe']
            ).add_to(peta)

        st_folium(peta, width=700, height=500)