
# ==========================================================
# HALAMAN 2 - STATISTIKA NONPARAMETRIK
# ANALISIS PENDAPATAN BPHTB KOTA SURABAYA
# ==========================================================

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path


# ==========================================================
# 1. KONFIGURASI HALAMAN
# ==========================================================

st.set_page_config(
    page_title="Statistika Nonparametrik BPHTB",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==========================================================
# 2. WARNA DAN STYLING
# ==========================================================

NAVY = "#193B61"
BLUE = "#377FB8"
GOLD = "#D5A143"
GREEN = "#168678"
RED = "#D9534F"

WARNA_TAHUN = [
    "#193B61",
    "#377FB8",
    "#168678",
    "#D5A143",
    "#8872B5"
]

st.markdown("""
<style>
.block-container {
    max-width: 100%;
    padding-top: 1.5rem;
    padding-left: 1.8rem;
    padding-right: 1.8rem;
    padding-bottom: 2rem;
}

[data-testid="stSidebar"] {
    background-color: #F1F5F9;
}

[data-testid="stMetric"] {
    background-color: #F8FAFC;
    border: 1px solid #E2E8F0;
    border-radius: 12px;
    padding: 17px 12px;
    min-height: 110px;
}

[data-testid="stMetricValue"] * {
    font-size: 1.3rem !important;
    font-weight: 700 !important;
}

[data-testid="stMetricValue"] {
    overflow: visible !important;
}

h1, h2, h3 {
    color: #193B61;
}

[data-testid="stCaptionContainer"] {
    line-height: 1.6;
}
</style>
""", unsafe_allow_html=True)


# ==========================================================
# 3. FORMAT ANGKA
# ==========================================================

def format_angka(nilai, desimal=2):

    return (
        f"{float(nilai):,.{desimal}f}"
        .replace(",", "_")
        .replace(".", ",")
        .replace("_", ".")
    )


def format_pvalue(nilai):

    nilai = float(nilai)

    if nilai < 0.001:
        return f"{nilai:.6f}".replace(".", ",")

    return format_angka(nilai, 4)


NAMA_BULAN = {
    1: "Jan", 2: "Feb", 3: "Mar",
    4: "Apr", 5: "Mei", 6: "Jun",
    7: "Jul", 8: "Agu", 9: "Sep",
    10: "Okt", 11: "Nov", 12: "Des"
}

URUTAN_BULAN = list(NAMA_BULAN.values())


# ==========================================================
# 4. MEMBACA DATASET
# ==========================================================

BASE_DIR = Path(__file__).resolve().parents[1]

FOLDER_NONPARAM = (
    BASE_DIR / "02_Statistika_Nonparametrik"
)

FOLDER_MASTER = (
    BASE_DIR / "01_Data_Preparation"
)

FILE_DATA = {
    "master":
        FOLDER_MASTER /
        "BPHTB_Master_Bulanan_2021_2026.csv",

    "friedman":
        FOLDER_NONPARAM /
        "hasil_friedman.csv",

    "peringkat":
        FOLDER_NONPARAM /
        "peringkat_bulanan.csv",

    "spearman":
        FOLDER_NONPARAM /
        "korelasi_spearman_tahunan.csv",

    "sensitivitas":
        FOLDER_NONPARAM /
        "sensitivitas_spearman.csv"
}


@st.cache_data
def baca_csv(lokasi):
    return pd.read_csv(lokasi)


for nama, lokasi in FILE_DATA.items():

    if not lokasi.exists():
        st.error(
            f"File {nama} tidak ditemukan: {lokasi}"
        )
        st.stop()


try:

    master = baca_csv(FILE_DATA["master"])

    hasil_friedman = baca_csv(
        FILE_DATA["friedman"]
    )

    peringkat_bulanan = baca_csv(
        FILE_DATA["peringkat"]
    )

    spearman_tahunan = baca_csv(
        FILE_DATA["spearman"]
    )

    sensitivitas = baca_csv(
        FILE_DATA["sensitivitas"]
    )

except Exception as error:

    st.error(f"Gagal membaca dataset: {error}")
    st.stop()


# ==========================================================
# 5. PERSIAPAN MASTER DATA
# ==========================================================

data_historis = master[
    (master["tahun"].between(2021, 2025)) &
    (master["status_nilai"].astype(str).str.strip()
     == "Realisasi")
].copy()

data_historis = data_historis.sort_values(
    ["tahun", "bulan_ke"]
)

data_historis["bulan"] = (
    data_historis["bulan_ke"].map(NAMA_BULAN)
)

data_historis["realisasi_miliar"] = (
    data_historis["realisasi_rp"] / 1e9
)

assert len(data_historis) == 60, (
    "Data historis harus terdiri dari 60 bulan."
)

assert data_historis["realisasi_rp"].notna().all()

assert data_historis["jumlah_sspd"].notna().all()


# ==========================================================
# 6. SIDEBAR DAN NAVIGASI
# ==========================================================

st.sidebar.title("Analisis BPHTB")
st.sidebar.caption("Bapenda Kota Surabaya")

st.sidebar.divider()

st.sidebar.subheader("Navigasi")

# Ikon rumah outline biru navy
home_html = (
    '<a href="/" target="_self" '
    'style="display:flex;align-items:center;gap:12px;'
    'padding:11px 14px;text-decoration:none;'
    'color:#193B61;font-weight:600;font-size:15px;">'
    '<svg xmlns="http://www.w3.org/2000/svg" '
    'width="23" height="23" viewBox="0 0 24 24" '
    'fill="none" stroke="#193B61" '
    'stroke-width="2.2" stroke-linecap="round" '
    'stroke-linejoin="round">'
    '<path d="M3 10.5 12 3l9 7.5v9'
    'a1 1 0 0 1-1 1h-5v-7H9v7H4'
    'a1 1 0 0 1-1-1z"/>'
    '</svg>'
    '<span>Beranda</span>'
    '</a>'
)

st.sidebar.markdown(
    home_html,
    unsafe_allow_html=True
)

st.sidebar.page_link(
    "pages/2_Statistika_Nonparametrik.py",
    label="Statistika Nonparametrik",
    icon=":material/query_stats:"
)

st.sidebar.divider()

# Filter hanya untuk grafik eksploratif
st.sidebar.subheader("Filter Data")

pilihan_tahun = [
    "2021–2025", 2021, 2022, 2023, 2024, 2025
]

tahun_pilih = st.sidebar.selectbox(
    "Pilih Tahun",
    pilihan_tahun
)

if tahun_pilih == "2021–2025":

    data_tampil = data_historis.copy()
    daftar_tahun = [2021, 2022, 2023, 2024, 2025]

else:

    data_tampil = data_historis[
        data_historis["tahun"] == tahun_pilih
    ].copy()

    daftar_tahun = [tahun_pilih]


# ==========================================================
# 7. HEADER
# ==========================================================

st.title("Statistika Nonparametrik")

st.markdown(
    "**Analisis Penerimaan BPHTB Kota Surabaya**"
)

st.caption("Periode analisis statistik 2021–2025")

st.divider()


# ==========================================================
# 8. MENGAMBIL NILAI HASIL UJI
# ==========================================================

friedman = hasil_friedman.iloc[0]

stat_friedman = float(
    friedman["statistik_uji"]
)

p_permutasi = float(
    friedman["p_value_permutasi"]
)

kendall_w = float(
    friedman["kendalls_w"]
)

data_keseluruhan = sensitivitas[
    sensitivitas["metode"] == "Seluruh data"
].iloc[0]

rho_keseluruhan = float(
    data_keseluruhan["spearman_rho"]
)


# ==========================================================
# 9. KPI STATISTIK
# ==========================================================

st.subheader("Ringkasan Hasil Pengujian")

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.metric(
        "Statistik Friedman",
        format_angka(stat_friedman, 2)
    )

with k2:
    st.metric(
        "P-value Permutasi",
        format_pvalue(p_permutasi)
    )

with k3:
    st.metric(
        "Kendall's W",
        format_angka(kendall_w, 4)
    )

with k4:
    st.metric(
        "Spearman Keseluruhan",
        format_angka(rho_keseluruhan, 4)
    )

if p_permutasi < 0.05:

    st.caption(
        "Uji Friedman menunjukkan perbedaan "
        "peringkat penerimaan yang signifikan "
        "antarbulan pada periode 2021–2025."
    )

else:

    st.caption(
        "Uji Friedman belum menunjukkan "
        "bukti perbedaan peringkat penerimaan "
        "yang signifikan antarbulan."
    )

st.divider()


# ==========================================================
# 10. FUNGSI STYLING GRAFIK
# ==========================================================

def style_grafik(fig, judul_y, tinggi=340):

    fig.update_layout(
        height=tinggi,
        margin=dict(
            l=10,
            r=10,
            t=55,
            b=10
        ),
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(
            family="Arial",
            size=12
        ),
        xaxis_title=None,
        yaxis_title=judul_y,
        hovermode="closest",
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.03,
            xanchor="left",
            x=0
        )
    )

    fig.update_xaxes(
        showgrid=False
    )

    fig.update_yaxes(
        showgrid=True,
        gridcolor="#E9EEF5"
    )

    return fig


