import streamlit as st
from streamlit_lottie import st_lottie
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit.components.v1 as components

# --------------------- Page & Global CSS ---------------------
st.set_page_config(
    page_title="STEM Employment Data Dashboard 2024",
    page_icon="🧪",
    layout="wide",
)
st.markdown("""
<style>
.stApp { background: #ffffff !important; color: #111 !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
:root { --content-max: 1200px; --content-pad: 2rem; }

/* 1) Hilangkan padding global supaya bisa buat segmen full-bleed */
.block-container{
  padding-left: 0 !important;
  padding-right: 0 !important;
  padding-bottom: 0 !important;
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
    ["University Graduates with a major in STEM fields", "Currently attending school and not engaged in any form of employment", 0.80],
    ["University Graduates with a major in STEM fields", "Engaged in any form of employment", 80.89],
    ["University Graduates with a major in STEM fields", "No longer attending school and not employed", 18.31],
    ["Engaged in any form of employment", "STEM Jobs", 27.77],
    ["Engaged in any form of employment", "Not in STEM Jobs", 53.12],
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


def _to_js_tpl_literal(s: str) -> str:
    return s.replace("\\", "\\\\").replace("`", "\\`")

## Sex Overview Table
df_sex = pd.read_excel("data.xlsx", sheet_name="sex")


overview_csv = df_sex.to_csv(index=False)
overview_html = df_sex.head(60).to_html(index=False, border=0, classes="striped highlight responsive-table")

overview_html_js = _to_js_tpl_literal(overview_html)

overview_csv_js = _to_js_tpl_literal(overview_csv)
csv_filename_sex = "Percentage of STEM University Graduates by Sex 2024.csv"



## Gen Overview Table
df_gen = pd.read_excel("data.xlsx", sheet_name="gen")

legend_html = """
<div class="rse-legend" style="margin-top:8px;font-size:.9rem;color:#6b7280">
  <span class="chip chip-yellow"></span> 25%≤RSE&lt;50%
  &nbsp;&nbsp;&nbsp;
  <span class="chip chip-red"></span> RSE≥50%
</div>
"""
overview_csv_gen = df_gen.to_csv(index=False, na_rep='NA')

overview_html_gen = df_gen.head(60).to_html(
    index=False,
    border=0,
    classes="striped highlight responsive-table",
    table_id="gen-table",
    na_rep='NA'
)

overview_html_gen += legend_html


overview_html_gen_js = _to_js_tpl_literal(overview_html_gen)

overview_csv_gen_js = _to_js_tpl_literal(overview_csv_gen)
csv_filename_gen = "Percentage of STEM University Graduates by Generation 2024.csv"




## Age Overview Table
df_age = pd.read_excel("data.xlsx", sheet_name="age")

legend_html = """
<div class="rse-legend" style="margin-top:8px;font-size:.9rem;color:#6b7280">
  <span class="chip chip-yellow"></span> 25%≤RSE&lt;50%
  &nbsp;&nbsp;&nbsp;
  <span class="chip chip-red"></span> RSE≥50%
</div>
"""
overview_csv_age = df_age.to_csv(index=False, na_rep='NA')

overview_html_age = df_age.head(60).to_html(
    index=False,
    border=0,
    classes="striped highlight responsive-table",
    table_id="age-table",
    na_rep='NA'  
)
overview_html_age += legend_html


overview_html_age_js = _to_js_tpl_literal(overview_html_age)

overview_csv_age_js = _to_js_tpl_literal(overview_csv_age)
csv_filename_age = "Percentage of STEM University Graduates by Age Group 2024.csv"


## Disability Overview Table
df_disability = pd.read_excel("data.xlsx", sheet_name="disability")

legend_html = """
<div class="rse-legend" style="margin-top:8px;font-size:.9rem;color:#6b7280">
  Note: The concept of disability includes mild difficulty, severe difficulty, and complete inability.
  &nbsp;&nbsp;&nbsp;
  <span class="chip chip-yellow"></span> 25%≤RSE&lt;50%
  &nbsp;&nbsp;&nbsp;
  <span class="chip chip-red"></span> RSE≥50%
</div>
"""
overview_csv_disability = df_disability.to_csv(index=False, na_rep='NA')

overview_html_disability = df_disability.head(60).to_html(
    index=False,
    border=0,
    classes="striped highlight responsive-table",
    table_id="disability-table",
    na_rep='NA'  
)
overview_html_disability += legend_html


overview_html_disability_js = _to_js_tpl_literal(overview_html_disability)

overview_csv_disability_js = _to_js_tpl_literal(overview_csv_disability)
csv_filename_disability = "PPercentage of STEM University Graduates by Disability Condition 2024.csv"


## Education and Occupaction Overview Table

df_edunocup = pd.read_excel("data.xlsx", sheet_name="edunocup")

overview_csv_edunocup = df_edunocup.to_csv(index=False, na_rep='NA')
overview_html_edunocup = df_edunocup.head(60).to_html(index=False, border=0, classes="striped highlight responsive-table",na_rep='NA')

overview_html_edunocup_js = _to_js_tpl_literal(overview_html_edunocup)

overview_csv_edunocup_js = _to_js_tpl_literal(overview_csv_edunocup)
csv_filename_edunocup = "University Graduates by Education and Occupation in STEM 2024.csv"


df_province_dist = pd.read_excel("data.xlsx", sheet_name="province_dist")

csv_prov = df_province_dist.to_csv(index=False, na_rep='NA')
csv_prov_js = _to_js_tpl_literal(csv_prov)  # escape backtick & slash biar aman di template literal JS
csv_prov_filename = "STEM_Graduates_Province_Distribution_2024.csv"




## ============= Choropleth Map =============
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


st.markdown("<style>.block-container{padding-top:0; padding-bottom:0}</style>", unsafe_allow_html=True)

components.html("""
<!DOCTYPE html>
<html lang="id">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />

  <!-- Materialize CSS & Icons -->
  <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
  <link href="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css" rel="stylesheet">

  <!-- Lottie -->
  <script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>

  <style>
    html, body { margin:0; padding:0; background:#ffffff; }  /* halaman setelah wave putih */
    .hero-blue { background:#2196f3; color:#fff; padding-top:5%; } /* biru cerah */
    .hero-pad { padding: 32px 0 16px; } /* ruang atas hero */
    .title-strong { font-weight:800; margin:0 0 50px 0; }
    .desc {margin-bottom:5%; font-size:1.1rem; line-height:1.6; }
    .quote-card {
      border-radius:16px;
      background: rgba(255,255,255,0.10);   /* semi-transparan di atas biru */
      border: 1px solid rgba(255,255,255,0.25);
      padding:16px 18px;
      color:#fff;
    }
    .quote-card i { color:#fff; margin-right:8px; }


    .wave-container {
      width:100%;
      height:200px;
      overflow:hidden;
      line-height:0;
      background:#2196f3; /* sama dengan hero agar menyatu */
    }
    .wave-container svg { width:100%; height:100%; display:block; }
  </style>
</head>
<body>


  <div class="hero-blue">
    <div class=" hero-pad">
      <div class="row valign-wrapper">
        <!-- Kiri: Teks -->
        <div class="col s12 m6 offset-m1">
          <h4 class="title-strong white-text">STEM EMPLOYMENT DATA DASHBOARD 2024</h4>

          <p class="flow-text desc white-text">
            The STEM Employment Data Dashboard presents a comprehensive view of how graduates transition from education
            to the workforce, covering employment status, job alignment, gender, generation, and regional patterns.
            It highlights mismatches and gaps to inform strategies for better utilization of STEM talent in Indonesia.
          </p>

          <!-- Highlight rounded dengan teks putih -->
          <div class="quote-card">
            <i class="material-icons left">format_quote</i>
            <span style="font-style:italic;">
              STEM employment data is more than numbers—it reveals how talent meets opportunity, where gaps persist, and how we can unlock the full potential of future innovators.
            </span>
          </div>
        </div>

        <!-- Kanan: Lottie -->
        <div class="col s12 m6 center-align offset-m1 hide-on-small-only">
          <lottie-player
            src="https://lottie.host/51a834a6-c752-463e-9d4d-a5ce8a2868ec/GvLk1hszLK.json"
            background="transparent"
            speed="1"
            style="width:100%;max-width:560px;height:520px"
            loop
            autoplay>
          </lottie-player>
        </div>
      </div>
    </div>
  </div>


<div class="wave-container">
  <svg viewBox="0 0 1000 200" preserveAspectRatio="none" style="width: 100%; height: 100%;">
    <path
      d="M0,200 L0.0,100.0 C 6.3,101.7 18.8,105.2 25.0,106.9 C 31.3,108.5 43.8,111.8 50.0,113.4 C 56.3,114.8 68.8,117.7 75.0,119.1 C 81.3,120.2 93.8,122.5 100.0,123.6 C 106.3,124.3 118.8,125.8 125.0,126.6 C 131.3,126.9 143.8,127.6 150.0,127.9 C 156.3,127.8 168.8,127.7 175.0,127.6 C 181.3,127.1 193.8,126.0 200.0,125.5 C 206.3,124.6 218.8,122.7 225.0,121.8 C 231.3,120.5 243.8,118.0 250.0,116.8 C 256.3,115.3 268.8,112.2 275.0,110.7 C 281.3,109.0 293.8,105.7 300.0,104.0 C 306.3,102.3 318.8,98.8 325.0,97.0 C 331.3,95.3 343.8,91.9 350.0,90.2 C 356.3,88.7 368.8,85.5 375.0,84.0 C 381.3,82.7 393.8,80.1 400.0,78.8 C 406.3,77.8 418.8,75.9 425.0,74.9 C 431.3,74.3 443.8,73.2 450.0,72.6 C 456.3,72.4 468.8,72.2 475.0,72.0 C 481.3,72.3 493.8,72.9 500.0,73.2 C 506.3,73.9 518.8,75.2 525.0,75.9 C 531.3,77.0 543.8,79.1 550.0,80.2 C 556.3,81.6 568.8,84.4 575.0,85.8 C 581.3,87.4 593.8,90.6 600.0,92.2 C 606.3,93.9 618.8,97.4 625.0,99.1 C 631.3,100.8 643.8,104.3 650.0,106.0 C 656.3,107.7 668.8,110.9 675.0,112.6 C 681.3,114.0 693.8,117.0 700.0,118.4 C 706.3,119.6 718.8,121.8 725.0,123.0 C 731.3,123.8 743.8,125.5 750.0,126.3 C 756.3,126.7 768.8,127.4 775.0,127.8 C 781.3,127.8 793.8,127.7 800.0,127.7 C 806.3,127.2 818.8,126.3 825.0,125.8 C 831.3,125.0 843.8,123.3 850.0,122.4 C 856.3,121.2 868.8,118.7 875.0,117.5 C 881.3,116.0 893.8,113.0 900.0,111.5 C 906.3,109.8 918.8,106.6 925.0,104.9 C 931.3,103.2 943.8,99.7 950.0,97.9 C 956.3,96.2 968.8,92.8 975.0,91.1 C 981.3,89.5 993.8,86.4 1000.0,84.8 C 1006.3,83.5 1018.8,80.8 1025.0,79.4 L1000.0,200.0 L0,200.0Z"
      fill="#ffffff"
      >
        <animate
          attributeName="d"
          dur="9.0s"
          repeatCount="indefinite"
          values="M0,200 L0.0,100.0 C 6.3,101.7 18.8,105.2 25.0,106.9 C 31.3,108.5 43.8,111.8 50.0,113.4 C 56.3,114.8 68.8,117.7 75.0,119.1 C 81.3,120.2 93.8,122.5 100.0,123.6 C 106.3,124.3 118.8,125.8 125.0,126.6 C 131.3,126.9 143.8,127.6 150.0,127.9 C 156.3,127.8 168.8,127.7 175.0,127.6 C 181.3,127.1 193.8,126.0 200.0,125.5 C 206.3,124.6 218.8,122.7 225.0,121.8 C 231.3,120.5 243.8,118.0 250.0,116.8 C 256.3,115.3 268.8,112.2 275.0,110.7 C 281.3,109.0 293.8,105.7 300.0,104.0 C 306.3,102.3 318.8,98.8 325.0,97.0 C 331.3,95.3 343.8,91.9 350.0,90.2 C 356.3,88.7 368.8,85.5 375.0,84.0 C 381.3,82.7 393.8,80.1 400.0,78.8 C 406.3,77.8 418.8,75.9 425.0,74.9 C 431.3,74.3 443.8,73.2 450.0,72.6 C 456.3,72.4 468.8,72.2 475.0,72.0 C 481.3,72.3 493.8,72.9 500.0,73.2 C 506.3,73.9 518.8,75.2 525.0,75.9 C 531.3,77.0 543.8,79.1 550.0,80.2 C 556.3,81.6 568.8,84.4 575.0,85.8 C 581.3,87.4 593.8,90.6 600.0,92.2 C 606.3,93.9 618.8,97.4 625.0,99.1 C 631.3,100.8 643.8,104.3 650.0,106.0 C 656.3,107.7 668.8,110.9 675.0,112.6 C 681.3,114.0 693.8,117.0 700.0,118.4 C 706.3,119.6 718.8,121.8 725.0,123.0 C 731.3,123.8 743.8,125.5 750.0,126.3 C 756.3,126.7 768.8,127.4 775.0,127.8 C 781.3,127.8 793.8,127.7 800.0,127.7 C 806.3,127.2 818.8,126.3 825.0,125.8 C 831.3,125.0 843.8,123.3 850.0,122.4 C 856.3,121.2 868.8,118.7 875.0,117.5 C 881.3,116.0 893.8,113.0 900.0,111.5 C 906.3,109.8 918.8,106.6 925.0,104.9 C 931.3,103.2 943.8,99.7 950.0,97.9 C 956.3,96.2 968.8,92.8 975.0,91.1 C 981.3,89.5 993.8,86.4 1000.0,84.8 C 1006.3,83.5 1018.8,80.8 1025.0,79.4 L1000.0,200.0 L0,200.0Z;
       M0,200 L0.0,100.0 C 6.3,98.3 18.8,94.8 25.0,93.1 C 31.3,91.5 43.8,88.2 50.0,86.6 C 56.3,85.2 68.8,82.3 75.0,80.9 C 81.3,79.8 93.8,77.5 100.0,76.4 C 106.3,75.7 118.8,74.2 125.0,73.4 C 131.3,73.1 143.8,72.4 150.0,72.1 C 156.3,72.2 168.8,72.3 175.0,72.4 C 181.3,72.9 193.8,74.0 200.0,74.5 C 206.3,75.4 218.8,77.3 225.0,78.2 C 231.3,79.5 243.8,82.0 250.0,83.2 C 256.3,84.7 268.8,87.8 275.0,89.3 C 281.3,91.0 293.8,94.3 300.0,96.0 C 306.3,97.8 318.8,101.3 325.0,103.0 C 331.3,104.7 343.8,108.1 350.0,109.8 C 356.3,111.3 368.8,114.5 375.0,116.0 C 381.3,117.3 393.8,119.9 400.0,121.2 C 406.3,122.2 418.8,124.1 425.0,125.1 C 431.3,125.7 443.8,126.8 450.0,127.4 C 456.3,127.6 468.8,127.8 475.0,128.0 C 481.3,127.7 493.8,127.1 500.0,126.8 C 506.3,126.1 518.8,124.8 525.0,124.1 C 531.3,123.0 543.8,120.9 550.0,119.8 C 556.3,118.4 568.8,115.6 575.0,114.2 C 581.3,112.6 593.8,109.4 600.0,107.8 C 606.3,106.1 618.8,102.6 625.0,100.9 C 631.3,99.2 643.8,95.7 650.0,94.0 C 656.3,92.3 668.8,89.1 675.0,87.4 C 681.3,86.0 693.8,83.0 700.0,81.6 C 706.3,80.4 718.8,78.2 725.0,77.0 C 731.3,76.2 743.8,74.5 750.0,73.7 C 756.3,73.3 768.8,72.6 775.0,72.2 C 781.3,72.2 793.8,72.3 800.0,72.3 C 806.3,72.8 818.8,73.7 825.0,74.2 C 831.3,75.0 843.8,76.8 850.0,77.6 C 856.3,78.8 868.8,81.3 875.0,82.5 C 881.3,84.0 893.8,87.0 900.0,88.5 C 906.3,90.2 918.8,93.4 925.0,95.1 C 931.3,96.8 943.8,100.3 950.0,102.1 C 956.3,103.8 968.8,107.2 975.0,108.9 C 981.3,110.5 993.8,113.6 1000.0,115.2 C 1006.3,116.5 1018.8,119.3 1025.0,120.6 L1000.0,200.0 L0,200.0Z;
       M0,200 L0.0,100.0 C 6.3,101.7 18.8,105.2 25.0,106.9 C 31.3,108.5 43.8,111.8 50.0,113.4 C 56.3,114.8 68.8,117.7 75.0,119.1 C 81.3,120.2 93.8,122.5 100.0,123.6 C 106.3,124.3 118.8,125.8 125.0,126.6 C 131.3,126.9 143.8,127.6 150.0,127.9 C 156.3,127.8 168.8,127.7 175.0,127.6 C 181.3,127.1 193.8,126.0 200.0,125.5 C 206.3,124.6 218.8,122.7 225.0,121.8 C 231.3,120.5 243.8,118.0 250.0,116.8 C 256.3,115.3 268.8,112.2 275.0,110.7 C 281.3,109.0 293.8,105.7 300.0,104.0 C 306.3,102.3 318.8,98.8 325.0,97.0 C 331.3,95.3 343.8,91.9 350.0,90.2 C 356.3,88.7 368.8,85.5 375.0,84.0 C 381.3,82.7 393.8,80.1 400.0,78.8 C 406.3,77.8 418.8,75.9 425.0,74.9 C 431.3,74.3 443.8,73.2 450.0,72.6 C 456.3,72.4 468.8,72.2 475.0,72.0 C 481.3,72.3 493.8,72.9 500.0,73.2 C 506.3,73.9 518.8,75.2 525.0,75.9 C 531.3,77.0 543.8,79.1 550.0,80.2 C 556.3,81.6 568.8,84.4 575.0,85.8 C 581.3,87.4 593.8,90.6 600.0,92.2 C 606.3,93.9 618.8,97.4 625.0,99.1 C 631.3,100.8 643.8,104.3 650.0,106.0 C 656.3,107.7 668.8,110.9 675.0,112.6 C 681.3,114.0 693.8,117.0 700.0,118.4 C 706.3,119.6 718.8,121.8 725.0,123.0 C 731.3,123.8 743.8,125.5 750.0,126.3 C 756.3,126.7 768.8,127.4 775.0,127.8 C 781.3,127.8 793.8,127.7 800.0,127.7 C 806.3,127.2 818.8,126.3 825.0,125.8 C 831.3,125.0 843.8,123.3 850.0,122.4 C 856.3,121.2 868.8,118.7 875.0,117.5 C 881.3,116.0 893.8,113.0 900.0,111.5 C 906.3,109.8 918.8,106.6 925.0,104.9 C 931.3,103.2 943.8,99.7 950.0,97.9 C 956.3,96.2 968.8,92.8 975.0,91.1 C 981.3,89.5 993.8,86.4 1000.0,84.8 C 1006.3,83.5 1018.8,80.8 1025.0,79.4 L1000.0,200.0 L0,200.0Z"
        />
      </path>
  </svg>
</div>

  <!-- Setelah wave: putih (default body) -->
  <div class="section white">
    <div class="container">
      <!-- Konten lanjutan Anda di sini -->
      <!-- <h5 class="black-text">Section berikutnya</h5> -->
    </div>
  </div>

  <!-- Materialize JS (opsional untuk komponen interaktif) -->
  <script src="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/js/materialize.min.js"></script>
</body>
</html>
""", height=800, scrolling=False)

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


      .cards-grid.container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 24px;
        max-width: 1200px;
        margin: 0 auto 36px;
      }

      @media (min-width: 600px) and (max-width: 1375px) {
        .cards-grid.container {
          grid-template-columns: repeat(3, 1fr); /* paksa 3 kolom */
        }

        .cards-grid.container .card-button:nth-child(4) {
          grid-column: 2;
        }
      }

      .cards-grid.is-hidden {
        opacity: 0;
        transform: translateY(6px);
        pointer-events: none;
      }

      .card-button {
        display:flex; flex-direction:column; align-items:center; justify-content:flex-start;
        width:100%;
        min-height: 260px;          
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


      #close-bar { display:none; margin:12px auto 0; }
      #close-bar.show { display:block; }

      .blue-text { color:#3498db !important; }
      .gray-text { color:#6b7280 !important; }

      .rse-yellow{ background:#fff3bf !important; }  /* kuning lembut */
      .rse-red{    background:#ffc9c9 !important; }  /* merah lembut */


      .rse-legend .chip{
        display:inline-block; width:12px; height:12px;
        border-radius:2px; vertical-align:middle; margin:0 6px 0 0;
        border:1px solid rgba(0,0,0,.15);
      }
      .rse-legend .chip-yellow{ background:#fff3bf; border-color:#f2c94c; }
      .rse-legend .chip-red{    background:#ffc9c9; border-color:#ef4444; }
      .collapsible-body table.responsive-table tbody tr:last-child td,
      .collapsible-body table.responsive-table tbody tr:last-child th{
        font-weight: 700 !important;
      }


      ul.select-dropdown li:not(.optgroup):not(.disabled) > span {
        color: #3498db !important;
        cursor: pointer;
      }

      ul.select-dropdown li.optgroup > span {
        color: #6b7280 !important;
        font-weight: 700;
      }

      ul.select-dropdown li:not(.optgroup):hover {
        background-color: rgba(52,152,219,.08) !important;
      }
      ul.select-dropdown li.selected:not(.optgroup) {
        background-color: rgba(52,152,219,.12) !important;
      }

      ul.select-dropdown li.optgroup:hover {
        background-color: transparent !important;
      }


      @media (min-width: 992px){
        .table-wrap{
          max-height: 420px;     
          overflow: auto;        
          position: relative;
        }
        .table-wrap table{
          border-collapse: separate;
          border-spacing: 0;
        }
        .table-wrap thead th,
        .table-wrap thead td{
          position: sticky;
          position: -webkit-sticky; /* Safari */
          top: 0;
          z-index: 3;
          background: #ffffff;
          box-shadow: 0 1px 0 rgba(0,0,0,.06);
        }

        .table-wrap tbody th:first-child,
        .table-wrap tbody td:first-child{
          position: sticky;
          left: 0;
          z-index: 2;
          background: #ffffff;
          box-shadow: 1px 0 0 rgba(0,0,0,.06);
        }
        .table-wrap thead th:first-child{ left: 0; z-index: 4; }

        /* Pastikan responsive-table kembali ke layout tabel biasa di desktop */
        table.responsive-table thead{ display: table-header-group !important; }
        table.responsive-table tbody tr{ display: table-row !important; }
        table.responsive-table td,
        table.responsive-table th{ display: table-cell !important; }
      }

      @media (max-width: 991.98px){
        .table-wrap{
          max-height: none;
          overflow: visible;
        }
      }

      .map-wrap { position: relative; }
      .map-download {
        position: absolute;
        top: 10px; right: 10px;
        z-index: 12;                
        background: #2196f3;        
      }
      @media (max-width: 600px){
        .map-download { top: 8px; right: 8px; }
      }


      .content-wrap .title-row{
        display:flex;
        justify-content:center;
      }
      .content-wrap .title-row .title-text{
        display:flex;
        align-items:baseline;
        justify-content:center;
        gap:.35em;                
        text-align:center;         
      }


      .content-wrap .title-row .btn-flat.download-btn{
        font-size:1em !important;  
        height:auto; line-height:1; min-height:0; padding:0 .15em;
      }
      .content-wrap .title-row .btn-flat.download-btn i.material-icons{
        font-size:1em !important;
        transform:translateY(.07em);
      }

      @media (max-width: 900px){
        .content-wrap .title-row .title-text{
          flex-direction: column;
          align-items: center;
          gap: .25em;
        }
        #prov-csv-btn{ margin-top: .25rem; }
      }



      .content-wrap .title-row .download-btn{
        color: #3498db !important; 
      }
      .content-wrap .title-row .download-btn i.material-icons{
        color: inherit !important;
      }

      .content-wrap .title-row .download-btn:hover{
        background-color: rgba(158,158,158,.12) !important;
      }
      .content-wrap .title-row .download-btn:focus-visible{
        outline: 2px solid #3498db; outline-offset: 2px;
      }

      .waves-effect .waves-ripple{
        background-color: rgba(158,158,158,.35) !important;
      }

      

      #sankey-panel .sankey-controls{
        display: flex;
        align-items: flex-end;
        gap: 12px;
        flex-wrap: wrap;


      #sankey-filter-wrap{
        flex: 1 1 460px;
        min-width: 320px;
        margin: 0; 
      }


      #sankey-panel .select-wrapper,
      #sankey-panel input.select-dropdown{
        width: 100%;
      }


      #sankey-download{
        flex: 0 0 auto;
        margin: 0 0 6px 0;
      }


      .dropdown-content.select-dropdown{
        min-width: 420px;
      }


      @media (max-width: 600px){
        #sankey-filter-wrap{ flex: 1 1 100%; min-width: 0; }
        #sankey-download{ width: 100%; margin: 6px 0 0 0; }
      }


    </style>
  </head>
  <body>

    <div class="after-wave">
      <div class="wrap" id="wrap">

        <!-- Grid card -->
        <div class="title-text blue-text" id="topic-title">Topic</div>

        <div class="cards-grid container" id="cards-grid">

          <div class="card-button" role="button" tabindex="0" data-card="c1" data-label="STEM Pathways and Gender Gap">
            <dotlottie-wc class="lottie" src="https://lottie.host/7a38af72-125a-45bf-8d64-9fff33ae1a46/8xicPjFxDT.json" speed="1" autoplay loop></dotlottie-wc>
            <div class="label">STEM Pathways and Gender Gap</div>
          </div>

          <div class="card-button" role="button" tabindex="0" data-card="c2" data-label="STEM Across Generations">
            <dotlottie-wc class="lottie" src="https://lottie.host/aaa296d4-a366-4b66-ad09-a65876a5c693/o2R9oQMkNI.json" speed="1" autoplay loop></dotlottie-wc>
            <div class="label">STEM Across Generations</div>
          </div>

          <div class="card-button" role="button" tabindex="0" data-card="c3" data-label="Disability Representation in STEM Graduates">
            <dotlottie-wc class="lottie" src="https://lottie.host/db326799-1c61-45b9-855d-9360ed98dad7/vJkWU0LUHX.json" speed="1" autoplay loop></dotlottie-wc>
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
        <div class="content-wrap" style="margin-top:10%; margin-bottom:10%;">
          <div class="title-row">
            <div class="title-text blue-text" id="topic-title">
              Map of Percentage of STEM University Graduates 2024
              <a id="prov-csv-btn"
                class="btn-flat waves-effect download-btn"
                title="Download CSV" aria-label="Download Province CSV">
                <i class="material-icons">file_download</i>
              </a>
            </div>
          </div>



          <div class="map-wrap">
            <div id="choropleth" style="width:100%;height:500px;"></div>
          </div>

          <div style="background-color:#f0f0f0; padding:20px; border-radius:10px;
              box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
              font-size:18px; font-style:italic; color:#333;
              width:80%; margin:40px auto; text-align:center;">
              “In 2024, the distribution of STEM graduates in Indonesia shows that the largest shares are concentrated in provinces like <b> Jawa Barat (16.74%) </b> and <b>Jawa Timur (12.92%)</b>, reflecting the dominance of Java as the country’s STEM hub. Male and female shares are relatively balanced with provincial differences.”
          </div>
        </div>

      </div>
    </div>

    <!-- Materialize JS -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/js/materialize.min.js"></script>
    <script src="https://cdn.plot.ly/plotly-2.30.0.min.js"></script>
    <script>
      (function(){
        const OVERVIEW_HTML = `__OVERVIEW_HTML__`;
        const CSV_DATA = `__CSV_DATA__`;
        const CSV_FILENAME = `__CSV_FILENAME__`;

        const OVERVIEW_GEN_HTML = `__OVERVIEW_GEN_HTML__`;
        const CSV_GEN_DATA = `__CSV_GEN_DATA__`;
        const CSV_GEN_FILENAME = `__CSV_GEN_FILENAME__`;

        const OVERVIEW_AGE_HTML = `__OVERVIEW_AGE_HTML__`;
        const CSV_AGE_DATA = `__CSV_AGE_DATA__`;
        const CSV_AGE_FILENAME = `__CSV_AGE_FILENAME__`;


        const OVERVIEW_DISABILITY_HTML = `__OVERVIEW_DISABILITY_HTML__`;
        const CSV_DISABILITY_DATA = `__CSV_DISABILITY_DATA__`;
        const CSV_DISABILITY_FILENAME = `__CSV_DISABILITY_FILENAME__`;

        const OVERVIEW_EDUNOCUP_HTML = `__OVERVIEW_EDUNOCUP_HTML__`;
        const CSV_EDUNOCUP_DATA = `__CSV_EDUNOCUP_DATA__`;
        const CSV_EDUNOCUP_FILENAME = `__CSV_EDUNOCUP_FILENAME__`;

        
        const CSV_PROV_DATA = `__CSV_PROV_DATA__`;
        const CSV_PROV_FILENAME = `__CSV_PROV_FILENAME__`;
        const CSV_PROV_URL = 'data:text/csv;charset=utf-8,' + encodeURIComponent(CSV_PROV_DATA);


        const CSV_URL = 'data:text/csv;charset=utf-8,' + encodeURIComponent(CSV_DATA);
        const CSV_GEN_URL = 'data:text/csv;charset=utf-8,' + encodeURIComponent(CSV_GEN_DATA);
        const CSV_AGE_URL = 'data:text/csv;charset=utf-8,' + encodeURIComponent(CSV_AGE_DATA);
        const CSV_DISABILITY_URL = 'data:text/csv;charset=utf-8,' + encodeURIComponent(CSV_DISABILITY_DATA);
        const CSV_EDUNOCUP_URL = 'data:text/csv;charset=utf-8,' + encodeURIComponent(CSV_EDUNOCUP_DATA);


        const WRAP = document.getElementById('wrap');
        const GRID = document.getElementById('cards-grid');
        const HERO = document.getElementById('detail-hero');
        const QUOTES = document.getElementById('detail-quotes');
        const LIST = document.getElementById('detail-collapsible');
        const CLOSE_BAR = document.getElementById('close-bar');
        const CLOSE_BTN = document.getElementById('close-btn');
        const cards = Array.from(document.querySelectorAll('.card-button'));
        const TITLE = document.getElementById('topic-title');
        let activeId = null;
        const singleSelect = true;

        const HERO_BY_CARD = {
          c1: `
            <div class="container">
              <div class="row hero-row">
                <div class="col s12 m5 l4 center-align">
                  <dotlottie-wc class="hero-lottie"
                    src="https://lottie.host/7a38af72-125a-45bf-8d64-9fff33ae1a46/8xicPjFxDT.json"
                    autoplay loop speed="1"></dotlottie-wc>
                </div>
                <div class="col s12 m7 l8">
                  <blockquote class="quote-block gray-text flow-text">
                    Most STEM university graduates are absorbed into employment (80.89%), yet a striking mismatch persists as only 27.77% work in STEM-related jobs while the majority (53.12%) shift to non-STEM fields. Male graduates show higher employment rates (87.11%) and lower alignment with STEM jobs (25.17%) compared to females, who face lower employment (74.67%), but better STEM job integration (30.36%). 
                  </blockquote>
                </div>
              </div>
            </div>`,
          c2: `<div class="container">
              <div class="row hero-row">
                <div class="col s12 m5 l4 center-align">
                  <dotlottie-wc class="hero-lottie"
                    src="https://lottie.host/aaa296d4-a366-4b66-ad09-a65876a5c693/o2R9oQMkNI.json"
                    autoplay loop speed="1"></dotlottie-wc>
                </div>
                <div class="col s12 m7 l8">
                  <blockquote class="quote-block gray-text flow-text">
                    Indonesia’s STEM graduates show a workforce in transition, with Millennials still the largest group (52.98%), followed by Gen Z (21.79%), Gen X (19.30%), and a smaller share of Baby Boomers (5.93%). Millennials dominate across all provinces, though the share of Gen Z ranges from around 18% to 27%. 
                  </blockquote>
                </div>
              </div>
            </div>`,
            c3: `<div class="container">
              <div class="row hero-row">
                <div class="col s12 m5 l4 center-align">
                  <dotlottie-wc class="hero-lottie"
                    src="https://lottie.host/db326799-1c61-45b9-855d-9360ed98dad7/vJkWU0LUHX.json"
                    autoplay loop speed="1"></dotlottie-wc>
                </div>
                <div class="col s12 m7 l8">
                  <blockquote class="quote-block gray-text flow-text">
                    Persons with disabilities accounted for just 3.22% of STEM university graduates in Indonesia, showing that their presence in the field is still limited. While most provinces mirror this national pattern, higher proportions are seen in Gorontalo (4.98%), DKI Jakarta (4.81%), and Banten (4.63%), suggesting stronger visibility or inclusion efforts, whereas Bengkulu (0.77%) and Kepulauan Riau (0.93%) record the lowest shares. 
                  </blockquote>
                </div>
              </div>
            </div>`,
            c4: `<div class="container">
              <div class="row hero-row">
                <div class="col s12 m5 l4 center-align">
                  <dotlottie-wc class="hero-lottie"
                    src="https://lottie.host/b2bb87b5-6a84-442a-9ee0-d4b29fae5f97/qw1cYx0jll.json"
                    autoplay loop speed="1"></dotlottie-wc>
                </div>
                <div class="col s12 m7 l8">
                  <blockquote class="quote-block gray-text flow-text">
                    Nationally, only 11.46% of graduates are employed in STEM jobs aligned with their education, while a much larger proportion (21.94%) shift into non-STEM roles. Nearly one in four graduates experience a job–education misalignment, underscoring the gap between academic training and labor market absorption. 
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
              “STEM graduates often face job mismatch, as men find work more easily outside the field while women encounter higher barriers but greater alignment within STEM.”
            </div>`,
          c2:`<div style="background-color:#f0f0f0; padding:20px; border-radius:10px;
              box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
              font-size:18px; font-style:italic; color:#333;
              width:80%; margin:40px auto; text-align:center;">
              “Millennials dominate Indonesia’s STEM graduates, while Gen Z is emerging, underscoring the need to integrate new talent while drawing on older generations’ expertise.”
            </div>`,
          c3:`<div style="background-color:#f0f0f0; padding:20px; border-radius:10px;
              box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
              font-size:18px; font-style:italic; color:#333;
              width:80%; margin:40px auto; text-align:center;">
              “The uneven regional representation of STEM graduates with disabilities highlights the need to strengthen inclusive education and improve accessibility to expand opportunities across Indonesia.”
            </div>`,
          c4:`<div style="background-color:#f0f0f0; padding:20px; border-radius:10px;
              box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
              font-size:18px; font-style:italic; color:#333;
              width:80%; margin:40px auto; text-align:center;">
              “This pattern suggests persistent underutilization of STEM talent and structural mismatches between higher education output and labor market absorption.”
            </div>`
        };

        const DATA = {
          c1: [
            { t:"Percentage of STEM University Graduates by Sex, 2024 (Source: Sakernas, BPS)", raw:true, body: OVERVIEW_HTML, csv:true },
            { 
              t:"Graph — Distribution of STEM University Graduates by Employment Status, 2024",
              raw:true, nowrap:true, 
              body: `
                <div id="sankey-panel">
                  <div class="sankey-controls">
                    <div class="input-field" id="sankey-filter-wrap">
                      <select id="sankey-filter">
                        <option value="All" selected>All</option>
                        <optgroup label="— Sex —">
                          <option value="Female">Female</option>
                          <option value="Male">Male</option>
                        </optgroup>
                        <optgroup label="— Region —">
                          <option value="Sumatera">Sumatera</option>
                          <option value="Jawa–Bali">Jawa–Bali</option>
                          <option value="Kalimantan">Kalimantan</option>
                          <option value="Sulawesi">Sulawesi</option>
                          <option value="Nusa Tenggara, Maluku, Papua">Nusa Tenggara, Maluku, Papua</option>
                        </optgroup>
                      </select>
                      <label for="sankey-filter">Filters</label>
                    </div>

                    <!-- tombol biru -->
                    <a id="sankey-download"
                      class="btn btn-small blue waves-effect"
                      title="Download Image (PNG). Alt-click untuk JPG"
                      aria-label="Download Sankey PNG">
                      Download Image
                    </a>
                  </div>

                  <div id="sankey-chart" style="width:100%;height:420px; margin-top:5%;"></div>
                </div>

              `
            }
          ],
          c2: [
            { t:"Percentage of STEM University Graduates by Generation, 2024 (Source: Sakernas, BPS)", raw:true, body: OVERVIEW_GEN_HTML, csvGen:true },
            { t:"Percentage of STEM University Graduates by Age Group, 2024 (Source: Sakernas, BPS)", raw:true, body: OVERVIEW_AGE_HTML, csvAge:true }
          ],
          c3: [
            { t:"Percentage of STEM University Graduates by Disability Condition, 2024 (Source: Sakernas, BPS)", raw:true, body: OVERVIEW_DISABILITY_HTML, csvDisability:true },
          ],
          c4: [
            { t:"University Graduates by Education and Occupation in STEM, 2024 (Source: Sakernas, BPS)", raw:true, body: OVERVIEW_EDUNOCUP_HTML, csvEdunocup:true },
          ]
        };

        /* ==== Auto-resize iframe (lebih kuat) ==== */
        const ROOT = document.getElementById('wrap') || document.body;

        function setHeight(){
          const h = Math.ceil(
            Math.max(
              ROOT.scrollHeight,
              ROOT.offsetHeight,
              ROOT.getBoundingClientRect().height
            )
          ) + 4;

          if (window.Streamlit && window.Streamlit.setFrameHeight) {
            window.Streamlit.setFrameHeight(h);
          } else if (window.parent && window.parent.postMessage) {
            window.parent.postMessage({ type: "streamlit:setFrameHeight", height: h }, "*");
          }
          if (window.frameElement) window.frameElement.style.height = h + "px";
        }

        // Kick awal agresif (cegah “kalah start” sama iframe peta)
        let n = 0;
        const iv = setInterval(() => { setHeight(); if (++n > 20) clearInterval(iv); }, 80);

        // Resize saat ukuran ROOT berubah
        new ResizeObserver(setHeight).observe(ROOT);

        // Pantau perubahan DOM (buka/tutup collapsible, ganti konten, dll)
        new MutationObserver(setHeight).observe(ROOT, {
          childList: true, subtree: true, attributes: true
        });

        window.addEventListener("load", setHeight);
        document.fonts && document.fonts.ready && document.fonts.ready.then(setHeight);
        setTimeout(setHeight, 400);
        setTimeout(setHeight, 1200);

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
          return items.map(it => {
            // Kumpulkan semua tombol yang perlu ditampilkan
            const btns = [];
            if (it.csv) {
              btns.push(`
                <a href="${CSV_URL}" download="${CSV_FILENAME}"
                  class="btn-flat waves-effect download-btn"
                  title="Download CSV" onclick="event.stopPropagation();">
                  <i class="material-icons">download</i>
                </a>`);
            }
            if (it.csvGen) {
              btns.push(`
                <a href="${CSV_GEN_URL}" download="${CSV_GEN_FILENAME}"
                  class="btn-flat waves-effect download-btn"
                  title="Download CSV" onclick="event.stopPropagation();">
                  <i class="material-icons">download</i>
                </a>`);
            }
            if (it.csvAge) {
              btns.push(`
                <a href="${CSV_AGE_URL}" download="${CSV_AGE_FILENAME}"
                  class="btn-flat waves-effect download-btn"
                  title="Download CSV" onclick="event.stopPropagation();">
                  <i class="material-icons">download</i>
                </a>`);
            }
            if (it.csvDisability) {
              btns.push(`
                <a href="${CSV_DISABILITY_URL}" download="${CSV_DISABILITY_FILENAME}"
                  class="btn-flat waves-effect download-btn"
                  title="Download CSV" onclick="event.stopPropagation();">
                  <i class="material-icons">download</i>
                </a>`);
            }
            if (it.csvEdunocup) {
              btns.push(`
                <a href="${CSV_EDUNOCUP_URL}" download="${CSV_EDUNOCUP_FILENAME}"
                  class="btn-flat waves-effect download-btn"
                  title="Download CSV" onclick="event.stopPropagation();">
                  <i class="material-icons">download</i>
                </a>`);
            }
            const downloads = btns.join('');

            const bodyHtml = it.raw
              ? (it.nowrap ? it.body : `<div class="table-wrap">${it.body}</div>`)
              : `<span>${it.body || ""}</span>`;

            return `
              <li>
                <div class="collapsible-header">
                  <div class="hdr-left"><i class="material-icons">expand_more</i>${it.t}</div>
                  ${downloads}
                </div>
                <div class="collapsible-body">
                  ${bodyHtml}
                </div>
              </li>`;
          }).join('');
        }



          function decorateTableByHeader({
            tableId,
            headers = [],            
            provinceCol = 0,         
            yellow = [],             
            red = [],                
            yellowClass = 'rse-yellow',
            redClass = 'rse-red',
            exact = false,           
            caseSensitive = false,   
            boldLastRow = false,     
            debug = false
          }) {
            const t = document.getElementById(tableId);
            if (!t) { if (debug) console.warn('Table not found:', tableId); return; }


            const normalize = s => s.replace(/\s+/g, ' ').trim();
            const norm = s => caseSensitive ? normalize(s) : normalize(s).toLowerCase();


            const headRow = t.tHead ? t.tHead.rows[0] : t.rows[0];
            if (!headRow) { if (debug) console.warn('No header row in table:', tableId); return; }
            const headCells = Array.from(headRow.cells);


            let headerIdxs = [];
            if (exact) {
              const headerSet = new Set(headers.map(norm));
              headerIdxs = headCells.reduce((acc, th, idx) => {
                const txt = norm(th.textContent);
                if (headerSet.has(txt)) acc.push(idx);
                return acc;
              }, []);
            } else {
              const headersNorm = headers.map(norm);
              headerIdxs = headCells.reduce((acc, th, idx) => {
                const txt = norm(th.textContent);
                if (headersNorm.some(h => txt.includes(h))) acc.push(idx);
                return acc;
              }, []);
            }

            if (debug) console.log({ tableId, headers, exact, caseSensitive, headerIdxs });

            if (!headerIdxs.length) { if (debug) console.warn('Target headers not found:', headers); return; }

            const yellowSet = new Set(yellow);
            const redSet = new Set(red);

            const body = t.tBodies[0] || t;
            for (const r of Array.from(body.rows)) {
              const provCell = r.cells[provinceCol];
              if (!provCell) continue;
              const prov = normalize(provCell.textContent);

              for (const idx of headerIdxs) {
                const cell = r.cells[idx];
                if (!cell) continue;
                if (yellowSet.has(prov)) cell.classList.add(yellowClass);
                if (redSet.has(prov))    cell.classList.add(redClass);
              }
            }

            if (boldLastRow) {
              const rows = Array.from(body.rows);
              const last = rows[rows.length - 1];
              if (last) last.style.fontWeight = '700';
            }
          }

        let sankeyReady = false;

        function initMaterialize(){
          const elems = document.querySelectorAll('.collapsible');
          M.Collapsible.init(elems, {
            accordion: false,
            onOpenEnd: (el) => {
              // jika panel yang dibuka berisi sankey, render/resize di sini
              const holder = el.querySelector('#sankey-chart');
              if (holder) {
                if (!sankeyReady) {
                  setupSankey();      
                  sankeyReady = true;
                } else {
                  Plotly.Plots.resize(holder);  
                }
              }
              if (el.querySelector('#gen-table')) {
                decorateTableByHeader({
                  tableId: 'gen-table',
                  headers: ['Baby Boomer', 'Pre-Boomer'],
                  provinceCol: 0,
                  yellow: [
                    'Riau','Jambi','Bengkulu','Bangka-Belitung','Nusa Tenggara Barat',
                    'Kalimantan Tengah','Kalimantan Utara','Sulawesi Tengah','Maluku Utara','Papua Barat'
                  ],
                  red: ['Maluku','Sulawesi Barat','Kepulauan Riau']
                });
              }


                if (el.querySelector('#age-table')) {
                  decorateTableByHeader({
                    tableId: 'age-table',
                    headers: ['60+ yo'],
                    provinceCol: 0,
                    yellow: [
                      'Riau','Jambi','Bengkulu','Bangka-Belitung','Nusa Tenggara Barat', 'Kalimantan Barat',
                      'Kalimantan Tengah','Kalimantan Utara','Sulawesi Tengah','Maluku Utara','Papua Barat'
                    ],
                    red: ['Gorontalo','Sulawesi Barat','Kepulauan Riau']
                  });
                }

                if (el.querySelector('#disability-table')) {
                  decorateTableByHeader({
                    tableId: 'disability-table',
                    headers: ['disabled'],
                    provinceCol: 0,
                    yellow: [
                      'Riau','Jambi','Sumatera Selatan','Bengkulu','Lampung','Bangka-Belitung','DKI Jakarta','D I Yogyakarta','Banten','Bali','Nusa Tenggara Barat', 'Kalimantan Barat',
                      'Kalimantan Tengah','Kalimantan Selatan','Kalimantan Timur','Sulawesi Utara','Sulawesi Tengah','Sulawesi Selatan','Sulawesi Tenggara','Gorontalo','Sulawesi Barat','Maluku','Papua','Papua Barat'
                    ],
                    red: ['Kalimantan Utara'],
                    exact: true
                  });
                }
              requestAnimationFrame(setHeight);
            },
            onCloseEnd: () => requestAnimationFrame(setHeight)
          });
          setHeight();
        }

        const SANKEY_MAP = __SANKEY_MAP__;

        function sankeyToPlotly(data) {

          const nodes = [...new Set(data.flatMap(([s,t,_]) => [s,t]))];
          const index = Object.fromEntries(nodes.map((n,i)=>[n,i]));
          const source = data.map(([s]) => index[s]);
          const target = data.map(([,t]) => index[t]);
          const value  = data.map(([, ,v]) => +v);


          const inTot  = new Array(nodes.length).fill(0);
          const outTot = new Array(nodes.length).fill(0);
          for (let i=0;i<value.length;i++){ inTot[target[i]]+=value[i]; outTot[source[i]]+=value[i]; }
          const totals = inTot.map((v,i)=> v>0 ? v : outTot[i]);

          const labelsPlain  = nodes;                                    
          const labelsNumber = nodes.map((n,i)=> `${n}<br>${totals[i].toFixed(2)}`); 

          return { nodes, link:{source,target,value}, totals, labelsPlain, labelsNumber };
        }


        let currentChoice = 'All';
        let sankeyCache = null;

        function renderSankey(choice='All'){
          currentChoice = choice;
          const el = document.getElementById('sankey-chart');
          if(!el || typeof Plotly === 'undefined') return;

          const arr = SANKEY_MAP[choice] || SANKEY_MAP['All'];
          const {nodes, link, totals, labelsPlain, labelsNumber} = sankeyToPlotly(arr);
          sankeyCache = {link, totals, labelsPlain, labelsNumber};

          const colors = ['#8dd3c7','#8CD5AE','#bebada','#E1A0A0','#DFC78C'];
          const linkColors = link.value.map((_, i) => colors[i % colors.length]);

          const trace = {
            type: 'sankey',
            valueformat: '.2f',
            node: {
              pad:20, thickness:20,
              label: labelsPlain,
              line:{color:'#000', width:0.5},
              textfont:{size:13, color:'#111'},
              customdata: totals,
              hovertemplate: '%{label}<br>%{customdata:.2f}%<extra></extra>'
            },
            link: {
              ...link,
              color: linkColors,
              hovertemplate: '%{value:.2f}%<extra></extra>'
            }
          };

          const layout = {
            margin:{l:0,r:0,t:8,b:24},
            paper_bgcolor:'rgba(0,0,0,0)',
            plot_bgcolor:'rgba(0,0,0,0)',
            height: 420,
            // TIDAK ADA title di mode web
          };

          Plotly.react(el, [trace], layout, {displayModeBar:false});
          requestAnimationFrame(setHeight);
        }

        function buildTitle(choice){
          const map = { Male:'Men', Female:'Women' };
          const who = map[choice] || choice; 
          var titleFinal = ""

          if (who !== 'All') {
            titleFinal = `Distribution of STEM Graduates by Employment Status in ${who}, 2024`;

          }else{
            titleFinal = `Distribution of STEM Graduates by Employment Status, 2024`;
          }
          return titleFinal;
        }

        function buildDownloadFigure(choice){
          const arr = SANKEY_MAP[choice] || SANKEY_MAP['All'];
          const { link, labelsNumber } = sankeyToPlotly(arr);

          const colors = ['#8dd3c7','#8CD5AE','#bebada','#E1A0A0','#DFC78C'];
          const linkColors = link.value.map((_, i) => colors[i % colors.length]);

          const data = [{
            type: 'sankey',
            valueformat: '.2f',
            node: {
              pad: 28, thickness: 20,
              label: labelsNumber,
              line: { color: '#000', width: 0.5 },
              textfont: { size: 14, color: '#111' },
              hovertemplate: '%{label}<extra></extra>' // (tak penting untuk file)
            },
            link: {
              ...link,
              color: linkColors,
              hovertemplate: '%{value:.2f}%<extra></extra>'
            }
          }];

          const layout = {
            width: 1200, height: 560,
            margin: { l: 30, r: 30, t: 70, b: 80 },
            paper_bgcolor: '#ffffff',
            plot_bgcolor: '#ffffff',
            title: { text: buildTitle(choice), x: 0.5, xanchor: 'center', font: { size: 18, color: '#111' } }
          };
          return { data, layout };
        }
        function setupSankey(){
          const select = document.getElementById('sankey-filter');
          const el = document.getElementById('sankey-chart');
          if(!select || !el) return;

          M.FormSelect.init(select, {
            dropdownOptions: {
              container: document.body,   
              coverTrigger: false,
              constrainWidth: false,
              alignment: 'left',
              closeOnClick: true
            }
          });
          
          setTimeout(() => {
            const inst = M.FormSelect.getInstance(select);
            inst && inst.dropdown && inst.dropdown.recalculateDimensions();
          }, 0);
          renderSankey(select.value || 'All');

          select.addEventListener('change', (e) => {
            e.stopPropagation();                
            renderSankey(e.target.value);
          });

          const dl = document.getElementById('sankey-download');
          if (dl) {
            dl.addEventListener('click', async (e) => {
              e.preventDefault();
              const fmt = e.altKey ? 'jpeg' : 'png';
              const safe = String(currentChoice || 'All').replace(/[^\w\-]+/g,'_');
              const { data, layout } = buildDownloadFigure(currentChoice);

              const holder = document.createElement('div');
              holder.style.cssText =
                `position:fixed;left:-99999px;top:-99999px;width:${layout.width}px;height:${layout.height}px;opacity:0;pointer-events:none;`;
              document.body.appendChild(holder);

              try {
                await Plotly.newPlot(holder, data, layout, { staticPlot: true, displayModeBar: false, responsive: false });
                await Plotly.downloadImage(holder, { format: fmt, filename: `sankey_${safe}_2024`, width: layout.width, height: layout.height, scale: 2 });
              } finally {
                Plotly.purge(holder);
                holder.remove();
              }
            });
          }

          const ro = new ResizeObserver(() => Plotly.Plots.resize(el));
          ro.observe(el);
        }
        function clearActive(){
          cards.forEach(c => c.classList.remove('active'));
          activeId = null;
          if (TITLE) TITLE.textContent = 'Topic';   
          LIST.innerHTML = "";
          HERO.innerHTML = "";
          QUOTES.innerHTML = "";                     
          CLOSE_BAR.classList.remove('show');
          GRID.style.display = "";
          requestAnimationFrame(() => {
            GRID.classList.remove('is-hidden');
            fadeOut(LIST); fadeOut(HERO); fadeOut(QUOTES);
            setHeight();
          });
          sankeyReady = false;  
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
          if (TITLE) TITLE.textContent = card.dataset.label || 'Topic';


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

          const GEOJSON = __GEOJSON__;
          const MAPDATA = __MAPDATA__;


          const props0 = GEOJSON?.features?.[0]?.properties || {};
          const FEATURE_KEY = ('Provinsi' in props0) ? 'Provinsi'
                          : ('Propinsi' in props0) ? 'Propinsi'
                          : Object.keys(props0)[0];


          const canon = s => String(s ?? '')
            .normalize('NFKD')
            .replace(/[.\s\u00A0\-–—_/]/g, '')
            .toUpperCase();


          const geoNameMap = new Map(
            (GEOJSON.features || []).map(f => {
              const raw = f.properties[FEATURE_KEY];
              return [canon(raw), String(raw)];
            })
          );


          const ALIAS = new Map([
            ['ACEH','DI. ACEH'],
            ['DIYOGYAKARTA','DAERAH ISTIMEWA YOGYAKARTA'],
            ['DAERAHISTIMEWAYOGYAKARTA','DAERAH ISTIMEWA YOGYAKARTA'],
          ]);

          const locationsFixed = (MAPDATA.locations || []).map(src => {
            const c = canon(src);
            return geoNameMap.get(c) || ALIAS.get(c) || null;
          });


          const misses = [];
          locationsFixed.forEach((v,i)=>{ if(!v) misses.push(MAPDATA.locations[i]); });
          console.warn('Masih tidak ketemu:', misses.length ? misses : '—');
          console.table((MAPDATA.locations||[]).map((src,i)=>({src, mapped: locationsFixed[i]})));


          const z = (MAPDATA.values || []).map(v => (v==null || v==='') ? null : +v);
          const SCALE_BLUE = [[0, "#b8d7f2"], [1, "#3498db"]];

          Plotly.newPlot(
            "choropleth",
            [{
              type: "choropleth",
              geojson: GEOJSON,
              featureidkey: `properties.${FEATURE_KEY}`,
              locations: locationsFixed,
              z,
              colorscale: SCALE_BLUE,
              marker: { line: { color: "white", width: 0.5 } },
              colorbar: { title: "" },

              hovertemplate: "<b>%{location}</b><br>Percentage of STEM University Graduates : %{z:.2f}%<extra></extra>"
            }],
            {
              geo: { fitbounds: "geojson", visible: false },
              margin: { t:0, r:0, b:0, l:0 },
              height: 500,

              hoverlabel: { namelength: -1 }
            },
            { responsive: true }
          ).then(() => setHeight());

          
          const PROV_CSV_BTN = document.getElementById('prov-csv-btn');
          if (PROV_CSV_BTN) {
            PROV_CSV_BTN.href = CSV_PROV_URL;
            PROV_CSV_BTN.setAttribute('download', CSV_PROV_FILENAME);
          }


        CLOSE_BTN.addEventListener('click', function(){
          CLOSE_BAR.classList.remove('show');
          fadeOut(LIST, function(){ LIST.innerHTML = ""; setHeight(); });
          fadeOut(QUOTES, function(){ QUOTES.innerHTML = ""; setHeight(); });
          fadeOut(HERO, function(){
            HERO.innerHTML = "";
            GRID.style.display = "";
            TITLE.textContent = "Topic";
            requestAnimationFrame(() => { GRID.classList.remove('is-hidden'); setHeight(); });
            activeId = null;
            cards.forEach(c => c.classList.remove('active'));
            sankeyReady = false;       
          });
        });
      })();
    </script>
  </body>
</html>
"""



card_html = card_html.replace("__SANKEY_MAP__", json.dumps(dataset_map, ensure_ascii=False))
card_html = card_html.replace("__OVERVIEW_HTML__", overview_html_js)
card_html = card_html.replace("__CSV_DATA__", overview_csv_js)
card_html = card_html.replace("__CSV_FILENAME__", csv_filename_sex)

card_html = card_html.replace("__OVERVIEW_GEN_HTML__", overview_html_gen_js)
card_html = card_html.replace("__CSV_GEN_DATA__", overview_csv_gen_js)
card_html = card_html.replace("__CSV_GEN_FILENAME__", csv_filename_gen)


card_html = card_html.replace("__OVERVIEW_AGE_HTML__", overview_html_age_js)
card_html = card_html.replace("__CSV_AGE_DATA__", overview_csv_age_js)
card_html = card_html.replace("__CSV_AGE_FILENAME__", csv_filename_age)

card_html = card_html.replace("__OVERVIEW_DISABILITY_HTML__", overview_html_disability_js)
card_html = card_html.replace("__CSV_DISABILITY_DATA__", overview_csv_disability_js)
card_html = card_html.replace("__CSV_DISABILITY_FILENAME__", csv_filename_disability)


card_html = card_html.replace("__OVERVIEW_EDUNOCUP_HTML__", overview_html_edunocup_js)
card_html = card_html.replace("__CSV_EDUNOCUP_DATA__", overview_csv_edunocup_js)
card_html = card_html.replace("__CSV_EDUNOCUP_FILENAME__", csv_filename_edunocup)

# inject placeholder ke template HTML
card_html = card_html.replace("__CSV_PROV_DATA__", csv_prov_js)
card_html = card_html.replace("__CSV_PROV_FILENAME__", csv_prov_filename)

# inject ke template
card_html = card_html.replace("__CSV_PROV_DATA__", csv_prov_js)
card_html = card_html.replace("__CSV_PROV_FILENAME__", csv_prov_filename)

df_js = df_province_dist[["Province", "Total"]].copy()
if df_js['Province'].iloc[-1].strip().casefold() == 'indonesia':
    df_js = df_js.iloc[:-1]
df_js["Province"] = df_js["Province"].replace(province_name_mapping)

data_dict = {
    "locations": df_js["Province"].tolist(),
    "values": df_js["Total"].tolist()
}

geojson_str = json.dumps(indonesia_geojson, ensure_ascii=False)
data_map = {
    "locations": df_js["Province"].tolist(),  
    "values": df_js["Total"].tolist()
}
card_html = card_html.replace("__GEOJSON__", geojson_str)
card_html = card_html.replace("__MAPDATA__", json.dumps(data_map, ensure_ascii=False))


components.html(card_html, height=0, scrolling=False)
