# =============================================================
# DASHBOARD ANALISIS BPHTB KOTA SURABAYA
# =============================================================

from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
from html import escape
import json

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
import streamlit as st
import streamlit.components.v1 as components

from PIL import Image, ImageDraw
from scipy.stats import friedmanchisquare, spearmanr


# =============================================================
# 1. KONFIGURASI APLIKASI
# =============================================================

st.set_page_config(
    page_title="Dashboard Analisis BPHTB",
    page_icon=":material/account_balance:",
    layout="wide",
    initial_sidebar_state="expanded",
)

NAVY = "#193B61"
DARK = "#102B4A"
BLUE = "#3479B7"
GOLD = "#D5A143"
GREEN = "#168678"
RED = "#C7474F"

BULAN = dict(
    enumerate(
        "Jan Feb Mar Apr Mei Jun Jul Agu Sep Okt Nov Des".split(),
        1
    )
)


# =============================================================
# 2. CSS DASHBOARD
# =============================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

html, body,
[data-testid="stAppViewContainer"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
}

[data-testid="stAppViewContainer"],
.stApp {
    background: #F6F8FB;
}


/* Jarak konten dari header Streamlit */
.block-container {
    max-width: 1480px;
    padding: 5rem 1.6rem 2.7rem !important;
}

/* Memastikan banner tampil utuh */
.hero {
    margin-top: 0 !important;
}


h1, h2, h3, h4, h5 {
    color: #193B61;
    letter-spacing: -.025em;
}

/* ============================================================
   SIDEBAR
   ============================================================ */

[data-testid="stSidebar"] {
    background: linear-gradient(
        175deg,
        #193B61,
        #0A203B
    );
    border-right: 1px solid #365574;
}