# ==========================================================
# 11. GRAFIK PERINGKAT DAN POLA BULANAN
# ==========================================================

col1, col2 = st.columns(2, gap="medium")


# ----------------------------------------------------------
# GRAFIK 1 - RATA-RATA PERINGKAT FRIEDMAN
# ----------------------------------------------------------

with col1:

    with st.container(border=True):

        st.markdown(
            "#### Peringkat Penerimaan Berdasarkan Bulan"
        )

        data_rank = peringkat_bulanan.sort_values(
            "bulan_ke"
        )

        fig1 = go.Figure()

        fig1.add_trace(
            go.Bar(
                x=data_rank["bulan"],
                y=data_rank["rata_rata_rank"],
                name="Rata-rata Peringkat",
                marker_color=BLUE
            )
        )

        fig1.update_layout(
            yaxis_range=[0, 12]
        )

        st.plotly_chart(
            style_grafik(
                fig1,
                "Rata-rata Peringkat"
            ),
            use_container_width=True
        )

        tertinggi = data_rank.loc[
            data_rank["rata_rata_rank"].idxmax()
        ]

        terendah = data_rank.loc[
            data_rank["rata_rata_rank"].idxmin()
        ]

        st.caption(
            f"{tertinggi['bulan']} memiliki rata-rata "
            f"peringkat penerimaan tertinggi "
            f"({format_angka(tertinggi['rata_rata_rank'], 1)}), "
            f"sedangkan {terendah['bulan']} "
            f"terendah "
            f"({format_angka(terendah['rata_rata_rank'], 1)}). "
            f"Peringkat dihitung dari seluruh tahun 2021–2025."
        )


