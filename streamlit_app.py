import streamlit as st
from streamlit_lottie import st_lottie
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit.components.v1 as components

# --------------------- Page & Global CSS ---------------------
st.set_page_config(layout="wide")

st.markdown("""
<style>
:root { --content-max: 1200px; --content-pad: 2rem; }

/* 1) Hilangkan padding global supaya bisa buat segmen full-bleed */
.block-container{
  padding-left: 0 !important;
  padding-right: 0 !important;
  max-width: 100% !important;
}

/* 2) Kembalikan layout normal via wrapper */
.content-wrap{
  max-width: var(--content-max);
  margin: 0 auto;
  padding: 0 var(--content-pad);
}

/* Spasi vertikal antar section (opsional) */
.section-spacer{ height: 16px; }

/* Typo helper */
.title-text {
  font-size: 2.8rem;
  font-weight: 800;
  margin-bottom: 1rem;
  color: #3498db;
}
.paragraph-text {
  font-size: 1.1rem;
  line-height: 1.6;
  text-align: justify;
}

@media (max-width: 600px){
  .content-wrap{ padding: 0 1rem; }
}
</style>
""", unsafe_allow_html=True)

# --------------------- Data & Figures ---------------------
data_total = [
    ["University Graduates with a major in STEM fields", "Currently attending school and not engaged in any form of employment", 1.89],
    ["University Graduates with a major in STEM fields", "Engaged in any form of employment", 79.39],
    ["University Graduates with a major in STEM fields", "No longer attending school and not employed", 18.72],
    ["Engaged in any form of employment", "STEM Jobs", 18.39],
    ["Engaged in any form of employment", "Not in STEM Jobs", 61.00],
]


data_male = [
    ["University Graduates with a major in STEM fields", "Currently attending school and not engaged in any form of employment", 0.53],
    ["University Graduates with a major in STEM fields", "Engaged in any form of employment", 87.11],
    ["University Graduates with a major in STEM fields", "No longer attending school and not employed", 12.35],
    ["Engaged in any form of employment", "STEM Jobs", 25.17],
    ["Engaged in any form of employment", "Not in STEM Jobs", 61.94],
]


data_female = [
    ["University Graduates with a major in STEM fields", "Currently attending school and not engaged in any form of employment", 1.06],
    ["University Graduates with a major in STEM fields", "Engaged in any form of employment", 74.67],
    ["University Graduates with a major in STEM fields", "No longer attending school and not employed", 24.27],
    ["Engaged in any form of employment", "STEM Jobs", 30.36],
    ["Engaged in any form of employment", "Not in STEM Jobs", 44.31],
]


data_sumatera = [
    ["University Graduates with a major in STEM fields", "Currently attending school and not engaged in any form of employment", 0.55],
    ["University Graduates with a major in STEM fields", "Engaged in any form of employment", 80.25],
    ["University Graduates with a major in STEM fields", "No longer attending school and not employed", 19.20],
    ["Engaged in any form of employment", "STEM Jobs", 25.03],
    ["Engaged in any form of employment", "Not in STEM Jobs", 55.22],
]


data_jawa_bali = [
    ["University Graduates with a major in STEM fields", "Currently attending school and not engaged in any form of employment", 0.88],
    ["University Graduates with a major in STEM fields", "Engaged in any form of employment", 80.57],
    ["University Graduates with a major in STEM fields", "No longer attending school and not employed", 18.54],
    ["Engaged in any form of employment", "STEM Jobs", 29.19],
    ["Engaged in any form of employment", "Not in STEM Jobs", 51.38],
]


data_kalimatan = [
    ["University Graduates with a major in STEM fields", "Currently attending school and not engaged in any form of employment", 0.70],
    ["University Graduates with a major in STEM fields", "Engaged in any form of employment", 82.62],
    ["University Graduates with a major in STEM fields", "No longer attending school and not employed", 16.68],
    ["Engaged in any form of employment", "STEM Jobs", 27.39],
    ["Engaged in any form of employment", "Not in STEM Jobs", 55.23],
]

data_sulawesi = [
    ["University Graduates with a major in STEM fields", "Currently attending school and not engaged in any form of employment", 1.31],
    ["University Graduates with a major in STEM fields", "Engaged in any form of employment", 79.50],
    ["University Graduates with a major in STEM fields", "No longer attending school and not employed", 19.19],
    ["Engaged in any form of employment", "STEM Jobs", 26.84],
    ["Engaged in any form of employment", "Not in STEM Jobs", 52.66],
]

data_nustra_mal_papua = [
    ["University Graduates with a major in STEM fields", "Currently attending school and not engaged in any form of employment", 0.36],
    ["University Graduates with a major in STEM fields", "Engaged in any form of employment", 85.23],
    ["University Graduates with a major in STEM fields", "No longer attending school and not employed", 14.41],
    ["Engaged in any form of employment", "STEM Jobs", 27.51],
    ["Engaged in any form of employment", "Not in STEM Jobs", 57.71],
]