[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p,
[data-testid="stSidebar"] .stCaptionContainer p {
    color: #F0F5FC !important;
}

[data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
    gap: .43rem !important;
}

[data-testid="stSidebar"] hr {
    border-color: rgba(255,255,255,.15) !important;
    margin: .5rem 0 !important;
}

/* Navigasi sidebar sejajar */

[data-testid="stSidebar"] .stButton button {
    width: 100% !important;
    min-height: 42px !important;

    border-radius: 11px !important;
    padding: 9px 13px !important;

    display: flex !important;
    align-items: center !important;
    justify-content: flex-start !important;

    gap: 11px !important;
    text-align: left !important;
    font-weight: 700;
}

[data-testid="stSidebar"] .stButton button > div {
    display: flex !important;
    align-items: center !important;
    justify-content: flex-start !important;

    gap: 11px !important;
    width: 100% !important;
}

[data-testid="stSidebar"] .stButton button span[data-testid="stIconMaterial"],
[data-testid="stSidebar"] .stButton button span[data-testid="stIcon"] {
    min-width: 23px !important;
    width: 23px !important;

    display: inline-flex !important;
    justify-content: center !important;
}

[data-testid="stSidebar"] .stButton button p {
    margin: 0 !important;
    text-align: left !important;
}

[data-testid="stSidebar"] .stButton button[kind="secondary"] {
    background: transparent !important;
    border: 1px solid transparent !important;
    color: #EFF5FC !important;
}

[data-testid="stSidebar"] .stButton button[kind="secondary"]:hover {
    background: rgba(255,255,255,.11) !important;
}

[data-testid="stSidebar"] .stButton button[kind="primary"] {
    background: #E7B751 !important;
    border: 1px solid #EDC568 !important;
    color: #193B61 !important;

    box-shadow: 0 3px 10px rgba(0,0,0,.12);
}

[data-testid="stSidebar"] .stButton button[kind="primary"] * {
    color: #193B61 !important;
}

[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background: white !important;
    border-radius: 10px !important;
}

[data-testid="stSidebar"] [data-baseweb="select"] * {
    color: #193B61 !important;
}

/* Tombol close sidebar bawaan Streamlit */

[data-testid="stSidebarHeader"] {
    min-height: 37px !important;
    padding: 3px 9px !important;
}

[data-testid="stSidebarCollapseButton"],
[data-testid="stSidebarCollapsedControl"] {
    visibility: visible !important;
    opacity: 1 !important;
}

[data-testid="stSidebarCollapseButton"] button {
    color: white !important;
    background: rgba(255,255,255,.10) !important;
    border-radius: 9px !important;
}

[data-testid="stSidebarCollapseButton"] svg {
    color: white !important;
}

/* Identitas aplikasi */

.sidebar-brand-name {
    font-size: 1.03rem;
    color: #FFFFFF;
    font-weight: 800;
    line-height: 1.3;
}

.sidebar-brand-sub {
    color: #F3C86C;
    font-weight: 750;
    font-size: .70rem;
    letter-spacing: .07em;
    margin-top: 3px;
}

.sidebar-brand-agency {
    color: #D5E5F4;
    font-size: .73rem;
    line-height: 1.4;
    margin-top: 4px;
}

.sidebar-year {
    display: inline-block;
    margin-top: 4px;

    border: 1px solid rgba(255,255,255,.26);
    background: rgba(255,255,255,.09);

    color: #FFF2D3;
    border-radius: 999px;

    padding: 6px 12px;
    font-weight: 750;
    font-size: .80rem;
}

/* Teks informasi sidebar */

.sidebar-note {
    padding: 12px 13px;

    border: 1px solid rgba(255,255,255,.16);
    border-radius: 11px;

    background: rgba(255,255,255,.09);
    color: #E9F2FC !important;

    line-height: 1.65;
    font-size: .78rem;
    margin-top: 10px;
}

/* ============================================================
   HERO HEADER
   ============================================================ */

.hero {
    background: linear-gradient(
        115deg,
        #102D4D,
        #193B61 56%,
        #316A91
    );

    border-radius: 18px;
    padding: 24px 27px;
    margin-bottom: 16px;

    box-shadow: 0 9px 23px rgba(22,49,78,.14);

    position: relative;
    overflow: hidden;
}

.hero:after {
    content: '';

    position: absolute;
    right: -57px;
    top: -100px;

    width: 255px;
    height: 255px;

    border: 1px solid rgba(255,255,255,.17);
    border-radius: 50%;

    box-shadow: 0 0 0 36px rgba(255,255,255,.035);
}

.hero-eyebrow {
    color: #F1C46B;

    font-weight: 800;
    letter-spacing: .11em;
    font-size: .70rem;
}

.hero h1 {
    color: white !important;
    font-size: clamp(1.55rem,2.4vw,2.15rem);

    margin: 7px 0 8px;
    line-height: 1.25;

    position: relative;
    z-index: 1;
}

.hero-desc {
    color: #DBE8F5;
    font-size: .88rem;

    position: relative;
    z-index: 1;
}

.hero-period {
    display: inline-block;
    margin-top: 12px;

    color: #FFE4A2;
    border: 1px solid rgba(255,220,140,.5);

    border-radius: 999px;
    padding: 5px 12px;

    background: rgba(219,173,83,.14);

    font-weight: 750;
    font-size: .77rem;

    position: relative;
    z-index: 1;
}

/* ============================================================
   KPI COMPACT
   ============================================================ */

.kpi {
    height: 124px;
    min-height: 124px;
    box-sizing: border-box;

    background: white;

    border: 1px solid #E2EAF2;
    border-left: 5px solid var(--accent,#3479B7);

    border-radius: 13px;
    padding: 13px 16px;

    box-shadow: 0 3px 12px rgba(26,53,86,.05);

    transition:
        transform .17s,
        box-shadow .17s;
}

.kpi:hover {
    transform: translateY(-2px);
    box-shadow: 0 7px 17px rgba(26,53,86,.11);
}

.kpi-label {
    color: #66798D;
    font-size: .76rem;
    font-weight: 750;
    margin-bottom: 8px;
}

.kpi-value {
    color: #193B61;
    font-weight: 800;
    font-size: 1.42rem;
    line-height: 1.25;
    overflow-wrap: anywhere;
}

.kpi.featured {
    background: linear-gradient(
        140deg,
        #FFFFFF,
        #F7FAFF
    );

    border-left-width: 6px;
}

.kpi.featured .kpi-value {
    font-size: 1.69rem;
    color: var(--accent,#193B61);
}

.kpi-note {
    color: #738499;
    font-size: .70rem;
    margin-top: 7px;
}

.kpi-status {
    float: right;

    background: #EDF2F7;
    color: #355472;

    border-radius: 99px;
    padding: 3px 7px;

    font-size: .63rem;
    font-weight: 800;
}

/* Native metric untuk YoY */

[data-testid="stMetric"] {
    height: 124px;
    min-height: 124px;

    border: 1px solid #E2EAF2;
    border-left: 5px solid #3479B7;

    border-radius: 13px;

    background: white;
    box-shadow: 0 3px 12px rgba(26,53,86,.05);

    padding: 12px 15px;
    box-sizing: border-box;
}

[data-testid="stMetricLabel"] p {
    font-size: .77rem !important;
    color: #687C91 !important;
}

[data-testid="stMetricValue"] {
    font-size: 1.40rem !important;
    color: #193B61 !important;
    font-weight: 800 !important;
}

/* ============================================================
   TABS - JARAK LEBIH RAPI
   ============================================================ */

[data-baseweb="tab-list"] {
    display: flex !important;
    flex-wrap: wrap !important;

    gap: 11px !important;

    background: #E9F0F7 !important;

    padding: 9px !important;
    border-radius: 13px !important;

    margin-bottom: 14px !important;
    border-bottom: 0 !important;
}

[data-baseweb="tab"] {
    margin: 0 !important;
    padding: 10px 19px !important;

    min-height: 42px !important;
    border-radius: 10px !important;

    background: transparent !important;

    white-space: nowrap !important;

    color: #405D78 !important;
    font-weight: 750 !important;
}

[data-baseweb="tab"][aria-selected="true"] {
    background: white !important;
    color: #193B61 !important;

    box-shadow: 0 2px 9px rgba(17,49,82,.11) !important;
}

[data-baseweb="tab-highlight"],
[data-baseweb="tab-border"] {
    display: none !important;
}

/* ============================================================
   FILTER BULAN
   ============================================================ */

.month-summary {
    background: #FFFFFF;

    border: 1px solid #DCE7F2;
    border-radius: 12px;

    padding: 12px 15px;
    margin: 3px 0 12px;

    color: #193B61;
    font-size: .84rem;
}

.month-summary strong {
    font-weight: 800;
}

/* Tombol popover pengaturan bulan */

[data-testid="stPopover"] button {
    border: 1px solid #B6CBDE !important;
    border-radius: 10px !important;

    background: white !important;
    color: #193B61 !important;

    font-weight: 750 !important;
}

[data-testid="stPopover"] button:hover {
    border-color: #3479B7 !important;
    background: #F0F5FA !important;
}

/* ============================================================
   PANEL GRAFIK
   ============================================================ */

[data-testid="stVerticalBlockBorderWrapper"]:has(iframe),
[data-testid="stVerticalBlockBorderWrapper"]:has([data-testid="stPlotlyChart"]) {
    border-radius: 15px !important;
    background: #FFFFFF !important;

    border-color: #E2EAF2 !important;

    box-shadow: 0 4px 13px rgba(28,54,87,.05) !important;
}

/* ============================================================
   INSIGHT
   ============================================================ */

.insight {
    min-height: 126px;

    border: 1px solid #E4EBF3;
    border-radius: 12px;

    padding: 15px;
    background: white;

    box-shadow: 0 3px 12px rgba(20,50,82,.05);
}

.insight-label {
    color: #6B7D92;
    font-size: .71rem;
    font-weight: 750;

    text-transform: uppercase;
    letter-spacing: .04em;
}

.insight-value {
    color: #193B61;
    font-size: 1.07rem;
    font-weight: 800;

    margin: 8px 0 5px;
}

.insight-detail {
    color: #5E738A;
    font-size: .76rem;
    line-height: 1.55;
}

/* ============================================================
   CUSTOM CALLOUT
   ============================================================ */

.callout {
    border: 1px solid #E0E8F0;
    border-left: 5px solid var(--accent);

    background: var(--fill);

    padding: 13px 16px;
    border-radius: 11px;

    margin: 9px 0 13px;

    color: #36516B;
    font-size: .84rem;
    line-height: 1.65;
}

.callout strong {
    color: #193B61;
}

/* ============================================================
   PRIORITY BADGE
   ============================================================ */

.priority {
    border-radius: 99px;
    padding: 4px 10px;

    color: var(--accent);
    background: var(--fill);

    font-weight: 800;
    font-size: .74rem;

    display: inline-block;
}

/* ============================================================
   FOOTER
   ============================================================ */

.footer {
    border-top: 1px solid #DDE7F0;

    margin-top: 26px;
    padding-top: 13px;

    color: #748599;
    font-size: .72rem;

    display: flex;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 8px;
}
</style>
""", unsafe_allow_html=True)


# =============================================================
# 3. FUNGSI FORMAT
# =============================================================

def fmt(x, digit=2):

    if pd.isna(x):
        return "—"

    return (
        f"{float(x):,.{digit}f}"
        .replace(",", "_")
        .replace(".", ",")
        .replace("_", ".")
    )


def uang(x):

    if pd.isna(x):
        return "—"

    x = float(x)

    sign = "−" if x < 0 else ""
    a = abs(x)

    if a >= 1e12:
        return f"{sign}Rp{fmt(a / 1e12)} T"

    if a >= 1e9:
        return f"{sign}Rp{fmt(a / 1e9)} M"

    if a >= 1e6:
        return f"{sign}Rp{fmt(a / 1e6)} Jt"

    return f"{sign}Rp{fmt(a, 0)}"


# =============================================================
# 4. HTML RENDERER
# =============================================================

def html(content, place=None):

    target = (
        place
        if place is not None
        else st
    )

    cleaned = " ".join(
        s.strip()
        for s in content.splitlines()
        if s.strip()
    )

    if hasattr(target, "html"):

        target.html(cleaned)

    else:

        target.markdown(
            cleaned,
            unsafe_allow_html=True
        )


# =============================================================
# 5. KOMPONEN TAMPILAN
# =============================================================

def hero(title, desc, period):

    html(
        f'''
        <section class="hero">

            <div class="hero-eyebrow">
                BAPENDA KOTA SURABAYA · ANALISIS BPHTB
            </div>

            <h1>{escape(title)}</h1>

            <div class="hero-desc">
                {escape(desc)}
            </div>

            <div class="hero-period">
                Periode: {escape(period)}
            </div>

        </section>
        '''
    )


def kpi(
    label,
    value,
    tone="blue",
    note="",
    featured=False,
    status=""
):

    colors = {
        "blue": BLUE,
        "gold": GOLD,
        "green": GREEN,
        "red": RED,
        "navy": NAVY
    }

    accent = colors.get(tone, BLUE)

    status_tag = (
        f'<span class="kpi-status">{escape(str(status))}</span>'
        if status
        else ""
    )

    klass = (
        "kpi featured"
        if featured
        else "kpi"
    )

    html(
        f'''
        <div class="{klass}"
             style="--accent:{accent}">

            <div class="kpi-label">
                {escape(str(label))}
                {status_tag}
            </div>

            <div class="kpi-value">
                {escape(str(value))}
            </div>

            <div class="kpi-note">
                {escape(str(note)) if note else '&nbsp;'}
            </div>

        </div>
        '''
    )


def callout(tone, title, message):

    tones = {
        "success": (GREEN, "#EDF9F5"),
        "warning": (GOLD, "#FFF9E9"),
        "danger": (RED, "#FFF1F2"),
        "info": (BLUE, "#EFF6FD")
    }

    accent, fill = tones.get(
        tone,
        tones["info"]
    )

    html(
        f'''
        <div class="callout"
             style="--accent:{accent};--fill:{fill}">

            <strong>{escape(title)}</strong>

            <div>
                {escape(message)}
            </div>

        </div>
        '''
    )


def insight(label, value, detail):

    html(
        f'''
        <div class="insight">

            <div class="insight-label">
                {escape(label)}
            </div>

            <div class="insight-value">
                {escape(str(value))}
            </div>

            <div class="insight-detail">
                {escape(detail)}
            </div>

        </div>
        '''
    )


# =============================================================
# 6. LOGO DASHBOARD
# =============================================================

@st.cache_data(show_spinner=False)
def create_logo():

    """
    Logo dibuat langsung dengan Pillow.

    Tidak bergantung pada HTML/SVG sehingga
    tidak muncul lagi kotak emas kosong.
    """

    im = Image.new(
        "RGBA",
        (256, 256),
        (0, 0, 0, 0)
    )

    dr = ImageDraw.Draw(im)

    # Latar emas
    dr.rounded_rectangle(
        (5, 5, 250, 250),
        radius=57,
        fill=(231, 183, 81, 255)
    )

    # Atap bangunan
    dr.polygon(
        [
            (38, 108),
            (127, 53),
            (217, 108)
        ],
        fill=(20, 51, 82, 255)
    )

    # Balok atas
    dr.rounded_rectangle(
        (42, 110, 212, 124),
        radius=3,
        fill=(20, 51, 82, 255)
    )

    # Pilar bangunan
    for x in (62, 111, 160):

        dr.rounded_rectangle(
            (x, 129, x + 30, 198),
            radius=4,
            fill=(20, 51, 82, 255)
        )

    # Dasar bangunan
    dr.rounded_rectangle(
        (39, 204, 215, 217),
        radius=3,
        fill=(20, 51, 82, 255)
    )

    dr.rounded_rectangle(
        (29, 221, 225, 231),
        radius=4,
        fill=(20, 51, 82, 255)
    )

    # Garis pertumbuhan penerimaan
    dr.line(
        [
            (59, 183),
            (94, 162),
            (122, 177),
            (165, 140),
            (193, 151)
        ],
        fill=(255, 255, 255, 255),
        width=10,
        joint="curve"
    )

    dr.ellipse(
        (188, 146, 200, 158),
        fill=(255, 255, 255, 255)
    )

    return im.resize(
        (128, 128),
        Image.Resampling.LANCZOS
    )


# =============================================================
# 7. STYLE GRAFIK
# =============================================================

def style_chart(
    fig,
    y_title=None,
    x_title="Bulan",
    height=310
):

    gauge = any(
        tr.type == "indicator"
        for tr in fig.data
    )

    fig.update_layout(
        height=height,

        paper_bgcolor="white",
        plot_bgcolor="white",

        font=dict(
            family="Plus Jakarta Sans, sans-serif",
            color="#36516B",
            size=11
        ),

        margin=dict(
            l=85,
            r=30,
            t=61,
            b=70
        ),

        hovermode="x unified",

        legend=dict(
            orientation="h",
            x=0,
            y=1.03,
            yanchor="bottom"
        ),

        uniformtext=dict(
            minsize=9,
            mode="hide"
        )
    )

    if gauge:

        fig.update_layout(
            showlegend=False,

            margin=dict(
                l=58,
                r=58,
                t=52,
                b=30
            )
        )

    else:

        fig.update_xaxes(
            title_text=x_title,
            title_standoff=12,

            showgrid=False,
            showline=True,

            linecolor="#DFE6EF",
            automargin=True
        )

        fig.update_yaxes(
            title_text=y_title,
            title_standoff=10,

            showgrid=True,
            gridcolor="#EDF1F6",

            automargin=True,
            zeroline=False
        )

    return fig


# =============================================================
# 8. ANIMASI GRAFIK OTOMATIS
# =============================================================

def plot_frames(original):

    fig = go.Figure(original)

    details = []

    low = 0.0
    high = 0.0

    for i, tr in enumerate(original.data):

        if tr.type in ("bar", "scatter"):

            axis = (
                "x"
                if tr.type == "bar"
                and tr.orientation == "h"
                else "y"
            )

            try:

                arr = np.asarray(
                    getattr(tr, axis),
                    dtype=float
                )

            except (TypeError, ValueError):
                continue

            if (
                not arr.size
                or not np.any(np.isfinite(arr))
            ):
                continue

            vals = arr[np.isfinite(arr)]

            low = min(
                low,
                float(vals.min())
            )

            high = max(
                high,
                float(vals.max())
            )

            setattr(
                fig.data[i],
                axis,
                np.zeros_like(arr).tolist()
            )

            if (
                tr.type == "bar"
                and tr.text is not None
            ):

                fig.data[i].text = [
                    ""
                ] * len(arr)

            details.append(
                (
                    i,
                    tr.type,
                    axis,
                    arr,
                    tr.text
                )
            )

        elif tr.type == "heatmap":

            arr = np.asarray(
                tr.z,
                dtype=float
            )

            if arr.size:

                fig.data[i].z = (
                    np.zeros_like(arr).tolist()
                )

                details.append(
                    (
                        i,
                        "heatmap",
                        "z",
                        arr,
                        None
                    )
                )

    if not details:
        return fig

    if (
        fig.layout.yaxis.range is None

        and any(
            axis == "y"
            for _, _, axis, _, _ in details
        )
    ):

        pad = max(
            2,
            (high - low) * .18
        )

        fig.update_yaxes(
            range=[
                min(0, low - pad),
                high + pad
            ]
        )

    fractions = [
        .02,
        .06,
        .13,
        .23,
        .35,
        .49,
        .63,
        .76,
        .86,
        .94,
        .985,
        1.0
    ]

    frames = []

    for j, factor in enumerate(fractions):

        items = []
        indices = []

        for i, typ, axis, arr, labels in details:

            entry = {
                "type": typ,
                axis: (arr * factor).tolist()
            }

            if (
                typ == "bar"
                and labels is not None
            ):

                entry["text"] = (
                    list(labels)
                    if j == len(fractions) - 1
                    else [""] * len(arr)
                )

            items.append(entry)
            indices.append(i)

        frames.append(
            go.Frame(
                data=items,
                traces=indices,
                name=f"frame{j}"
            )
        )

    fig.frames = frames

    return fig


def show_chart(chart, height=310):

    """
    Animasi aktif untuk semua grafik.

    Gauge menggunakan animasi nilai,
    sedangkan bar/line/heatmap menggunakan
    frame Plotly.
    """

    gauges = [
        {
            "idx": i,
            "value": float(tr.value)
        }

        for i, tr in enumerate(chart.data)

        if (
            tr.type == "indicator"
            and tr.value is not None
        )
    ]

    if gauges:

        animated = go.Figure(chart)

        for item in gauges:

            animated.data[
                item["idx"]
            ].value = 0

    else:

        animated = plot_frames(chart)

    widget = pio.to_html(
        animated,

        full_html=False,
        include_plotlyjs=True,

        auto_play=not bool(gauges),

        animation_opts={
            "frame": {
                "duration": 90,
                "redraw": True
            },

            "transition": {
                "duration": 85,
                "easing": "cubic-in-out"
            },

            "mode": "immediate"
        },

        config={
            "responsive": True,
            "displaylogo": False,

            "modeBarButtonsToRemove": [
                "lasso2d",
                "select2d"
            ]
        },

        default_width="100%",
        default_height=f"{height}px"
    )

    # Animasi khusus gauge
    if gauges:

        widget += """
        <script>
        (function() {
            const goals = __GOALS__;

            const reduced = window.matchMedia(
                '(prefers-reduced-motion: reduce)'
            ).matches;

            function start() {
                const gd = document.querySelector(
                    '.js-plotly-plot'
                );

                if (
                    !gd ||
                    !gd._fullLayout ||
                    typeof Plotly === 'undefined'
                ) {
                    requestAnimationFrame(start);
                    return;
                }

                const begin = performance.now();
                let last = 0;

                function tick(now) {
                    const p = reduced
                        ? 1
                        : Math.min(
                            1,
                            (now - begin) / 1250
                        );

                    if (
                        p < 1 &&
                        now - last < 42
                    ) {
                        requestAnimationFrame(tick);
                        return;
                    }

                    last = now;

                    const smooth =
                        1 - Math.pow(1-p, 3);

                    goals.forEach(g => {
                        Plotly.restyle(
                            gd,
                            {
                                value: [
                                    g.value * smooth
                                ]
                            },
                            [g.idx]
                        );
                    });

                    if (p < 1) {
                        requestAnimationFrame(tick);
                    }
                }

                requestAnimationFrame(tick);
            }

            requestAnimationFrame(start);
        })();
        </script>
        """.replace(
            "__GOALS__",
            json.dumps(gauges)
        )

    widget = (
        "<style>"
        "html,body{margin:0;padding:0;"
        "background:white;overflow:hidden;}"
        "@media(prefers-reduced-motion:reduce){"
        ".js-plotly-plot{animation:none!important;}}"
        "</style>"
        + widget
    )

    components.html(
        widget,
        height=height + 9,
        scrolling=False
    )


def panel(
    title,
    fig,
    interpretation,
    key,
    ylabel=None,
    xlabel="Bulan",
    height=310
):

    with st.container(border=True):

        st.markdown(f"##### {title}")

        show_chart(
            style_chart(
                fig,
                ylabel,
                xlabel,
                height
            ),
            height
        )

        st.markdown(
            f"**Interpretasi:** {interpretation}"
        )


# =============================================================
# 9. GRAFIK TARGET - REALISASI
# =============================================================

def target_chart(df):

    fig = go.Figure()

    for col, name, color in [
        ("target_rp", "Target", GOLD),
        ("realisasi_rp", "Realisasi", BLUE)
    ]:

        values = df[col] / 1e9

        fig.add_bar(
            x=df.bulan,
            y=values,

            name=name,
            marker_color=color,

            text=[
                fmt(v, 0)
                for v in values
            ],

            textposition="outside",

            hovertemplate=(
                f"%{{x}}<br>"
                f"{name}: Rp%{{y:,.2f}} M"
                "<extra></extra>"
            )
        )

    fig.update_layout(
        barmode="group"
    )

    peak = df.loc[
        df.realisasi_rp.idxmax()
    ]

    fig.add_annotation(
        x=peak.bulan,
        y=peak.realisasi_rp / 1e9,

        text="Puncak realisasi",
        showarrow=True,

        ax=0,
        ay=-28,

        bgcolor="#EEF5FC",

        font=dict(
            color=NAVY,
            size=10
        )
    )

    return fig


# =============================================================
# 10. TABS
# =============================================================

def tabs(labels, key):

    try:

        return st.tabs(
            labels,
            key=key,
            on_change="rerun"
        )

    except TypeError:

        return st.tabs(labels)


def opened(tab):

    return getattr(
        tab,
        "open",
        None
    ) is not False


# =============================================================
# 11. LOKASI DATASET
# =============================================================

ROOT = Path(__file__).resolve().parent

FOLDERS = {
    "raw": "01_Data_Preparation",
    "np": "02_Statistika_Nonparametrik",
    "model": "03_Pemodelan_Data_Bisnis",
    "policy": "04_Analisis_Kebijakan"
}

FILES = {

    "master": (
        "raw",
        "BPHTB_Master_Bulanan_2021_2026.csv"
    ),

    "kategori": (
        "raw",
        "BPHTB_Rincian_Kategori_2026.csv"
    ),

    "audit_open": (
        "raw",
        "temuan_audit_terbuka.csv"
    ),

    "friedman": (
        "np",
        "hasil_friedman.csv"
    ),

    "rank": (
        "np",
        "peringkat_bulanan.csv"
    ),

    "spearman": (
        "np",
        "korelasi_spearman_tahunan.csv"
    ),

    "sens": (
        "np",
        "sensitivitas_spearman.csv"
    ),

    "posthoc": (
        "np",
        "posthoc_friedman_holm.csv"
    ),

    "profil": (
        "model",
        "profil_risiko_bulanan.csv"
    ),

    "risk_selected": (
        "model",
        "metode_risiko_terpilih.csv"
    ),

    "risk_compare": (
        "model",
        "evaluasi_hs_sdpp.csv"
    ),

    "backtest": (
        "model",
        "rolling_backtesting.csv"
    ),

    "extreme": (
        "model",
        "risiko_ekstrem.csv"
    ),

    "pred_selected": (
        "model",
        "model_prediksi_terpilih.csv"
    ),

    "pred_series": (
        "model",
        "prediksi_model_terpilih_2026.csv"
    ),

    "pred_eval": (
        "model",
        "evaluasi_model_2026.csv"
    ),

    "pred_validation": (
        "model",
        "seleksi_model_validasi_2024_2025.csv"
    ),

    "policy_selected": (
        "policy",
        "skenario_terpilih_dashboard.csv"
    ),

    "policy_tradeoff": (
        "policy",
        "tradeoff_uji_2025.csv"
    ),

    "indicator": (
        "policy",
        "indikator_bulanan.csv"
    ),

    "recommend": (
        "policy",
        "matriks_rekomendasi.csv"
    ),
}


# =============================================================
# 12. MEMBACA DATA
# =============================================================

PATHS = {
    name: ROOT / FOLDERS[folder] / filename

    for name, (folder, filename)
    in FILES.items()
}

missing = [
    str(path.relative_to(ROOT))

    for path in PATHS.values()
    if not path.exists()
]

if missing:

    st.error(
        "CSV final belum lengkap. "
        "Pastikan empat folder dataset "
        "berada sejajar dengan app.py."
    )

    st.code(
        "\n".join(missing)
    )

    st.stop()


@st.cache_data(show_spinner=False)
def load_data():

    return {
        name: pd.read_csv(path)

        for name, path
        in PATHS.items()
    }


d = load_data()


# =============================================================
# 13. VALIDASI KOLOM CSV
# =============================================================

required = {

    "master": [
        "tahun",
        "bulan_ke",
        "periode",
        "status_nilai",
        "target_rp",
        "realisasi_rp",
        "proyeksi_rp",
        "nilai_seri_rp",
        "jumlah_sspd"
    ],

    "kategori": [
        "periode",
        "kategori",
        "nilai_seri_rp"
    ],

    "audit_open": [
        "pemeriksaan",
        "hasil",
        "status",
        "tindak_lanjut"
    ],

    "friedman": [
        "statistik_uji",
        "p_value_permutasi",
        "kendalls_w"
    ],

    "spearman": [
        "tahun",
        "spearman_rho"
    ],

    "rank": [
        "bulan_ke",
        "bulan",
        "rata_rata_rank"
    ],

    "sens": [
        "metode",
        "spearman_rho"
    ],

    "posthoc": [
        "signifikan_5pct"
    ],

    "profil": [
        "bulan_ke",
        "bulan",
        "frekuensi_gagal_persen"
    ],

    "risk_selected": [
        "metode_terpilih",
        "tingkat_keyakinan",
        "batas_nominal_rp",
        "batas_relatif_persen"
    ],

    "risk_compare": [
        "jenis_risiko",
        "metode",
        "rata_pinball_loss",
        "pelampauan_persen"
    ],

    "backtest": [
        "tahun_uji",
        "tingkat_pelampauan_nominal",
        "tingkat_pelampauan_relatif"
    ],

    "extreme": [
        "periode",
        "jenis_risiko",
        "shortfall_rp",
        "shortfall_persen"
    ],

    "pred_selected": [
        "model_terpilih"
    ],

    "pred_series": [
        "periode",
        "aktual_rp",
        "prediksi_terpilih_rp"
    ],

    "pred_eval": [
        "model",
        "MAE_miliar",
        "RMSE_miliar",
        "WAPE_persen"
    ],

    "pred_validation": [
        "model",
        "MAE_validasi_miliar"
    ],

    "policy_selected": [
        "bobot_historis_terpilih",
        "MAE_uji_miliar",
        "shortfall_uji_miliar"
    ],

    "policy_tradeoff": [
        "MAE_baseline_miliar",
        "MAE_skenario_miliar",
        "bulan_gagal_baseline",
        "bulan_gagal_skenario"
    ],

    "indicator": [
        "bulan_ke",
        "bulan",
        "rata_gap_share_pp"
    ],

    "recommend": [
        "prioritas",
        "isu",
        "dasar_analisis",
        "rekomendasi",
        "batasan",
        "tindak_lanjut"
    ]
}

bad = {
    name: [
        c
        for c in cols
        if c not in d[name].columns
    ]

    for name, cols in required.items()
}

bad = {
    name: cols
    for name, cols in bad.items()
    if cols
}

if bad:

    st.error(
        "Struktur kolom data berbeda "
        "dari paket final."
    )

    st.json(bad)
    st.stop()


# =============================================================
# 14. PERSIAPAN MASTER DATA
# =============================================================

m = d["master"].copy()

m["status_nilai"] = (
    m.status_nilai
    .astype(str)
    .str.strip()
)

for col in [
    "tahun",
    "bulan_ke",
    "target_rp",
    "realisasi_rp",
    "proyeksi_rp",
    "nilai_seri_rp",
    "jumlah_sspd"
]:

    m[col] = pd.to_numeric(
        m[col],
        errors="coerce"
    )

m = m.sort_values(
    ["tahun", "bulan_ke"]
).reset_index(drop=True)

h = m[
    m.tahun.between(2021, 2025)
    & m.status_nilai.eq("Realisasi")
].copy()

h["bulan"] = h.bulan_ke.map(BULAN)

h["shortfall_rp"] = (
    h.target_rp - h.realisasi_rp
).clip(lower=0)

h["shortfall_pct"] = (
    100 * h.shortfall_rp / h.target_rp
)


# =============================================================
# 15. FUNGSI ANALITIK
# =============================================================

def valid_history():

    return (
        len(h) == 60

        and not h[
            ["tahun", "bulan_ke"]
        ].duplicated().any()

        and all(
            set(
                h.loc[
                    h.tahun.eq(y),
                    "bulan_ke"
                ]
            ) == set(range(1, 13))

            for y in range(2021, 2026)
        )

        and h[
            [
                "target_rp",
                "realisasi_rp",
                "jumlah_sspd"
            ]
        ].notna().all().all()

        and (h.target_rp > 0).all()

        and (h.realisasi_rp >= 0).all()

        and (h.jumlah_sspd >= 0).all()
    )


def audit_statistics():

    if not valid_history():
        return None

    matrix = h.pivot(
        index="tahun",
        columns="bulan_ke",
        values="realisasi_rp"
    )

    chi2 = float(
        friedmanchisquare(
            *[
                matrix[n].to_numpy()
                for n in range(1, 13)
            ]
        ).statistic
    )

    w = chi2 / (5 * 11)

    rho = float(
        spearmanr(
            h.jumlah_sspd,
            h.realisasi_rp
        ).statistic
    )

    ref = d["friedman"].iloc[0]

    rho_ref = d["sens"].loc[
        d["sens"].metode.eq("Seluruh data"),
        "spearman_rho"
    ]

    if rho_ref.empty:
        return None

    match = all(
        np.isclose(
            a,
            b,
            rtol=0,
            atol=1e-5
        )

        for a, b in [
            (
                chi2,
                float(ref.statistik_uji)
            ),

            (
                w,
                float(ref.kendalls_w)
            ),

            (
                rho,
                float(rho_ref.iloc[0])
            )
        ]
    )

    return {
        "chi2": chi2,
        "w": w,
        "rho": rho,
        "p": float(ref.p_value_permutasi),
        "match": match
    }


def annual_rho(df):

    if (
        len(df) < 3

        or df.jumlah_sspd.nunique() < 2

        or df.realisasi_rp.nunique() < 2
    ):
        return np.nan

    return float(
        spearmanr(
            df.jumlah_sspd,
            df.realisasi_rp
        ).statistic
    )


def yoy(df, year):

    previous = m[
        (m.tahun == year - 1)

        & m.status_nilai.eq("Realisasi")

        & m.bulan_ke.isin(df.bulan_ke)
    ]

    if (
        len(previous) != len(df)

        or set(previous.bulan_ke) != set(df.bulan_ke)

        or previous.realisasi_rp.sum() <= 0
    ):
        return None

    return 100 * (
        df.realisasi_rp.sum()
        / previous.realisasi_rp.sum()
        - 1
    )


# =============================================================
# 16. KPI PENDAPATAN
# =============================================================

def revenue_kpis(df, year):

    target = df.target_rp.sum()
    actual = df.realisasi_rp.sum()
    sspd = df.jumlah_sspd.sum()

    cap = 100 * actual / target
    growth = yoy(df, year)

    items = [
        (
            "Target penerimaan",
            uang(target),
            "gold",
            "Total bulan terpilih",
            False,
            ""
        ),

        (
            "Capaian target",
            f"{fmt(cap)}%",

            "green"
            if cap >= 100
            else "red",

            "Target tercapai"
            if cap >= 100
            else "Belum mencapai target",

            True,

            "TERCAPAI"
            if cap >= 100
            else "BELUM"
        ),

        (
            "Realisasi penerimaan",
            uang(actual),
            "blue",
            "Total realisasi aktual",
            False,
            ""
        )
    ]

    for col, item in zip(
        st.columns(3, gap="small"),
        items
    ):

        with col:

            kpi(*item)

    a, b, c = st.columns(
        3,
        gap="small"
    )

    with a:

        kpi(
            "Jumlah SSPD",
            fmt(sspd, 0),
            "blue",
            "Dokumen pembayaran"
        )

    with b:

        kpi(
            "Selisih realisasi − target",

            uang(actual - target),

            "green"
            if actual >= target
            else "red",

            "Surplus"
            if actual >= target
            else "Kekurangan"
        )

    with c:

        text = (
            "—"
            if growth is None

            else (
                "Naik"
                if growth > 0

                else (
                    "Turun"
                    if growth < 0
                    else "Tetap"
                )
            )
        )

        st.metric(
            "Tren YoY setara",

            text,

            delta=(
                f"{fmt(growth)}%"
                if growth is not None
                else None
            )
        )

    return growth


def attention(df):

    fail = df[
        df.realisasi_rp < df.target_rp
    ].copy()

    if fail.empty:

        callout(
            "success",
            "Sorotan kinerja bulanan",
            "Semua bulan pada periode pilihan "
            "mencapai target."
        )

        return

    fail["gap_pct"] = (
        100
        * (
            fail.target_rp
            - fail.realisasi_rp
        )
        / fail.target_rp
    )

    worst = fail.loc[
        fail.gap_pct.idxmax()
    ]

    callout(
        "warning",

        "Sorotan kinerja bulanan",

        f"{len(fail)} dari {len(df)} bulan "
        "belum mencapai target. "

        f"Shortfall relatif terbesar pada "
        f"{worst.bulan}, {fmt(worst.gap_pct)}% "

        f"atau "
        f"{uang(worst.target_rp - worst.realisasi_rp)}. "

        "Ini hasil monitoring, bukan prediksi."
    )


# =============================================================
# 17. SIDEBAR
# =============================================================

with st.sidebar:

    logo_col, text_col = st.columns(
        [1, 2.7],
        gap="small",
        vertical_alignment="center"
    )

    with logo_col:

        st.image(
            create_logo(),
            width=67
        )

    with text_col:

        html(
            '''
            <div class="sidebar-brand-name">
                BPHTB Analytics
            </div>

            <div class="sidebar-brand-sub">
                REVENUE INTELLIGENCE
            </div>

            <div class="sidebar-brand-agency">
                Bapenda Kota Surabaya
            </div>
            '''
        )

    st.divider()

    st.markdown(
        "**FILTER PERIODE**"
    )

    years = sorted(
        m.tahun
        .dropna()
        .astype(int)
        .unique()
    )

    year = st.selectbox(
        "Tahun realisasi",

        years,

        index=(
            years.index(2025)
            if 2025 in years
            else 0
        )
    )


# =============================================================
# 18. MENU NAVIGASI
# =============================================================

MENU = [
    ("Beranda", ":material/home:"),
    ("Ringkasan Pendapatan", ":material/bar_chart:"),
    ("Validasi Data", ":material/fact_check:"),
    ("Pola Penerimaan", ":material/monitoring:"),
    ("Risiko Pendapatan", ":material/shield:"),
    ("Evaluasi Prediksi", ":material/insights:"),
    ("Evaluasi Kebijakan", ":material/account_balance:"),
]

if "halaman_aktif" not in st.session_state:

    st.session_state.halaman_aktif = "Beranda"


def navigate(name):

    st.session_state.halaman_aktif = name


with st.sidebar:

    for name, icon in MENU:

        st.button(
            name,

            icon=icon,

            use_container_width=True,

            type=(
                "primary"
                if st.session_state.halaman_aktif == name
                else "secondary"
            ),

            key=(
                "nav_"
                + name.replace(" ", "_")
            ),

            on_click=navigate,
            args=(name,)
        )

    html(
        '''
        <div class="sidebar-note">
            Filter tahun hanya berlaku untuk
            pemantauan realisasi; analisis lain
            memakai periodenya masing-masing.
        </div>
        '''
    )

page = st.session_state.halaman_aktif


# =============================================================
# 19. DATA TAHUN TERPILIH
# =============================================================

akt = m[
    (m.tahun == year)

    & m.status_nilai.eq("Realisasi")
].copy()

if (
    akt.empty

    or akt[
        [
            "target_rp",
            "realisasi_rp",
            "jumlah_sspd"
        ]
    ].isna().any().any()

    or (akt.target_rp <= 0).any()

    or (akt.realisasi_rp < 0).any()

    or (akt.jumlah_sspd < 0).any()
):

    st.error(
        "Data aktual tidak lengkap atau "
        "terdapat nilai yang tidak valid."
    )

    st.stop()

akt["bulan"] = akt.bulan_ke.map(BULAN)

akt["capaian"] = (
    100 * akt.realisasi_rp / akt.target_rp
)

akt["target_kum"] = akt.target_rp.cumsum()

akt["real_kum"] = akt.realisasi_rp.cumsum()

akt["shortfall_rp"] = (
    akt.target_rp - akt.realisasi_rp
).clip(lower=0)

akt["shortfall_pct"] = (
    100 * akt.shortfall_rp / akt.target_rp
)

period = (
    f"Januari–Desember {year}"

    if len(akt) == 12

    else (
        f"Januari–"
        f"{BULAN[int(akt.bulan_ke.max())]} "
        f"{year} "
        f"({len(akt)} bulan aktual)"
    )
)


# =============================================================
# HALAMAN 1 - BERANDA
# =============================================================

if page == "Beranda":

    hero(
        "Dashboard Analisis BPHTB",

        "Pemantauan penerimaan dan capaian target "
        "BPHTB untuk mendukung evaluasi "
        "pendapatan daerah.",

        period
    )

    revenue_kpis(akt, year)

    st.subheader(
        "Ikhtisar penerimaan"
    )

    a, b = st.columns(
        [1.65, 1],
        gap="medium"
    )

    # ---------------------------------------------------------
    # GRAFIK TARGET DAN REALISASI
    # ---------------------------------------------------------

    with a:

        peak = akt.loc[
            akt.realisasi_rp.idxmax()
        ]

        panel(
            "Target dan Realisasi Bulanan",

            target_chart(akt),

            f"{int((akt.capaian >= 100).sum())} "
            f"dari {len(akt)} bulan mencapai target. "

            f"Realisasi tertinggi pada "
            f"{peak.bulan} sebesar "
            f"{uang(peak.realisasi_rp)}.",

            "home_target",

            "Penerimaan (Rp miliar)",

            height=340
        )

    # ---------------------------------------------------------
    # GAUGE CAPAIAN
    # ---------------------------------------------------------

    with b:

        achieved = (
            100
            * akt.realisasi_rp.sum()
            / akt.target_rp.sum()
        )

        top = max(
            120,

            int(
                np.ceil(achieved / 10) * 10
            ) + 10
        )

        gauge = go.Figure(
            go.Indicator(
                mode="gauge+number",

                value=achieved,

                number=dict(
                    suffix="%",
                    valueformat=".1f",

                    font=dict(
                        size=29,
                        color=NAVY
                    )
                ),

                gauge=dict(
                    axis=dict(
                        range=[0, top],

                        tickmode="array",

                        tickvals=[
                            0,
                            50,
                            100
                        ],

                        ticktext=[
                            "0",
                            "50",
                            "100%"
                        ],

                        tickfont=dict(
                            size=10
                        )
                    ),

                    bar=dict(
                        color=(
                            GREEN
                            if achieved >= 100
                            else RED
                        )
                    ),

                    steps=[
                        dict(
                            range=[0, 100],
                            color="#F9E9E9"
                        ),

                        dict(
                            range=[100, top],
                            color="#E0F3EC"
                        )
                    ],

                    threshold=dict(
                        line=dict(
                            color=GOLD,
                            width=4
                        ),

                        thickness=.7,
                        value=100
                    )
                )
            )
        )

        panel(
            "Capaian Periode Terpilih",

            gauge,

            f"Capaian agregat sebesar "
            f"{fmt(achieved)}%; "

            + (
                "target tercapai."
                if achieved >= 100
                else "target belum tercapai."
            ),

            "home_gauge",

            height=340,
            xlabel=None
        )

    attention(akt)


# =============================================================
# HALAMAN 2 - RINGKASAN PENDAPATAN
# =============================================================

elif page == "Ringkasan Pendapatan":

    hero(
        "Ringkasan Pendapatan",

        "Perkembangan target, realisasi, capaian, "
        "dan SSPD per bulan.",

        period
    )

    available = (
        akt.bulan_ke
        .astype(int)
        .tolist()
    )

    # ---------------------------------------------------------
    # FILTER BULAN PROFESIONAL
    # ---------------------------------------------------------

    a, b = st.columns(
        [1.1, 3],
        vertical_alignment="center",
        gap="small"
    )

    with a:

        with st.popover(
            "Atur bulan",

            icon=":material/calendar_month:",

            use_container_width=True
        ):

            st.markdown(
                "**Pilih bulan yang dianalisis**"
            )

            checks = st.columns(4)

            for i, n in enumerate(available):

                key = f"filter_{year}_{n}"

                if key not in st.session_state:

                    st.session_state[key] = True

                with checks[i % 4]:

                    st.checkbox(
                        BULAN[n],
                        key=key
                    )

            f1, f2 = st.columns(2)

            with f1:

                if st.button(
                    "Semua bulan",
                    use_container_width=True
                ):

                    for n in available:

                        st.session_state[
                            f"filter_{year}_{n}"
                        ] = True

                    st.rerun()

            with f2:

                if st.button(
                    "Kosongkan",
                    use_container_width=True
                ):

                    for n in available:

                        st.session_state[
                            f"filter_{year}_{n}"
                        ] = False

                    st.rerun()

    selected = [
        n

        for n in available

        if st.session_state.get(
            f"filter_{year}_{n}",
            True
        )
    ]

    with b:

        label = (
            "Semua bulan dipilih"

            if len(selected) == len(available)

            else (
                f"{len(selected)} bulan dipilih: "

                + ", ".join(
                    BULAN[n]
                    for n in selected
                )
            )
        )

        html(
            f'''
            <div class="month-summary">

                <strong>Periode analisis:</strong>

                {escape(label)}

            </div>
            '''
        )

    if not selected:

        callout(
            "warning",

            "Belum ada bulan dipilih",

            "Klik Atur bulan lalu pilih "
            "minimal satu bulan."
        )

        st.stop()

    z = akt[
        akt.bulan_ke.isin(selected)
    ].copy()

    growth = revenue_kpis(z, year)

    st.caption(
        "KPI dihitung dari bulan terpilih; "
        "akumulasi kumulatif tetap "
        "dimulai dari Januari."
    )

    # ---------------------------------------------------------
    # TARGET VS REALISASI
    # ---------------------------------------------------------

    c1, c2 = st.columns(2)

    with c1:

        panel(
            "Target vs Realisasi",

            target_chart(z),

            f"Dari {len(z)} bulan, "

            f"{int((z.capaian >= 100).sum())} "
            "mencapai target. "

            f"Total realisasi "
            f"{uang(z.realisasi_rp.sum())}.",

            "ring_target",

            "Penerimaan (Rp miliar)"
        )

    # ---------------------------------------------------------
    # CAPAIAN BULANAN
    # ---------------------------------------------------------

    with c2:

        fig = go.Figure(
            go.Bar(
                x=z.bulan,
                y=z.capaian,

                marker_color=[
                    GREEN if x >= 100 else RED
                    for x in z.capaian
                ],

                text=[
                    f"{fmt(x, 0)}%"
                    for x in z.capaian
                ],

                textposition="outside",

                hovertemplate=(
                    "%{x}: %{y:.2f}%"
                    "<extra></extra>"
                )
            )
        )

        fig.add_hline(
            y=100,

            line=dict(
                color=GOLD,
                dash="dash"
            )
        )

        panel(
            "Capaian Target Bulanan",

            fig,

            f"Capaian tertinggi: "
            f"{z.loc[z.capaian.idxmax(), 'bulan']} "

            f"({fmt(z.capaian.max())}%). "

            f"Sebanyak "
            f"{int((z.capaian < 100).sum())} "

            "bulan belum memenuhi target.",

            "ring_cap",

            "Capaian target (%)"
        )

    # ---------------------------------------------------------
    # KUMULATIF DAN SSPD
    # ---------------------------------------------------------

    c3, c4 = st.columns(2)

    with c3:

        fig = go.Figure()

        for col, name, color in [
            (
                "target_kum",
                "Target kumulatif",
                GOLD
            ),

            (
                "real_kum",
                "Realisasi kumulatif",
                BLUE
            )
        ]:

            fig.add_scatter(
                x=z.bulan,
                y=z[col] / 1e9,

                name=name,
                mode="lines+markers",

                line=dict(
                    color=color,
                    width=3
                ),

                hovertemplate=(
                    "%{x}: Rp%{y:,.2f} M"
                    "<extra></extra>"
                )
            )

        panel(
            "Tren Kumulatif",

            fig,

            f"Sampai {z.iloc[-1].bulan}, "

            f"realisasi kumulatif "
            f"{uang(z.iloc[-1].real_kum)} "

            f"dan target kumulatif "
            f"{uang(z.iloc[-1].target_kum)}.",

            "ring_cum",

            "Kumulatif (Rp miliar)"
        )

    with c4:

        fig = go.Figure(
            go.Bar(
                x=z.bulan,
                y=z.jumlah_sspd,

                marker_color=BLUE,

                text=[
                    fmt(x, 0)
                    for x in z.jumlah_sspd
                ],

                textposition="outside"
            )
        )

        panel(
            "Jumlah SSPD",

            fig,

            f"Jumlah SSPD tertinggi: "
            f"{z.loc[z.jumlah_sspd.idxmax(), 'bulan']} "

            f"({fmt(z.jumlah_sspd.max(), 0)} "
            "dokumen); "

            f"total "
            f"{fmt(z.jumlah_sspd.sum(), 0)} "
            "dokumen.",

            "ring_sspd",

            "Jumlah SSPD (dokumen)"
        )

    # ---------------------------------------------------------
    # YEAR ON YEAR
    # ---------------------------------------------------------

    if growth is not None:

        prev = m[
            (m.tahun == year - 1)

            & m.status_nilai.eq("Realisasi")

            & m.bulan_ke.isin(z.bulan_ke)
        ]

        prev = (
            prev.set_index("bulan_ke")
            .reindex(z.bulan_ke)
        )

        fig = go.Figure()

        fig.add_bar(
            x=z.bulan,

            y=prev.realisasi_rp / 1e9,

            name=str(year - 1),
            marker_color=NAVY
        )

        fig.add_bar(
            x=z.bulan,

            y=z.realisasi_rp / 1e9,

            name=str(year),
            marker_color=BLUE
        )

        fig.update_layout(
            barmode="group"
        )

        direction = (
            "meningkat"
            if growth > 0

            else (
                "menurun"
                if growth < 0
                else "tetap"
            )
        )

        panel(
            "Perbandingan Tahun ke Tahun",

            fig,

            f"Pada bulan yang setara, "
            f"penerimaan {year} {direction} "

            f"{fmt(abs(growth))}% "

            f"dibandingkan {year - 1}.",

            "ring_yoy",

            "Realisasi (Rp miliar)"
        )

    # ---------------------------------------------------------
    # PROYEKSI 2026
    # ---------------------------------------------------------

    if year == 2026:

        projection = m[
            (m.tahun == 2026)

            & m.status_nilai.eq("Proyeksi")
        ]

        if not projection.empty:

            with st.expander(
                "Detail proyeksi sumber "
                "September–Desember 2026"
            ):

                fig = go.Figure()

                fig.add_scatter(
                    x=akt.periode,
                    y=akt.realisasi_rp / 1e9,

                    name="Realisasi",
                    mode="lines+markers",

                    line=dict(
                        color=BLUE
                    )
                )

                fig.add_scatter(
                    x=projection.periode,
                    y=projection.proyeksi_rp / 1e9,

                    name="Proyeksi sumber",
                    mode="lines+markers",

                    line=dict(
                        color=GOLD,
                        dash="dash"
                    )
                )

                show_chart(
                    style_chart(
                        fig,

                        "Penerimaan (Rp miliar)",
                        "Periode",
                        300
                    ),

                    300
                )

                st.markdown(
                    "**Interpretasi:** Proyeksi sumber "
                    "September–Desember berjumlah "

                    f"{uang(projection.proyeksi_rp.sum())}; "

                    "bukan realisasi atau "
                    "prediksi model terpilih."
                )


# =============================================================
# HALAMAN 3 - VALIDASI DATA
# =============================================================

elif page == "Validasi Data":

    hero(
        "Validasi Data",

        "Pemeriksaan kelengkapan historis, "
        "konsistensi, dan catatan audit sumber.",

        period
    )

    t1, t2, t3 = tabs(
        [
            "Tahun terpilih",
            "Audit historis",
            "Catatan sumber"
        ],

        "tabs_validasi"
    )

    # ---------------------------------------------------------
    # TAB 1
    # ---------------------------------------------------------

    if opened(t1):

        with t1:

            required_months = set(
                range(
                    1,
                    9 if year == 2026 else 13
                )
            )

            n_na = int(
                akt[
                    [
                        "target_rp",
                        "realisasi_rp",
                        "jumlah_sspd"
                    ]
                ].isna().sum().sum()
            )

            n_dup = int(
                m[
                    m.tahun.eq(year)
                ].periode.duplicated().sum()
            )

            okay = (
                set(akt.bulan_ke) == required_months

                and len(akt) == len(required_months)

                and n_na == 0

                and n_dup == 0
            )

            checks = [
                (
                    "Bulan realisasi",
                    f"{len(akt)}/{len(required_months)}",
                    okay
                ),

                (
                    "Nilai kosong",
                    fmt(n_na, 0),
                    n_na == 0
                ),

                (
                    "Duplikasi periode",
                    fmt(n_dup, 0),
                    n_dup == 0
                ),

                (
                    "Status teknis",
                    "Sesuai" if okay else "Periksa",
                    okay
                )
            ]

            for col, (label, val, good) in zip(
                st.columns(4),
                checks
            ):

                with col:

                    kpi(
                        label,
                        val,

                        "green"
                        if good
                        else "red"
                    )

            callout(
                "success" if okay else "warning",

                "Pemeriksaan tahun",

                f"Kondisi teknis data {period}: "

                + (
                    "sesuai."
                    if okay
                    else "perlu pemeriksaan."
                )
            )

    # ---------------------------------------------------------
    # TAB 2
    # ---------------------------------------------------------

    if opened(t2):

        with t2:

            cat = d["kategori"].copy()

            cat["nilai_seri_rp"] = pd.to_numeric(
                cat.nilai_seri_rp,
                errors="coerce"
            )

            agg = (
                cat.groupby(
                    "periode",
                    as_index=False
                ).nilai_seri_rp.sum()
            )

            check2026 = m[
                m.tahun.eq(2026)
            ][
                [
                    "periode",
                    "nilai_seri_rp"
                ]
            ].merge(
                agg,

                on="periode",
                how="left",

                suffixes=(
                    "_master",
                    "_kategori"
                )
            )

            mismatch = (
                int(
                    (
                        ~np.isclose(
                            check2026.nilai_seri_rp_master,
                            check2026.nilai_seri_rp_kategori,

                            atol=1,
                            rtol=0
                        )
                    ).sum()
                )

                + max(
                    0,
                    12 - len(check2026)
                )
            )

            result = audit_statistics()

            checks = [
                (
                    "60 bulan historis",
                    valid_history()
                ),

                (
                    "Duplikasi master",
                    not m.periode.duplicated().any()
                ),

                (
                    "Duplikasi kategori",
                    not cat[
                        [
                            "periode",
                            "kategori"
                        ]
                    ].duplicated().any()
                ),

                (
                    "Rekonsiliasi 2026",
                    mismatch == 0
                ),

                (
                    "Reproduksi statistik",

                    bool(
                        result
                        and result["match"]
                    )
                )
            ]

            for col, (name, good) in zip(
                st.columns(5),
                checks
            ):

                with col:

                    kpi(
                        name,

                        "Sesuai"
                        if good
                        else "Periksa",

                        "green"
                        if good
                        else "red"
                    )

            if result:

                a, b, c = st.columns(3)

                with a:

                    kpi(
                        "Friedman χ²",
                        fmt(result["chi2"], 4),
                        "navy"
                    )

                with b:

                    kpi(
                        "Kendall's W",
                        fmt(result["w"], 4),
                        "blue"
                    )

                with c:

                    kpi(
                        "Spearman ρ",
                        fmt(result["rho"], 4),
                        "blue"
                    )

                callout(
                    "success"
                    if result["match"]
                    else "warning",

                    "Reproduksi statistik",

                    "Angka cocok dengan CSV arsip."
                    if result["match"]

                    else (
                        "Terdapat perbedaan terhadap "
                        "CSV arsip."
                    )
                )

            else:

                callout(
                    "danger",
                    "Statistik tidak dapat dihitung",
                    "Periksa kelengkapan historis."
                )

            st.caption(
                "P-value permutasi Friedman dibaca "
                "dari hasil notebook, bukan "
                "dihitung ulang di dashboard."
            )

    # ---------------------------------------------------------
    # TAB 3
    # ---------------------------------------------------------

    if opened(t3):

        with t3:

            if d["audit_open"].empty:

                callout(
                    "success",
                    "Audit sumber",
                    "Tidak terdapat temuan terbuka."
                )

            else:

                for _, r in d["audit_open"].iterrows():

                    callout(
                        "warning",

                        str(r.pemeriksaan),

                        f"Hasil: {r.hasil}; "
                        f"status: {r.status}. "

                        f"Tindak lanjut: "
                        f"{r.tindak_lanjut}."
                    )


# =============================================================
# HALAMAN 4 - POLA PENERIMAAN
# =============================================================

elif page == "Pola Penerimaan":

    hero(
        "Pola Penerimaan",

        "Pola tahun terpilih dan hasil "
        "pengujian nonparametrik historis "
        "2021–2025.",

        period
    )

    rho_year = annual_rho(akt)

    items = [
        (
            "Rata-rata",
            uang(akt.realisasi_rp.mean())
        ),

        (
            "Median",
            uang(akt.realisasi_rp.median())
        ),

        (
            "Korelasi SSPD (ρ)",
            fmt(rho_year, 3)
        ),

        (
            "Bulan aktual",
            str(len(akt))
        )
    ]

    for col, (name, val) in zip(
        st.columns(4),
        items
    ):

        with col:

            kpi(
                name,
                val,
                "blue"
            )

    a, b = st.columns(2)

    # ---------------------------------------------------------
    # TARGET - REALISASI TAHUN PILIHAN
    # ---------------------------------------------------------

    with a:

        fig = go.Figure()

        fig.add_scatter(
            x=akt.bulan,
            y=akt.realisasi_rp / 1e9,

            name="Realisasi",
            mode="lines+markers",

            line=dict(
                color=BLUE
            )
        )

        fig.add_scatter(
            x=akt.bulan,
            y=akt.target_rp / 1e9,

            name="Target",
            mode="lines+markers",

            line=dict(
                color=GOLD,
                dash="dash"
            )
        )

        peak = akt.loc[
            akt.realisasi_rp.idxmax()
        ]

        panel(
            "Pola Target dan Realisasi",

            fig,

            f"Realisasi tertinggi pada "
            f"{peak.bulan} sebesar "
            f"{uang(peak.realisasi_rp)}; "

            f"{int((akt.capaian < 100).sum())} "
            "bulan belum mencapai target.",

            "pola_line",

            "Penerimaan (Rp miliar)"
        )

    # ---------------------------------------------------------
    # SSPD VS REALISASI
    # ---------------------------------------------------------

    with b:

        fig = go.Figure(
            go.Scatter(
                x=akt.jumlah_sspd,
                y=akt.realisasi_rp / 1e9,

                mode="markers",

                marker=dict(
                    size=10,
                    color=BLUE
                )
            )
        )

        panel(
            "SSPD dan Realisasi",

            fig,

            f"Korelasi Spearman tahun {year} "
            f"adalah ρ={fmt(rho_year, 3)}; "

            "ini hubungan, bukan bukti sebab-akibat.",

            "pola_scatter",

            "Realisasi (Rp miliar)",

            xlabel="Jumlah SSPD (dokumen)"
        )

    # ---------------------------------------------------------
    # HASIL UJI HISTORIS
    # ---------------------------------------------------------

    st.subheader(
        "Pengujian historis 2021–2025"
    )

    result = audit_statistics()

    if (
        result is None

        or not result["match"]
    ):

        callout(
            "danger",

            "Validasi historis tidak cocok",

            "Periksa bagian Validasi Data."
        )

        st.stop()

    items = [
        (
            "Friedman χ²",
            fmt(result["chi2"], 4)
        ),

        (
            "P permutasi",
            fmt(result["p"], 6)
        ),

        (
            "Kendall's W",
            fmt(result["w"], 4)
        ),

        (
            "Spearman ρ",
            fmt(result["rho"], 4)
        )
    ]

    for col, (name, val) in zip(
        st.columns(4),
        items
    ):

        with col:

            kpi(
                name,
                val,
                "navy"
            )

    n_sig = int(
        d["posthoc"]
        .signifikan_5pct
        .astype(str)
        .str.strip()
        .str.lower()
        .eq("true")
        .sum()
    )

    callout(
        "info",

        "Hasil pengujian",

        f"Pada uji lanjut Holm, {n_sig} dari "
        f"{len(d['posthoc'])} pasangan bulan "
        "signifikan (daya uji terbatas: "
        "hanya 5 tahun pengamatan)."
    )

    a, b = st.columns(2)

    # ---------------------------------------------------------
    # FRIEDMAN
    # ---------------------------------------------------------

    with a:

        rank = d["rank"].sort_values(
            "bulan_ke"
        )

        fig = go.Figure(
            go.Bar(
                x=rank.bulan,
                y=rank.rata_rata_rank,

                marker_color=BLUE,

                text=[
                    fmt(x, 1)
                    for x in rank.rata_rata_rank
                ],

                textposition="outside"
            )
        )

        maxrow = rank.loc[
            rank.rata_rata_rank.idxmax()
        ]

        panel(
            "Peringkat Friedman",

            fig,

            f"Peringkat rata-rata tertinggi "
            f"pada {maxrow.bulan} "

            f"({fmt(maxrow.rata_rata_rank)}).",

            "pola_rank",

            "Rata-rata peringkat"
        )

    # ---------------------------------------------------------
    # RATA-RATA DAN MEDIAN
    # ---------------------------------------------------------

    with b:

        stat = (
            h.groupby("bulan_ke")
            .realisasi_rp

            .agg([
                "mean",
                "median"
            ])

            .reset_index()
        )

        fig = go.Figure()

        fig.add_bar(
            x=stat.bulan_ke.map(BULAN),
            y=stat["mean"] / 1e9,

            name="Rata-rata",
            marker_color=BLUE
        )

        fig.add_bar(
            x=stat.bulan_ke.map(BULAN),
            y=stat["median"] / 1e9,

            name="Median",
            marker_color=GOLD
        )

        fig.update_layout(
            barmode="group"
        )

        maxrow = stat.loc[
            stat["mean"].idxmax()
        ]

        panel(
            "Rata-rata vs Median Historis",

            fig,

            f"Rata-rata tertinggi terdapat "
            f"pada {BULAN[int(maxrow.bulan_ke)]}: "

            f"{uang(maxrow['mean'])}.",

            "pola_stat",

            "Realisasi (Rp miliar)"
        )

    # ---------------------------------------------------------
    # DETAIL SPEARMAN
    # ---------------------------------------------------------

    with st.expander(
        "Detail Spearman tahunan dan sensitivitas"
    ):

        st.dataframe(
            d["spearman"][
                [
                    "tahun",
                    "spearman_rho"
                ]
            ],

            hide_index=True,
            use_container_width=True
        )

        s = d["sens"]

        fig = go.Figure(
            go.Bar(
                x=s.spearman_rho,
                y=s.metode,

                orientation="h",
                marker_color=BLUE
            )
        )

        show_chart(
            style_chart(
                fig,

                "Metode analisis",
                "Koefisien Spearman (ρ)"
            ),

            310
        )

        st.markdown(
            "**Interpretasi:** nilai sensitivitas "
            f"berkisar "
            f"{fmt(s.spearman_rho.min(), 3)} "

            "hingga "

            f"{fmt(s.spearman_rho.max(), 3)}."
        )


# =============================================================
# HALAMAN 5 - RISIKO PENDAPATAN
# =============================================================

elif page == "Risiko Pendapatan":

    hero(
        "Risiko Ketidaktercapaian Target",

        "Monitoring shortfall dan batas "
        "risiko historis terpilih.",

        period
    )

    if not valid_history():

        callout(
            "danger",

            "Historis tidak valid",

            "Periksa menu Validasi Data."
        )

        st.stop()

    ri = d["risk_selected"].iloc[0]

    name = str(
        ri.metode_terpilih
    )

    limit_rp = (
        float(ri.batas_nominal_rp)
        / 1e9
    )

    limit_pct = float(
        ri.batas_relatif_persen
    )

    conf = (
        float(ri.tingkat_keyakinan)
        * 100
    )

    items = [
        (
            "Bulan belum tercapai",

            f"{int((akt.shortfall_rp > 0).sum())}"
            f"/{len(akt)}"
        ),

        (
            "Total shortfall",

            uang(akt.shortfall_rp.sum())
        ),

        (
            "Shortfall terbesar",

            uang(akt.shortfall_rp.max())
        ),

        (
            f"Batas historis {fmt(conf, 0)}%",

            uang(limit_rp * 1e9)
        )
    ]

    for col, (label, val) in zip(
        st.columns(4),
        items
    ):

        with col:

            kpi(
                label,
                val,

                "gold"
                if "Batas" in label
                else "red"
            )

    # ---------------------------------------------------------
    # SHORTFALL
    # ---------------------------------------------------------

    choice = st.radio(
        "Satuan shortfall",

        [
            "Nominal (Rp miliar)",
            "Relatif (%)"
        ],

        horizontal=True
    )

    nominal = choice.startswith(
        "Nominal"
    )

    vals = (
        akt.shortfall_rp / 1e9
        if nominal
        else akt.shortfall_pct
    )

    limit = (
        limit_rp
        if nominal
        else limit_pct
    )

    fig = go.Figure()

    fig.add_bar(
        x=akt.bulan,
        y=vals,

        name="Shortfall",

        marker_color=[
            RED if x > limit else GOLD
            for x in vals
        ],

        text=[
            fmt(x, 1)
            for x in vals
        ],

        textposition="outside"
    )

    fig.add_scatter(
        x=akt.bulan,

        y=[
            limit
        ] * len(akt),

        name="Batas historis",
        mode="lines",

        line=dict(
            color=NAVY,
            dash="dash"
        )
    )

    extreme = akt.loc[
        akt.shortfall_rp.idxmax()
    ]

    panel(
        "Shortfall Bulanan",

        fig,

        f"Shortfall terbesar terjadi pada "
        f"{extreme.bulan}, "

        f"{uang(extreme.shortfall_rp)}. "

        f"Batas {name} {fmt(conf, 0)}% "
        f"adalah {uang(limit_rp * 1e9)}.",

        "risk_shortfall",

        "Shortfall (Rp miliar)"
        if nominal
        else "Shortfall relatif (%)"
    )

    attention(akt)

    # ---------------------------------------------------------
    # ALASAN PEMILIHAN METODE
    # ---------------------------------------------------------

    with st.expander(
        "Alasan pemilihan metode risiko"
    ):

        comp = d["risk_compare"]

        for _, r in comp[
            comp.jenis_risiko.eq("nominal")
        ].iterrows():

            st.write(
                f"**{r.metode}**: "

                f"pinball loss "
                f"Rp{fmt(r.rata_pinball_loss)} miliar; "

                f"pelampauan "
                f"{fmt(r.pelampauan_persen)}%."
            )

        st.caption(
            "Pemilihan metode menggunakan "
            "evaluasi historis, bukan kepastian "
            "risiko masa depan."
        )

    # ---------------------------------------------------------
    # PROFIL RISIKO
    # ---------------------------------------------------------

    profile = d["profil"].sort_values(
        "bulan_ke"
    )

    fig = go.Figure(
        go.Bar(
            x=profile.bulan,

            y=profile.frekuensi_gagal_persen,

            marker_color=RED,

            text=[
                f"{fmt(x, 0)}%"
                for x in profile.frekuensi_gagal_persen
            ],

            textposition="outside"
        )
    )

    top = profile.loc[
        profile.frekuensi_gagal_persen.idxmax()
    ]

    panel(
        "Frekuensi Gagal Target Historis",

        fig,

        f"Frekuensi tertinggi pada {top.bulan}: "

        f"{fmt(top.frekuensi_gagal_persen, 0)}% "

        "dari lima tahun pengamatan.",

        "risk_freq",

        "Frekuensi gagal (%)"
    )

    # ---------------------------------------------------------
    # HEATMAP
    # ---------------------------------------------------------

    mat = h.pivot(
        index="tahun",
        columns="bulan_ke",
        values="shortfall_pct"
    ).reindex(
        columns=range(1, 13)
    )

    fig = go.Figure(
        go.Heatmap(
            z=mat.to_numpy(),

            x=list(BULAN.values()),

            y=[
                str(x)
                for x in mat.index
            ],

            colorscale=[
                [0, "#EDF6F4"],
                [.5, "#F2D8A5"],
                [1, "#C7474F"]
            ],

            zmin=0,

            zmax=max(
                60,
                float(
                    np.nanmax(
                        mat.to_numpy()
                    )
                )
            ),

            colorbar=dict(
                title="%"
            )
        )
    )

    panel(
        "Heatmap Shortfall 2021–2025",

        fig,

        f"Shortfall relatif maksimum pada "
        "data historis sebesar "

        f"{fmt(np.nanmax(mat.to_numpy()))}%. "

        "Warna lebih gelap menunjukkan "
        "kekurangan yang lebih besar.",

        "risk_heat",

        "Tahun",

        xlabel="Bulan"
    )

    # ---------------------------------------------------------
    # DETAIL BACKTESTING
    # ---------------------------------------------------------

    with st.expander(
        "Detail backtesting dan risiko ekstrem"
    ):

        bt = d["backtest"].sort_values(
            "tahun_uji"
        )

        fig = go.Figure()

        fig.add_bar(
            x=bt.tahun_uji.astype(str),

            y=bt.tingkat_pelampauan_nominal,

            name="Nominal",
            marker_color=BLUE
        )

        fig.add_bar(
            x=bt.tahun_uji.astype(str),

            y=bt.tingkat_pelampauan_relatif,

            name="Relatif",
            marker_color=GOLD
        )

        fig.add_hline(
            y=5,

            line=dict(
                color=RED,
                dash="dash"
            )
        )

        fig.update_layout(
            barmode="group"
        )

        show_chart(
            style_chart(
                fig,

                "Pelampauan (%)",
                "Tahun uji"
            ),

            310
        )

        st.markdown(
            "**Interpretasi:** frekuensi pelampauan "
            "dibandingkan patokan teoretis 5%; "
            "sampel evaluasi terbatas."
        )

        for _, r in d["extreme"].iterrows():

            st.write(
                f"{r.periode} · {r.jenis_risiko}: "

                f"{uang(float(r.shortfall_rp) * 1e9)} "

                f"({fmt(r.shortfall_persen)}%)."
            )


# =============================================================
# HALAMAN 6 - EVALUASI PREDIKSI
# =============================================================

elif page == "Evaluasi Prediksi":

    hero(
        "Evaluasi Prediksi Penerimaan",

        "Model dipilih pada validasi 2024–2025 "
        "dan diuji Januari–Agustus 2026.",

        "Januari–Agustus 2026 (evaluasi tetap)"
    )

    name = str(
        d["pred_selected"]
        .iloc[0]
        .model_terpilih
    )

    v = d["pred_validation"][
        d["pred_validation"].model.eq(name)
    ]

    e = d["pred_eval"][
        d["pred_eval"].model.eq(name)
    ]

    pr = d["pred_series"].sort_values(
        "periode"
    ).copy()

    if (
        v.empty

        or e.empty

        or len(pr) != 8

        or pr.periode.duplicated().any()

        or pr[
            [
                "aktual_rp",
                "prediksi_terpilih_rp"
            ]
        ].isna().any().any()
    ):

        callout(
            "danger",

            "Data evaluasi tidak konsisten",

            "Periksa file prediksi CSV final."
        )

        st.stop()

    v = v.iloc[0]
    e = e.iloc[0]

    calc = (
        (
            pr.prediksi_terpilih_rp
            - pr.aktual_rp
        ).abs().mean()

        / 1e9
    )

    if not np.isclose(
        calc,

        float(e.MAE_miliar),

        atol=1e-4,
        rtol=0
    ):

        callout(
            "danger",
            "MAE berbeda",
            "Seri prediksi tidak sama "
            "dengan hasil evaluasi."
        )

        st.stop()

    items = [
        (
            "Model terpilih",
            name
        ),

        (
            "MAE validasi",
            uang(v.MAE_validasi_miliar * 1e9)
        ),

        (
            "MAE uji 2026",
            uang(e.MAE_miliar * 1e9)
        ),

        (
            "WAPE uji 2026",
            f"{fmt(e.WAPE_persen)}%"
        )
    ]

    for col, (label, val) in zip(
        st.columns(4),
        items
    ):

        with col:

            kpi(
                label,
                val,

                "navy"
                if label == "Model terpilih"
                else "blue"
            )

    # ---------------------------------------------------------
    # GRAFIK PREDIKSI
    # ---------------------------------------------------------

    fig = go.Figure()

    fig.add_scatter(
        x=pr.periode,
        y=pr.aktual_rp / 1e9,

        name="Realisasi",
        mode="lines+markers",

        line=dict(
            color=BLUE,
            width=3
        )
    )

    fig.add_scatter(
        x=pr.periode,
        y=pr.prediksi_terpilih_rp / 1e9,

        name=name,
        mode="lines+markers",

        line=dict(
            color=GOLD,
            dash="dash",
            width=3
        )
    )

    panel(
        "Prediksi Model Terpilih vs Realisasi",

        fig,

        f"MAE model {name} pada uji 2026 "
        f"adalah {uang(e.MAE_miliar * 1e9)}. "

        "Prediksi satu langkah ke depan, "
        "bukan proyeksi setahun penuh.",

        "pred_series",

        "Penerimaan (Rp miliar)",

        xlabel="Periode (bulan)",
        height=360
    )

    best = d["pred_eval"].nsmallest(
        1,
        "MAE_miliar"
    ).iloc[0]

    if best.model != name:

        callout(
            "info",

            "Model paling akurat pada uji akhir berbeda",

            f"{name} dipilih dari validasi. "

            f"Pada uji 2026, {best.model} "
            "memiliki MAE terendah "

            f"{uang(best.MAE_miliar * 1e9)}; "

            "hasil uji akhir tidak digunakan "
            "untuk mengubah pilihan."
        )

    # ---------------------------------------------------------
    # DETAIL SELISIH
    # ---------------------------------------------------------

    with st.expander(
        "Detail selisih prediksi bulanan"
    ):

        a, b = st.columns(2)

        with a:

            kpi(
                "RMSE uji",

                uang(e.RMSE_miliar * 1e9),

                "blue"
            )

        with b:

            kpi(
                "Periode uji",
                "8 bulan",
                "navy"
            )

        err = (
            pr.prediksi_terpilih_rp
            - pr.aktual_rp
        ) / 1e9

        fig = go.Figure(
            go.Bar(
                x=pr.periode,
                y=err,

                marker_color=[
                    RED if v > 0 else BLUE
                    for v in err
                ]
            )
        )

        fig.add_hline(
            y=0,
            line_color=NAVY
        )

        show_chart(
            style_chart(
                fig,

                "Prediksi − aktual (Rp miliar)",
                "Periode uji"
            ),

            310
        )

        st.markdown(
            "**Interpretasi:** nilai positif "
            "berarti prediksi di atas aktual."
        )


# =============================================================
# HALAMAN 7 - EVALUASI KEBIJAKAN
# =============================================================

elif page == "Evaluasi Kebijakan":

    hero(
        "Evaluasi Target dan Kebijakan",

        "Evaluasi porsi target bulanan dan "
        "skenario kebijakan terpilih.",

        period
    )

    t1, t2, t3 = tabs(
        [
            "Distribusi",
            "Skenario",
            "Rekomendasi"
        ],

        "tabs_kebijakan"
    )

    # ---------------------------------------------------------
    # TAB 1 - DISTRIBUSI
    # ---------------------------------------------------------

    if opened(t1):

        with t1:

            total_t = akt.target_rp.sum()
            total_r = akt.realisasi_rp.sum()

            if (
                total_t <= 0

                or total_r <= 0
            ):

                st.error(
                    "Target atau realisasi tidak valid."
                )

                st.stop()

            zz = akt[
                [
                    "bulan",
                    "bulan_ke",
                    "target_rp",
                    "realisasi_rp"
                ]
            ].copy()

            zz["gap_pp"] = (
                100
                * (
                    zz.target_rp / total_t

                    - zz.realisasi_rp / total_r
                )
            )

            maximum = zz.loc[
                zz.gap_pp.idxmax()
            ]

            a, b, c = st.columns(3)

            with a:

                kpi(
                    "Bulan aktual",
                    len(zz),
                    "navy"
                )

            with b:

                kpi(
                    "Bulan gap positif",

                    f"{int((zz.gap_pp > 0).sum())} bulan",

                    "gold"
                )

            with c:

                kpi(
                    "Gap maksimum",

                    f"{fmt(maximum.gap_pp)} pp",

                    "gold",

                    f"Bulan {maximum.bulan}"
                )

            fig = go.Figure(
                go.Bar(
                    x=zz.bulan,
                    y=zz.gap_pp,

                    marker_color=[
                        GOLD if v > 0 else BLUE
                        for v in zz.gap_pp
                    ],

                    text=[
                        fmt(v, 1)
                        for v in zz.gap_pp
                    ],

                    textposition="outside"
                )
            )

            fig.add_hline(
                y=0,
                line_color=NAVY
            )

            keterangan = (
                "Pada 2026, proporsi hanya "
                "berdasarkan Jan–Agu."

                if year == 2026

                else (
                    "Proporsi dihitung terhadap "
                    "satu tahun penuh."
                )
            )

            panel(
                "Selisih Porsi Target − Realisasi",

                fig,

                f"Gap positif maksimum pada "
                f"{maximum.bulan} sebesar "
                f"{fmt(maximum.gap_pp)} pp. "

                + keterangan,

                "policy_gap",

                "Selisih porsi (pp)"
            )

    # ---------------------------------------------------------
    # TAB 2 - SKENARIO
    # ---------------------------------------------------------

    if opened(t2):

        with t2:

            info = d["policy_selected"].iloc[0]

            trade = d["policy_tradeoff"].iloc[0]

            weight = float(
                info.bobot_historis_terpilih
            )

            mae0 = float(
                trade.MAE_baseline_miliar
            )

            mae1 = float(
                trade.MAE_skenario_miliar
            )

            fail0 = int(
                trade.bulan_gagal_baseline
            )

            fail1 = int(
                trade.bulan_gagal_skenario
            )

            if not np.isclose(
                mae1,

                float(info.MAE_uji_miliar),

                atol=1e-5
            ):

                st.error(
                    "Nilai MAE kebijakan tidak cocok "
                    "antarsumber CSV."
                )

                st.stop()

            items = [
                (
                    "Bobot historis terpilih",
                    f"{fmt(weight * 100, 0)}%"
                ),

                (
                    "MAE uji 2025",
                    uang(mae1 * 1e9)
                ),

                (
                    "Shortfall uji 2025",
                    uang(
                        float(info.shortfall_uji_miliar)
                        * 1e9
                    )
                ),

                (
                    "Bulan gagal 2025",
                    f"{fail1}/12"
                )
            ]

            for col, (label, val) in zip(
                st.columns(4),
                items
            ):

                with col:

                    kpi(
                        label,
                        val,

                        "red"
                        if "gagal" in label.lower()
                        else "blue"
                    )

            names = [
                "Target aktual",

                f"Campuran historis "
                f"{fmt(weight * 100, 0)}%"
            ]

            a, b = st.columns(2)

            # -------------------------------------------------
            # PERBANDINGAN MAE
            # -------------------------------------------------

            with a:

                fig = go.Figure(
                    go.Bar(
                        x=names,

                        y=[
                            mae0,
                            mae1
                        ],

                        marker_color=[
                            NAVY,

                            GREEN
                            if mae1 < mae0
                            else RED
                        ],

                        text=[
                            fmt(mae0, 2),
                            fmt(mae1, 2)
                        ],

                        textposition="outside"
                    )
                )

                panel(
                    "MAE Gap pada Uji 2025",

                    fig,

                    f"MAE berubah dari "
                    f"{uang(mae0 * 1e9)} "

                    f"menjadi "
                    f"{uang(mae1 * 1e9)}.",

                    "policy_mae",

                    "MAE (Rp miliar)",

                    xlabel="Skenario"
                )

            # -------------------------------------------------
            # BULAN GAGAL
            # -------------------------------------------------

            with b:

                fig = go.Figure(
                    go.Bar(
                        x=names,

                        y=[
                            fail0,
                            fail1
                        ],

                        marker_color=[
                            NAVY,

                            RED
                            if fail1 > fail0
                            else GREEN
                        ],

                        text=[
                            str(fail0),
                            str(fail1)
                        ],

                        textposition="outside"
                    )
                )

                panel(
                    "Bulan Tidak Mencapai Target",

                    fig,

                    f"Jumlah bulan gagal berubah "
                    f"dari {fail0} menjadi "
                    f"{fail1} bulan. "

                    "Indikator ini perlu dinilai "
                    "bersama MAE.",

                    "policy_fail",

                    "Jumlah bulan",

                    xlabel="Skenario"
                )

            if fail1 > fail0:

                callout(
                    "warning",

                    "Trade-off yang harus diperhatikan",

                    f"Bobot historis "
                    f"{fmt(weight * 100, 0)}% "

                    "menurunkan MAE tetapi menambah "
                    "bulan gagal "

                    f"dari {fail0} menjadi {fail1}."
                )

            st.caption(
                "Simulasi meredistribusi target bulanan "
                "tanpa menaikkan total realisasi "
                "atau membuktikan efek kausal."
            )

    # ---------------------------------------------------------
    # TAB 3 - REKOMENDASI
    # ---------------------------------------------------------

    if opened(t3):

        with t3:

            st.subheader(
                "Rekomendasi berbasis hasil analisis"
            )

            for i in range(
                0,
                len(d["recommend"]),
                2
            ):

                rows = d["recommend"].iloc[
                    i:i + 2
                ]

                for col, (_, r) in zip(
                    st.columns(2),

                    rows.iterrows()
                ):

                    with col:

                        with st.container(border=True):

                            p = (
                                str(r.prioritas)
                                .strip()
                                .lower()
                            )

                            tone = (
                                RED

                                if p == "tinggi"

                                else (
                                    GOLD
                                    if p == "sedang"
                                    else GREEN
                                )
                            )

                            fill = (
                                "#FDECEE"

                                if p == "tinggi"

                                else (
                                    "#FFF5E5"
                                    if p == "sedang"
                                    else "#EAF8F1"
                                )
                            )

                            # Badge HTML tidak bocor
                            html(
                                f'<span class="priority" '
                                f'style="--accent:{tone};'
                                f'--fill:{fill}">'

                                f'Prioritas '
                                f'{escape(str(r.prioritas))}'

                                f'</span>'
                            )

                            st.markdown(
                                f"**{r.isu}**"
                            )

                            st.write(
                                r.rekomendasi
                            )

                            st.caption(
                                f"Dasar: {r.dasar_analisis}"
                            )

                            with st.expander(
                                "Tindak lanjut dan batasan"
                            ):

                                st.markdown(
                                    "**Tindak lanjut**"
                                )

                                st.write(
                                    r.tindak_lanjut
                                )

                                st.markdown(
                                    "**Keterbatasan**"
                                )

                                st.write(
                                    r.batasan
                                )

            # -------------------------------------------------
            # DETAIL HISTORIS
            # -------------------------------------------------

            with st.expander(
                "Detail pola porsi target 2021–2025"
            ):

                hist = d["indicator"].sort_values(
                    "bulan_ke"
                )

                fig = go.Figure(
                    go.Bar(
                        x=hist.bulan,
                        y=hist.rata_gap_share_pp,

                        marker_color=BLUE,

                        text=[
                            fmt(v, 2)

                            for v in hist.rata_gap_share_pp
                        ],

                        textposition="outside"
                    )
                )

                fig.add_hline(
                    y=0,
                    line_color=NAVY
                )

                show_chart(
                    style_chart(
                        fig,

                        "Rata-rata gap porsi (pp)",
                        "Bulan"
                    ),

                    310
                )

                row = hist.loc[
                    hist.rata_gap_share_pp.idxmax()
                ]

                st.markdown(
                    "**Interpretasi:** rata-rata gap "
                    "porsi tertinggi pada "

                    f"{row.bulan}, "

                    f"{fmt(row.rata_gap_share_pp)} pp."
                )


# =============================================================
# 20. FOOTER
# =============================================================

latest = m[
    m.status_nilai.eq("Realisasi")
].sort_values(
    ["tahun", "bulan_ke"]
).iloc[-1]

last_date = (
    f"{BULAN[int(latest.bulan_ke)]} "
    f"{int(latest.tahun)}"
)

updated = datetime.now(
    ZoneInfo("Asia/Jakarta")
).strftime(
    "%d/%m/%Y %H:%M WIB"
)

html(
    f'''
    <div class="footer">

        <span>
            Sumber: data BPHTB Bapenda Kota Surabaya
            · notebook perhitungan final
        </span>

        <span>
            Data aktual terakhir:
            {escape(last_date)}
            · Dimuat {escape(updated)}
        </span>

    </div>
    '''
)