# ----------------------------------------------------------
# GRAFIK 2 - POLA PENERIMAAN BULANAN
# ----------------------------------------------------------

with col2:

    with st.container(border=True):

        st.markdown(
            "#### Pola Penerimaan BPHTB Bulanan"
        )

        fig2 = go.Figure()

        for i, tahun in enumerate(daftar_tahun):

            data_per_tahun = data_tampil[
                data_tampil["tahun"] == tahun
            ].sort_values("bulan_ke")

            fig2.add_trace(
                go.Scatter(
                    x=data_per_tahun["bulan"],
                    y=data_per_tahun["realisasi_miliar"],
                    mode="lines+markers",
                    name=str(tahun),
                    line=dict(
                        color=WARNA_TAHUN[
                            (tahun - 2021) % len(WARNA_TAHUN)
                        ],
                        width=2.5
                    )
                )
            )

        fig2.update_layout(
            xaxis=dict(
                categoryorder="array",
                categoryarray=URUTAN_BULAN
            ),
            hovermode="x unified"
        )

        st.plotly_chart(
            style_grafik(
                fig2,
                "Realisasi (Miliar Rupiah)"
            ),
            use_container_width=True
        )

        rata_bulanan = (
            data_tampil.groupby("bulan_ke")[
                "realisasi_miliar"
            ].mean()
        )

        bulan_tinggi = int(
            rata_bulanan.idxmax()
        )

        bulan_rendah = int(
            rata_bulanan.idxmin()
        )

        st.caption(
            f"Pada data yang ditampilkan, "
            f"{NAMA_BULAN[bulan_tinggi]} memiliki "
            f"rata-rata penerimaan tertinggi "
            f"({format_angka(rata_bulanan.max())} miliar), "
            f"sedangkan {NAMA_BULAN[bulan_rendah]} "
            f"terendah "
            f"({format_angka(rata_bulanan.min())} miliar)."
        )


# ==========================================================
# 12. GRAFIK KORELASI SPEARMAN
# ==========================================================

col3, col4 = st.columns(2, gap="medium")


# ----------------------------------------------------------
# GRAFIK 3 - HUBUNGAN SSPD DAN REALISASI
# ----------------------------------------------------------