dataset_map = {
    "All": data_total,
    "Male": data_male,
    "Female": data_female,
    "Sumatera": data_sumatera,
    "Jawa–Bali": data_jawa_bali,
    "Kalimantan": data_kalimatan,
    "Sulawesi": data_sulawesi,
    "Nusa Tenggara, Maluku, Papua": data_nustra_mal_papua

}

def make_sankey(data):
    df = pd.DataFrame(data, columns=["source", "target", "value"])
    all_nodes = list(pd.unique(df[['source', 'target']].values.ravel()))
    node_indices = {node: i for i, node in enumerate(all_nodes)}
    df['source_id'] = df['source'].map(node_indices)
    df['target_id'] = df['target'].map(node_indices)

    fig = go.Figure(data=[go.Sankey(
        valueformat=".2f", 
        textfont=dict(color="black", size=14),
        node=dict(
            pad=20,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=all_nodes,
            color="rgba(44, 123, 182, 0.8)"
        ),
        link=dict(
            source=df['source_id'],
            target=df['target_id'],
            value=df['value'],
            color=["#8dd3c7", "#8CD5AE", "#bebada", "#E1A0A0", "#DFC78C"]
        )
    )])

    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=50),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=320
    )
    return fig


def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

with open("indonesia-prov-clean.geojson", "r", encoding="utf-8") as f:
    indonesia_geojson = json.load(f)

df_edunocup = pd.read_excel("data.xlsx", sheet_name="edunocup")

df_sex = pd.read_excel("data.xlsx", sheet_name="sex")

# --- Buat HTML table dari df_edunocup ---
overview_html = df_sex.to_html(
    index=False,
    border=0,
    classes="striped highlight responsive-table"  # kelas2 Materialize
)

# --- Escape agar aman dimasukkan ke JS template literal ---
overview_csv = df_sex.to_csv(index=False)
overview_html = df_sex.head(60).to_html(index=False, border=0, classes="striped highlight responsive-table")
def _to_js_tpl_literal(s: str) -> str:
    return s.replace("\\", "\\\\").replace("`", "\\`")

overview_html_js = _to_js_tpl_literal(overview_html)

overview_csv_js = _to_js_tpl_literal(overview_csv)
csv_filename_sex = "Percentage of STEM University Graduates by Sex 2024.csv"



province_name_mapping = {
    "Aceh": "DI. ACEH",
    "Sumatera Utara": "SUMATERA UTARA",
    "Sumatera Barat": "SUMATERA BARAT",
    "Riau": "RIAU",
    "Jambi": "JAMBI",
    "Sumatera Selatan": "SUMATERA SELATAN",
    "Bengkulu": "BENGKULU",
    "Lampung": "LAMPUNG",
    "Bangka-Belitung": "BANGKA BELITUNG",
    "Kepulauan Riau": "KEPULAUAN RIAU",
    "DKI Jakarta": "DKI JAKARTA",
    "Jawa Barat": "JAWA BARAT",
    "Jawa Tengah": "JAWA TENGAH",
    "D I Yogyakarta": "DAERAH ISTIMEWA YOGYAKARTA",
    "Jawa Timur": "JAWA TIMUR",
    "Banten": "BANTEN",
    "Bali": "BALI",
    "Nusa Tenggara Barat": "NUSATENGGARA BARAT",
    "Nusa Tenggara Timur": "NUSA TENGGARA TIMUR",
    "Kalimantan Barat": "KALIMANTAN BARAT",
    "Kalimantan Tengah": "KALIMANTAN TENGAH",
    "Kalimantan Selatan": "KALIMANTAN SELATAN",
    "Kalimantan Timur": "KALIMANTAN TIMUR",
    "Kalimantan Utara": "KALIMANTAN UTARA",
    "Sulawesi Utara": "SULAWESI UTARA",
    "Sulawesi Tengah": "SULAWESI TENGAH",
    "Sulawesi Selatan": "SULAWESI SELATAN",
    "Sulawesi Tenggara": "SULAWESI TENGGARA",
    "Gorontalo": "GORONTALO",
    "Sulawesi Barat": "SULAWESI BARAT",
    "Maluku": "MALUKU",
    "Maluku Utara": "MALUKU UTARA",
    "Papua Barat": "PAPUA BARAT",
    "Papua": "PAPUA"
}

def make_choropleth(input_df, province_col, value_col, color_theme="blue"):
    df_plot = input_df.copy()
    df_plot[province_col] = df_plot[province_col].replace(province_name_mapping)
    df_plot = df_plot[df_plot[province_col] != "Indonesia"]
    choropleth = px.choropleth(
        df_plot,
        geojson=indonesia_geojson,
        locations=province_col,
        featureidkey="properties.Propinsi",
        color=value_col,
        color_continuous_scale=color_theme,
        range_color=(10, df_plot[value_col].max()),
        labels={value_col: ""},
    )
    choropleth.update_geos(fitbounds="locations", visible=False)
    choropleth.update_layout(
        template="plotly_white",
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(l=0, r=0, t=0, b=0),
        height=350
    )
    return choropleth