with col3:

    with st.container(border=True):

        st.markdown(
            "#### Hubungan Jumlah SSPD dan Realisasi"
        )

        fig3 = go.Figure()

        for tahun in daftar_tahun:

            kelompok = data_tampil[
                data_tampil["tahun"] == tahun
            ]

            fig3.add_trace(
                go.Scatter(
                    x=kelompok["jumlah_sspd"],
                    y=kelompok["realisasi_miliar"],
                    mode="markers",
                    name=str(tahun),
                    marker=dict(
                        size=9,
                        color=WARNA_TAHUN[
                            (tahun - 2021) % len(WARNA_TAHUN)
                        ],
                        opacity=0.8
                    ),
                    hovertemplate=(
                        "SSPD: %{x:,.0f}"
                        "<br>Realisasi: %{y:,.2f} M"
                        "<extra>%{fullData.name}</extra>"
                    )
                )
            )

        fig3.update_layout(
            xaxis_title="Jumlah SSPD"
        )

        st.plotly_chart(
            style_grafik(
                fig3,
                "Realisasi (Miliar Rupiah)"
            ),
            use_container_width=True
        )

        if tahun_pilih == "2021–2025":

            rho = rho_keseluruhan

            st.caption(
                f"Korelasi Spearman keseluruhan "
                f"sebesar {format_angka(rho, 4)} "
                f"menunjukkan hubungan positif kuat "
                f"antara jumlah SSPD dan realisasi BPHTB. "
                f"Hubungan ini tidak membuktikan sebab-akibat."
            )

        else:

            baris_rho = spearman_tahunan[
                spearman_tahunan["tahun"] == tahun_pilih
            ].iloc[0]

            rho = float(
                baris_rho["spearman_rho"]
            )

            st.caption(
                f"Pada {tahun_pilih}, korelasi Spearman "
                f"sebesar {format_angka(rho, 4)} "
                f"menunjukkan hubungan positif antara "
                f"jumlah SSPD dan realisasi BPHTB."
            )


# ----------------------------------------------------------
# GRAFIK 4 - KORELASI SPEARMAN PER TAHUN
# ----------------------------------------------------------

with col4:

    with st.container(border=True):

        st.markdown(
            "#### Korelasi Spearman per Tahun"
        )

        data_rho = spearman_tahunan.sort_values(
            "tahun"
        )

        fig4 = go.Figure()

        fig4.add_trace(
            go.Bar(
                x=data_rho["tahun"].astype(str),
                y=data_rho["spearman_rho"],
                name="Koefisien Spearman",
                marker_color=GREEN
            )
        )

        fig4.update_layout(
            yaxis_range=[0, 1.05]
        )

        st.plotly_chart(
            style_grafik(
                fig4,
                "Koefisien Spearman"
            ),
            use_container_width=True
        )

        rho_min = data_rho[
            "spearman_rho"
        ].min()

        rho_max = data_rho[
            "spearman_rho"
        ].max()

        st.caption(
            f"Selama 2021–2025, seluruh tahun "
            f"menunjukkan korelasi positif, "
            f"dengan koefisien berkisar antara "
            f"{format_angka(rho_min, 4)} hingga "
            f"{format_angka(rho_max, 4)}."
        )


# ==========================================================
# 13. ANALISIS SENSITIVITAS
# ==========================================================

st.divider()

st.subheader("Pemeriksaan Sensitivitas Korelasi")

with st.container(border=True):

    fig5 = go.Figure()

    fig5.add_trace(
        go.Bar(
            y=sensitivitas["metode"],
            x=sensitivitas["spearman_rho"],
            orientation="h",
            name="Koefisien Spearman",
            marker_color=BLUE
        )
    )

    fig5.update_layout(
        xaxis=dict(
            title="Koefisien Spearman",
            range=[0, 1]
        ),
        yaxis=dict(autorange="reversed"),
        hovermode="closest"
    )

    st.plotly_chart(
        style_grafik(fig5, None, tinggi=290),
        use_container_width=True
    )

    nilai_min = sensitivitas[
        "spearman_rho"
    ].min()

    nilai_max = sensitivitas[
        "spearman_rho"
    ].max()

    st.caption(
        f"Korelasi tetap positif pada seluruh "
        f"pemeriksaan sensitivitas "
        f"({format_angka(nilai_min, 4)}–"
        f"{format_angka(nilai_max, 4)}). "
        f"Hasil ini mendukung konsistensi arah "
        f"hubungan, meskipun ketergantungan "
        f"antarbulan masih perlu diperhatikan."
    )


# ==========================================================
# 14. RINGKASAN HASIL STATISTIK
# ==========================================================

st.divider()

st.subheader("Kesimpulan Statistik")

st.markdown(
    "Uji Friedman menunjukkan adanya perbedaan "
    "peringkat penerimaan BPHTB antarbulan selama "
    "2021–2025. Sementara itu, korelasi Spearman "
    "menunjukkan bahwa jumlah SSPD dan realisasi "
    "BPHTB cenderung bergerak searah."
)

st.caption(
    "Hasil pengujian bersifat historis dan tidak "
    "secara langsung menjelaskan penyebab perubahan "
    "penerimaan maupun menjamin pola pada tahun berikutnya."
)