# --------------------- Konten normal (centered) ---------------------
# === SEGMENT 1: anchor yang 'membungkus' blok Streamlit berikutnya ===
st.markdown('<div id="wrap-s1"></div>', unsafe_allow_html=True)
st.markdown("""
<style>
/* Wrapper persis SETELAH anchor (kadang ada 1-2 level pembungkus) */
#wrap-s1 + div,
#wrap-s1 + div > div,
#wrap-s1 + div > div > div{
  max-width: 1200px !important;
  margin-left: auto !important;
  margin-right: auto !important;
  padding-left: 2rem !important;
  padding-right: 2rem !important;
}
@media (max-width: 600px){
  #wrap-s1 + div,
  #wrap-s1 + div > div,
  #wrap-s1 + div > div > div{
    padding-left: 1rem !important;
    padding-right: 1rem !important;
  }
}
</style>
""", unsafe_allow_html=True)
# === SEGMENT 1 (centered via spacer columns) ===
left_pad, mid, right_pad = st.columns([1, 10, 1], gap="small")

H_SEX = "— 𝗦𝗲𝘅 —"
H_REGION = "— 𝗥𝗲𝗴𝗶𝗼𝗻 —"

grouped_options = [
    "All",
    H_SEX, "Female", "Male",
    H_REGION, "Sumatera", "Jawa–Bali", "Kalimantan", "Sulawesi",
    "Nusa Tenggara, Maluku, Papua"
]

def _block_header_choice():
    v = st.session_state["filters_grouped"]
    if v in (H_SEX, H_REGION):
        # kembalikan ke All jika user mengklik header
        st.session_state["filters_grouped"] = "All"
with mid:
  st.markdown('<div class="title-text" style="text-align:center;">Distribution of STEM University Graduates by Employment Status, 2024</div>', unsafe_allow_html=True)
  choice = st.selectbox(
      "Filters",
      grouped_options,
      index=0, # default = All
      key="filters_grouped",
      on_change=_block_header_choice,
      help="Please choose value. Header 'Sex' dan 'Region' cannot be selected."
  )
  data_selected = dataset_map[choice]

  # Bangun fig baru
  fig_pipeline = make_sankey(data_selected)

  # Tampilkan chart
  st.plotly_chart(fig_pipeline, use_container_width=True, config={"displayModeBar": False})
# with mid:
#     col1, col2 = st.columns([3, 2], gap="large")
#     with col1:
#         st.markdown("""
#             <div class="title-text">STEM Pathways and Gender Gap</div>
#             <div class="paragraph-text">
#             Most STEM university graduates are absorbed into employment (79.39%), 
#             yet a striking mismatch persists as only 18.39% work in STEM-related jobs 
#             while the majority (61.00%) shift to non-STEM fields.<br><br>
#             Male graduates show higher employment rates (86.21%) and better alignment 
#             with STEM jobs (21.09%) compared to females, who face lower employment (73.56%), 
#             higher unemployment (25.62%), and weaker STEM job integration (16.09%).
#             </div>
#         """, unsafe_allow_html=True)

#     with col2:
#         choice = st.selectbox(
#             "Filters",
#             grouped_options,
#             index=0,                         # default = All
#             key="filters_grouped",
#             on_change=_block_header_choice,
#             help="Please choose value. Header 'Sex' dan 'Region' cannot be selected."
#         # )
#         fig_pipeline.update_layout(
#             margin=dict(l=0, r=0, t=0, b=50),
#             paper_bgcolor="rgba(0,0,0,0)",
#             plot_bgcolor="rgba(0,0,0,0)",
#             height=320  # opsional: sesuaikan selera
#         )
#         st.plotly_chart(fig_pipeline, use_container_width=True, config={"displayModeBar": False})




# --------------------- Segmen FULL-BLEED (hanya bagian ini) ---------------------
card_html = """
<html>
  <head>
    <meta charset="utf-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1"/>
    <!-- Materialize CSS & Icons -->
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css" rel="stylesheet">
    <script src="https://unpkg.com/@lottiefiles/dotlottie-wc@0.6.2/dist/dotlottie-wc.js" type="module"></script>

    <style>
      html, body { margin:0; padding:0; }

      .title-text {
        font-size:2rem; font-weight:800; font-family:'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        color:#fff; text-align:center; 
        margin-bottom: 20px;
      }

      /* GRID CARD */
      .cards-grid.container {
        display:grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 24px;
        max-width: 1200px;
        margin: 0 auto 36px;         /* beri jarak bawah dari hero/section berikutnya */
        transition: opacity .3s ease, transform .3s ease;
      }
      .cards-grid.is-hidden {
        opacity: 0;
        transform: translateY(6px);
        pointer-events: none;
      }

      .card-button {
        display:flex; flex-direction:column; align-items:center; justify-content:flex-start;
        width:100%;
        min-height: 260px;           /* ✅ Tinggi minimal agar label muat */
        border-radius:16px; background:#f0f0f0; color:inherit;
        box-shadow:0 4px 10px rgba(0,0,0,.15);
        cursor:pointer; transition:transform .2s, background .2s, color .2s, box-shadow .2s;
        border:none; text-align:center; padding:16px 14px; outline:0;
      }
      .card-button:hover { transform:translateY(-2px); }
      .card-button.active { background:#fde047; color:#111827; }

      .lottie { width:130px; height:130px; margin:6px auto 10px; flex:0 0 auto; }
      .label { margin-top:8px; font-size:15px; font-weight:700; line-height:1.25; }

      @media (max-width: 600px){
        .lottie{ width:100px; height:100px; }
        .label{ font-size:14px; }
        .card-button{ min-height: 220px; }
      }

      .detail-panel { max-width:1200px; margin: 12px auto 0; background:transparent; }
      .fadeable { transition: opacity .3s ease, transform .3s ease; }
      .fade-hidden { opacity: 0 !important; transform: translateY(6px); pointer-events: none; }

      .collapsible.popout > li { margin: 10px 0; border-radius: 12px; overflow: hidden; border: 1px solid #e5e7eb; }
      .collapsible-header {
        background:#ffffff; font-weight:700; color:#334155;
        display:flex; align-items:center; justify-content:space-between; gap:8px;
      }
      .collapsible-header .hdr-left{ display:flex; align-items:center; gap:8px; }
      .collapsible-header i.material-icons { color:#64748b; }
      .collapsible-body { background:#ffffff; color:#475569; font-size:.95rem; }
      .table-wrap{ max-height: 420px; overflow:auto; }
      .collapsible-body table { margin: 0; }
      .collapsible-body .responsive-table { width: 100%; }

      /* HERO (Materialize grid) */
      .hero-row{ margin: 12px auto 8px; }
      .hero-lottie{ width:100%; height:260px; }
      @media (max-width:600px){ .hero-lottie{ height:220px; } }

      .quote-block{
        border-left: 6px solid rgba(255,255,255,.95) !important;
        background: rgba(255,255,255,.10);
        color: #fff;
        padding: 16px 20px;
        margin: 0;
        border-radius: 10px;
      }

      /* CLOSE BAR */
      #close-bar { display:none; margin:12px auto 0; }
      #close-bar.show { display:block; }

      /* WAVE + BACKGROUND SAMBUNG */
      .wave-wrap { position: relative; width: 100%; overflow: hidden; }
      .wave-wrap svg { display: block; width: 100%; height: 120px; }
      .after-wave { background: #3498db; margin-top: -3%; padding: 40px 2vw 56px; }
    </style>
  </head>
  <body>
    <div class="wave-wrap">
    <svg viewBox="0 0 1000 200" preserveAspectRatio="none" style="width: 100%; height: 100%;">
        <path
        d="M0,200 L0.0,100.0 C 6.3,101.2 18.8,103.7 25.0,104.9 C 31.3,106.1 43.8,108.4 50.0,109.6 C 56.3,110.6 68.8,112.6 75.0,113.6 C 81.3,114.4 93.8,116.0 100.0,116.8 C 106.3,117.3 118.8,118.5 125.0,119.0 C 131.3,119.2 143.8,119.7 150.0,119.9 C 156.3,119.9 168.8,119.8 175.0,119.7 C 181.3,119.3 193.8,118.6 200.0,118.2 C 206.3,117.5 218.8,116.3 225.0,115.6 C 231.3,114.7 243.8,112.9 250.0,112.0 C 256.3,110.9 268.8,108.7 275.0,107.6 C 281.3,106.4 293.8,104.0 300.0,102.8 C 306.3,101.5 318.8,99.0 325.0,97.8 C 331.3,96.6 343.8,94.2 350.0,93.0 C 356.3,91.9 368.8,89.7 375.0,88.6 C 381.3,87.7 393.8,85.8 400.0,84.9 C 406.3,84.2 418.8,82.8 425.0,82.1 C 431.3,81.7 443.8,80.8 450.0,80.4 C 456.3,80.3 468.8,80.1 475.0,80.0 C 481.3,80.2 493.8,80.6 500.0,80.8 C 506.3,81.3 518.8,82.3 525.0,82.8 C 531.3,83.6 543.8,85.1 550.0,85.9 C 556.3,86.9 568.8,88.8 575.0,89.8 C 581.3,91.0 593.8,93.3 600.0,94.4 C 606.3,95.6 618.8,98.1 625.0,99.3 C 631.3,100.5 643.8,103.0 650.0,104.3 C 656.3,105.5 668.8,107.8 675.0,109.0 C 681.3,110.0 693.8,112.1 700.0,113.1 C 706.3,113.9 718.8,115.7 725.0,116.5 C 731.3,117.1 743.8,118.2 750.0,118.8 C 756.3,119.1 768.8,119.6 775.0,119.9 C 781.3,119.9 793.8,119.8 800.0,119.8 C 806.3,119.5 818.8,118.8 825.0,118.5 C 831.3,117.9 843.8,116.6 850.0,116.0 C 856.3,115.1 868.8,113.4 875.0,112.5 C 881.3,111.4 893.8,109.3 900.0,108.2 C 906.3,107.0 918.8,104.7 925.0,103.5 C 931.3,102.3 943.8,99.8 950.0,98.5 C 956.3,97.3 968.8,94.8 975.0,93.6 C 981.3,92.5 993.8,90.2 1000.0,89.1 C 1006.3,88.1 1018.8,86.3 1025.0,85.3 L1000.0,200.0 L0,200.0Z"
        fill="#3498db"
        >
            <animate
            attributeName="d"
            dur="9.0s"
            repeatCount="indefinite"
            values="M0,200 L0.0,100.0 C 6.3,101.2 18.8,103.7 25.0,104.9 C 31.3,106.1 43.8,108.4 50.0,109.6 C 56.3,110.6 68.8,112.6 75.0,113.6 C 81.3,114.4 93.8,116.0 100.0,116.8 C 106.3,117.3 118.8,118.5 125.0,119.0 C 131.3,119.2 143.8,119.7 150.0,119.9 C 156.3,119.9 168.8,119.8 175.0,119.7 C 181.3,119.3 193.8,118.6 200.0,118.2 C 206.3,117.5 218.8,116.3 225.0,115.6 C 231.3,114.7 243.8,112.9 250.0,112.0 C 256.3,110.9 268.8,108.7 275.0,107.6 C 281.3,106.4 293.8,104.0 300.0,102.8 C 306.3,101.5 318.8,99.0 325.0,97.8 C 331.3,96.6 343.8,94.2 350.0,93.0 C 356.3,91.9 368.8,89.7 375.0,88.6 C 381.3,87.7 393.8,85.8 400.0,84.9 C 406.3,84.2 418.8,82.8 425.0,82.1 C 431.3,81.7 443.8,80.8 450.0,80.4 C 456.3,80.3 468.8,80.1 475.0,80.0 C 481.3,80.2 493.8,80.6 500.0,80.8 C 506.3,81.3 518.8,82.3 525.0,82.8 C 531.3,83.6 543.8,85.1 550.0,85.9 C 556.3,86.9 568.8,88.8 575.0,89.8 C 581.3,91.0 593.8,93.3 600.0,94.4 C 606.3,95.6 618.8,98.1 625.0,99.3 C 631.3,100.5 643.8,103.0 650.0,104.3 C 656.3,105.5 668.8,107.8 675.0,109.0 C 681.3,110.0 693.8,112.1 700.0,113.1 C 706.3,113.9 718.8,115.7 725.0,116.5 C 731.3,117.1 743.8,118.2 750.0,118.8 C 756.3,119.1 768.8,119.6 775.0,119.9 C 781.3,119.9 793.8,119.8 800.0,119.8 C 806.3,119.5 818.8,118.8 825.0,118.5 C 831.3,117.9 843.8,116.6 850.0,116.0 C 856.3,115.1 868.8,113.4 875.0,112.5 C 881.3,111.4 893.8,109.3 900.0,108.2 C 906.3,107.0 918.8,104.7 925.0,103.5 C 931.3,102.3 943.8,99.8 950.0,98.5 C 956.3,97.3 968.8,94.8 975.0,93.6 C 981.3,92.5 993.8,90.2 1000.0,89.1 C 1006.3,88.1 1018.8,86.3 1025.0,85.3 L1000.0,200.0 L0,200.0Z;
        M0,200 L0.0,100.0 C 6.3,98.8 18.8,96.3 25.0,95.1 C 31.3,93.9 43.8,91.6 50.0,90.4 C 56.3,89.4 68.8,87.4 75.0,86.4 C 81.3,85.6 93.8,84.0 100.0,83.2 C 106.3,82.7 118.8,81.5 125.0,81.0 C 131.3,80.8 143.8,80.3 150.0,80.1 C 156.3,80.1 168.8,80.3 175.0,80.3 C 181.3,80.7 193.8,81.4 200.0,81.8 C 206.3,82.5 218.8,83.8 225.0,84.4 C 231.3,85.3 243.8,87.1 250.0,88.0 C 256.3,89.1 268.8,91.3 275.0,92.4 C 281.3,93.6 293.8,96.0 300.0,97.2 C 306.3,98.5 318.8,101.0 325.0,102.2 C 331.3,103.4 343.8,105.8 350.0,107.0 C 356.3,108.1 368.8,110.3 375.0,111.4 C 381.3,112.3 393.8,114.2 400.0,115.1 C 406.3,115.8 418.8,117.2 425.0,117.9 C 431.3,118.3 443.8,119.2 450.0,119.6 C 456.3,119.7 468.8,119.9 475.0,120.0 C 481.3,119.8 493.8,119.4 500.0,119.2 C 506.3,118.7 518.8,117.7 525.0,117.2 C 531.3,116.4 543.8,114.9 550.0,114.1 C 556.3,113.1 568.8,111.2 575.0,110.2 C 581.3,109.0 593.8,106.8 600.0,105.6 C 606.3,104.4 618.8,101.9 625.0,100.7 C 631.3,99.5 643.8,97.0 650.0,95.7 C 656.3,94.5 668.8,92.2 675.0,91.0 C 681.3,90.0 693.8,87.9 700.0,86.9 C 706.3,86.1 718.8,84.3 725.0,83.5 C 731.3,82.9 743.8,81.8 750.0,81.2 C 756.3,80.9 768.8,80.4 775.0,80.1 C 781.3,80.1 793.8,80.2 800.0,80.2 C 806.3,80.5 818.8,81.2 825.0,81.5 C 831.3,82.1 843.8,83.4 850.0,84.0 C 856.3,84.9 868.8,86.6 875.0,87.5 C 881.3,88.6 893.8,90.7 900.0,91.8 C 906.3,93.0 918.8,95.3 925.0,96.5 C 931.3,97.8 943.8,100.3 950.0,101.5 C 956.3,102.7 968.8,105.2 975.0,106.4 C 981.3,107.5 993.8,109.8 1000.0,110.9 C 1006.3,111.9 1018.8,113.8 1025.0,114.7 L1000.0,200.0 L0,200.0Z;
        M0,200 L0.0,100.0 C 6.3,101.2 18.8,103.7 25.0,104.9 C 31.3,106.1 43.8,108.4 50.0,109.6 C 56.3,110.6 68.8,112.6 75.0,113.6 C 81.3,114.4 93.8,116.0 100.0,116.8 C 106.3,117.3 118.8,118.5 125.0,119.0 C 131.3,119.2 143.8,119.7 150.0,119.9 C 156.3,119.9 168.8,119.8 175.0,119.7 C 181.3,119.3 193.8,118.6 200.0,118.2 C 206.3,117.5 218.8,116.3 225.0,115.6 C 231.3,114.7 243.8,112.9 250.0,112.0 C 256.3,110.9 268.8,108.7 275.0,107.6 C 281.3,106.4 293.8,104.0 300.0,102.8 C 306.3,101.5 318.8,99.0 325.0,97.8 C 331.3,96.6 343.8,94.2 350.0,93.0 C 356.3,91.9 368.8,89.7 375.0,88.6 C 381.3,87.7 393.8,85.8 400.0,84.9 C 406.3,84.2 418.8,82.8 425.0,82.1 C 431.3,81.7 443.8,80.8 450.0,80.4 C 456.3,80.3 468.8,80.1 475.0,80.0 C 481.3,80.2 493.8,80.6 500.0,80.8 C 506.3,81.3 518.8,82.3 525.0,82.8 C 531.3,83.6 543.8,85.1 550.0,85.9 C 556.3,86.9 568.8,88.8 575.0,89.8 C 581.3,91.0 593.8,93.3 600.0,94.4 C 606.3,95.6 618.8,98.1 625.0,99.3 C 631.3,100.5 643.8,103.0 650.0,104.3 C 656.3,105.5 668.8,107.8 675.0,109.0 C 681.3,110.0 693.8,112.1 700.0,113.1 C 706.3,113.9 718.8,115.7 725.0,116.5 C 731.3,117.1 743.8,118.2 750.0,118.8 C 756.3,119.1 768.8,119.6 775.0,119.9 C 781.3,119.9 793.8,119.8 800.0,119.8 C 806.3,119.5 818.8,118.8 825.0,118.5 C 831.3,117.9 843.8,116.6 850.0,116.0 C 856.3,115.1 868.8,113.4 875.0,112.5 C 881.3,111.4 893.8,109.3 900.0,108.2 C 906.3,107.0 918.8,104.7 925.0,103.5 C 931.3,102.3 943.8,99.8 950.0,98.5 C 956.3,97.3 968.8,94.8 975.0,93.6 C 981.3,92.5 993.8,90.2 1000.0,89.1 C 1006.3,88.1 1018.8,86.3 1025.0,85.3 L1000.0,200.0 L0,200.0Z"
            />
        </path>
    </svg>
    </div>

    <div class="after-wave">
      <div class="wrap" id="wrap">
        <div class="title-text">Topic</div>

        <!-- Grid card -->
        <div class="cards-grid container" id="cards-grid">
          <div class="card-button" role="button" tabindex="0" data-card="c1" data-label="STEM Pathways and Gender Gap">
            <dotlottie-wc class="lottie" src="https://lottie.host/51a834a6-c752-463e-9d4d-a5ce8a2868ec/GvLk1hszLK.json" speed="1" autoplay loop></dotlottie-wc>
            <div class="label">STEM Pathways and Gender Gap</div>
          </div>

          <div class="card-button" role="button" tabindex="0" data-card="c2" data-label="STEM Across Generations">
            <dotlottie-wc class="lottie" src="https://lottie.host/b2bb87b5-6a84-442a-9ee0-d4b29fae5f97/qw1cYx0jll.json" speed="1" autoplay loop></dotlottie-wc>
            <div class="label">STEM Across Generations</div>
          </div>

          <div class="card-button" role="button" tabindex="0" data-card="c3" data-label="Disability Representation in STEM Graduates">
            <dotlottie-wc class="lottie" src="https://lottie.host/b2bb87b5-6a84-442a-9ee0-d4b29fae5f97/qw1cYx0jll.json" speed="1" autoplay loop></dotlottie-wc>
            <div class="label">Disability Representation in STEM Graduates</div>
          </div>

          <div class="card-button" role="button" tabindex="0" data-card="c4" data-label="Education and Occupation">
            <dotlottie-wc class="lottie" src="https://lottie.host/b2bb87b5-6a84-442a-9ee0-d4b29fae5f97/qw1cYx0jll.json" speed="1" autoplay loop></dotlottie-wc>
            <div class="label">Education and Occupation</div>
          </div>
        </div>

        <!-- HERO + PANEL DETAIL -->
        <div id="detail-hero" class="fadeable fade-hidden"></div>

        <div class="detail-panel" style="margin-top:3%">
          <ul id="detail-collapsible" class="collapsible popout expandable fadeable fade-hidden"></ul>
          <div id="detail-quotes" class="fadeable fade-hidden"></div>

          <!-- CLOSE BAR -->
          <div id="close-bar" class="center-align">
            <a id="close-btn" class="btn red darken-1 waves-effect">
              <i class="material-icons left">close</i>Close
            </a>
          </div>
        </div>
      </div>
    </div>

    <!-- Materialize JS -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/js/materialize.min.js"></script>

    <script>
      (function(){
        const OVERVIEW_HTML = `__OVERVIEW_HTML__`;
        const CSV_DATA = `__CSV_DATA__`;
        const CSV_FILENAME = `__CSV_FILENAME__`;
        const CSV_URL = 'data:text/csv;charset=utf-8,' + encodeURIComponent(CSV_DATA);

        const WRAP = document.getElementById('wrap');
        const GRID = document.getElementById('cards-grid');
        const HERO = document.getElementById('detail-hero');
        const QUOTES = document.getElementById('detail-quotes');
        const LIST = document.getElementById('detail-collapsible');
        const CLOSE_BAR = document.getElementById('close-bar');
        const CLOSE_BTN = document.getElementById('close-btn');
        const cards = Array.from(document.querySelectorAll('.card-button'));
        let activeId = null;
        const singleSelect = true;

        const HERO_BY_CARD = {
          c1: `
            <div class="container">
              <div class="row hero-row">
                <div class="col s12 m5 l4 center-align">
                  <dotlottie-wc class="hero-lottie"
                    src="https://lottie.host/51a834a6-c752-463e-9d4d-a5ce8a2868ec/GvLk1hszLK.json"
                    autoplay loop speed="1"></dotlottie-wc>
                </div>
                <div class="col s12 m7 l8 white-text">
                  <blockquote class="quote-block white-text flow-text">
                    Most STEM university graduates are absorbed into employment (79.39%), yet a striking mismatch persists as only 18.39% work in STEM-related jobs while the majority (61.00%) shift to non-STEM fields. Male graduates show higher employment rates (86.21%) and better alignment with STEM jobs (21.09%) compared to females, who face lower employment (73.56%), higher unemployment (25.62%), and weaker STEM job integration (16.09%).
                  </blockquote>
                </div>
              </div>
            </div>`
        };

        const CARD_QUOTES = {
          c1:`<div style="background-color:#f0f0f0; padding:20px; border-radius:10px;
              box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
              font-size:18px; font-style:italic; color:#333;
              width:80%; margin:40px auto; text-align:center;">
              “Beyond the overall STEM talent underutilization, women experience a double disadvantage,
                highlighting the need for stronger industry-academia linkages and gender-inclusive policies
                to maximize STEM potential in the labor market.”
            </div>`
        };

        const DATA = {
          c1: [
            { t:"Percentage of STEM University Graduates by Sex, 2024 (Source: Sakernas, BPS)", raw:true, body: OVERVIEW_HTML, csv:true },
          ],
          c2: [
            { t:"Age Cohorts", body:"Perbandingan Gen Z, Milenial, dst."},
            { t:"Mobility", body:"Transisi pendidikan → pekerjaan lintas generasi."}
          ],
          c3: [
            { t:"Participation", body:"Tingkat partisipasi & hambatan."},
            { t:"Support", body:"Dukungan & akomodasi yang efektif."}
          ],
          c4: [
            { t:"Match Quality", body:"Kesesuaian jurusan–pekerjaan & wage premium."},
            { t:"Regional Gaps", body:"Perbedaan antardaerah & implikasi kebijakan."}
          ]
        };

        /* ==== Auto-resize iframe (lebih kuat) ==== */
        function setHeight(){
          try{
            const body = document.body;
            const h = Math.ceil(Math.max(
              body.scrollHeight, body.offsetHeight, body.clientHeight,
              WRAP ? WRAP.scrollHeight : 0
            ));
            if (window.frameElement) window.frameElement.style.height = (h + 1) + 'px';
          }catch(e){}
        }
        const ro1 = new ResizeObserver(setHeight);
        ro1.observe(document.body);
        if (WRAP) { const ro2 = new ResizeObserver(setHeight); ro2.observe(WRAP); }
        window.addEventListener('load', setHeight);
        document.addEventListener('DOMContentLoaded', setHeight);

        /* ==== Fade helpers ==== */
        function fadeOut(el, after){
          if(!el) return after && after();
          el.classList.add('fadeable', 'fade-hidden');
          el.style.opacity = '';
          setTimeout(() => { if (after) after(); setHeight(); }, 320);
        }
        function fadeIn(el){
          if(!el) return;
          el.classList.add('fadeable');
          el.classList.remove('fade-hidden');
          el.style.opacity = '';
          setTimeout(setHeight, 320);
        }

        /* ==== Collapsible builder ==== */
        function buildCollapsible(items){
          return items.map(it => `
            <li>
              <div class="collapsible-header">
                <div class="hdr-left"><i class="material-icons">expand_more</i>${it.t}</div>
                ${it.csv ? `
                  <a href="${CSV_URL}" download="${CSV_FILENAME}"
                     class="btn-flat waves-effect download-btn"
                     title="Download CSV" onclick="event.stopPropagation();">
                    <i class="material-icons">download</i>
                  </a>` : ``}
              </div>
              <div class="collapsible-body">
                ${it.raw ? `<div class="table-wrap">${it.body}</div>` : `<span>${it.body||""}</span>`}
              </div>
            </li>
          `).join('');
        }
        function initMaterialize(){
          const elems = document.querySelectorAll('.collapsible');
          M.Collapsible.init(elems, {
            accordion: false,
            onOpenEnd: () => requestAnimationFrame(setHeight),
            onCloseEnd: () => requestAnimationFrame(setHeight)
          });
          setHeight();
        }

        function clearActive(){
          cards.forEach(c => c.classList.remove('active'));
          activeId = null;
          LIST.innerHTML = "";
          HERO.innerHTML = "";
          CLOSE_BAR.classList.remove('show');
          GRID.style.display = "";
          requestAnimationFrame(() => {
            GRID.classList.remove('is-hidden');
            fadeOut(LIST); fadeOut(HERO);
            setHeight();
          });
        }

        function showPanel(id){
          HERO.innerHTML = HERO_BY_CARD[id] || "";
          LIST.innerHTML = buildCollapsible(DATA[id] || []);
          initMaterialize();
          QUOTES.innerHTML = CARD_QUOTES[id] || "";

          CLOSE_BAR.classList.add('show');
          fadeIn(HERO); fadeIn(LIST); fadeIn(QUOTES);
          LIST.scrollIntoView({behavior:'smooth', block:'nearest'});
        }

        function toggleCard(card){
          const id = card.getAttribute('data-card');
          if (singleSelect && activeId === id) { clearActive(); return; }
          cards.forEach(c => c.classList.remove('active'));
          card.classList.add('active');
          activeId = id;

          GRID.classList.add('is-hidden');
          setTimeout(function(){
            GRID.style.display = "none";
            showPanel(id);
          }, 320);
        }

        initMaterialize();
        cards.forEach(card => {
          card.addEventListener('click', () => toggleCard(card));
          card.addEventListener('keydown', e => {
            if(e.key === 'Enter' || e.key === ' '){ e.preventDefault(); toggleCard(card); }
          });
        });

        CLOSE_BTN.addEventListener('click', function(){
          CLOSE_BAR.classList.remove('show');
          fadeOut(LIST, function(){ LIST.innerHTML = ""; setHeight(); });
          fadeOut(QUOTES, function(){ QUOTES.innerHTML = ""; setHeight(); });
          fadeOut(HERO, function(){
            HERO.innerHTML = "";
            GRID.style.display = "";
            requestAnimationFrame(() => { GRID.classList.remove('is-hidden'); setHeight(); });
            activeId = null;
            cards.forEach(c => c.classList.remove('active'));
          });
        });
      })();
    </script>
  </body>
</html>
"""





# Segmen full-bleed: diletakkan tanpa wrapper .content-wrap
card_html = card_html.replace("__OVERVIEW_HTML__", overview_html_js)
card_html = card_html.replace("__CSV_DATA__", overview_csv_js)
card_html = card_html.replace("__CSV_FILENAME__", csv_filename_sex)

components.html(card_html, height=1100, scrolling=False)

