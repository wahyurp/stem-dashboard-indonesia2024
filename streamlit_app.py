#######################
# Import libraries
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import json

#######################
# Page configuration
st.set_page_config(
    page_title="Indonesia STEM Employment Dashboard",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")

#######################
# CSS styling
st.markdown("""
<style>

[data-testid="block-container"] {
    padding-left: 2rem;
    padding-right: 2rem;
    padding-top: 1rem;
    padding-bottom: 0rem;
    margin-bottom: -7rem;
}

[data-testid="stVerticalBlock"] {
    padding-left: 0rem;
    padding-right: 0rem;
}

[data-testid="stMetric"] {
    background-color: #393939;
    text-align: center;
    padding: 15px 0;
}

[data-testid="stMetricLabel"] {
  display: flex;
  justify-content: center;
  align-items: center;
}

[data-testid="stMetricDeltaIcon-Up"] {
    position: relative;
    left: 38%;
    -webkit-transform: translateX(-50%);
    -ms-transform: translateX(-50%);
    transform: translateX(-50%);
}

[data-testid="stMetricDeltaIcon-Down"] {
    position: relative;
    left: 38%;
    -webkit-transform: translateX(-50%);
    -ms-transform: translateX(-50%);
    transform: translateX(-50%);
}

</style>
""", unsafe_allow_html=True)


#######################
# Load data
# df_reshaped = pd.read_csv('data/us-population-2010-2019-reshaped.csv')
df_disability = pd.read_excel("data.xlsx", sheet_name="disability")
df_sex = pd.read_excel("data.xlsx", sheet_name="sex")
df_edunocup = pd.read_excel("data.xlsx", sheet_name="edunocup")
df_gen = pd.read_excel("data.xlsx", sheet_name="gen")

#######################
# Sidebar
# with st.sidebar:
#     st.title('🔬 US Population Dashboard')
    
#     # year_list = list(df_reshaped.year.unique())[::-1]
    
#     # selected_year = st.selectbox('Select a year', year_list)
#     # df_selected_year = df_reshaped[df_reshaped.year == selected_year]
#     # df_selected_year_sorted = df_selected_year.sort_values(by="population", ascending=False)
#     province_list = df_disability["Province"].unique().tolist()
#     selected_province = st.selectbox("Select Province:", province_list, index=province_list.index("Indonesia"))


#     color_theme_list = ['blues', 'cividis', 'greens', 'inferno', 'magma', 'plasma', 'reds', 'rainbow', 'turbo', 'viridis']
#     selected_color_theme = st.selectbox('Select a color theme', color_theme_list)


#######################
# Plots




def population_pyramid(df, province_col, male_col, female_col, width=600, height=400):


    df_long = df[[province_col, male_col, female_col]].melt(
        id_vars=[province_col], 
        value_vars=[male_col, female_col],
        var_name="gender", 
        value_name="population"
    )

    df_long.loc[df_long["gender"] == male_col, "population"] *= -1
    
    pyramid = alt.Chart(df_long).transform_calculate(
        abs_population="abs(datum.population)"
    ).mark_bar().encode(
        y=alt.Y(f"{province_col}:N", sort=df[province_col].tolist(), title="Province"),
        x=alt.X("population:Q", 
                title="Percentage",
                axis=alt.Axis(format="s", labelExpr="abs(datum.value)", grid=False)),  # label positif
        color=alt.Color("gender:N", 
                        scale=alt.Scale(domain=[male_col, female_col], 
                                        range=["#1f77b4", "#ff7f0e"])),
        tooltip=[
            alt.Tooltip(f"{province_col}:N", title="Province"),
            alt.Tooltip("gender:N", title="Gender"),
            alt.Tooltip("abs_population:Q", title="Percentage")  # kasih type :Q
        ]
    ).properties(width=width, height=height)
    
    rule = alt.Chart(pd.DataFrame({'x': [0]})).mark_rule().encode(x='x:Q')
    
    return pyramid + rule

# Heatmap
def make_heatmap(input_df, input_y, input_x, input_color, input_color_theme):
    heatmap = alt.Chart(input_df).mark_rect().encode(
            y=alt.Y(f'{input_y}:O', axis=alt.Axis(title="", titleFontSize=18, titlePadding=15, titleFontWeight=900, labelAngle=0)),
            x=alt.X(f'{input_x}:O', axis=alt.Axis(title="", titleFontSize=18, titlePadding=15, titleFontWeight=900)),
            color=alt.Color(f'max({input_color}):Q',
                             legend=None,
                             scale=alt.Scale(scheme=input_color_theme)),
            stroke=alt.value('black'),
            strokeWidth=alt.value(0.25),
        ).properties(width=900,height=850
        ).configure_axis(
        labelFontSize=12,
        titleFontSize=12
        ) 
    # height=300
    return heatmap



with open("indonesia-prov-clean.geojson", "r", encoding="utf-8") as f:
    indonesia_geojson = json.load(f)


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
    
    # print(df_plot)
    # print(province_col)
    df_plot = df_plot[df_plot[province_col] != "Indonesia"]
    
    choropleth = px.choropleth(
        df_plot,
        geojson=indonesia_geojson,
        locations=province_col,
        featureidkey="properties.Propinsi",
        color=value_col,
        color_continuous_scale=color_theme,
        range_color=(0, df_plot[value_col].max()),
        labels={value_col: ""},
    )

    # Styling
    choropleth.update_geos(fitbounds="locations", visible=False)
    choropleth.update_layout(
        template="plotly_dark",
        plot_bgcolor="rgba(0, 0, 0, 0)",
        paper_bgcolor="rgba(0, 0, 0, 0)",
        margin=dict(l=0, r=0, t=0, b=0),
        height=350
    )
    
    return choropleth



# Donut chart
def make_donut(input_response, input_text, input_color):
    if input_color == 'blue':
        chart_color = ['#29b5e8', '#155F7A']
    if input_color == 'green':
        chart_color = ['#27AE60', '#12783D']
    if input_color == 'orange':
        chart_color = ['#F39C12', '#875A12']
    if input_color == 'red':
        chart_color = ['#E74C3C', '#781F16']
      
    source = pd.DataFrame({
        "Topic": ['', input_text],
        "% value": [100-input_response, input_response]
    })
    source_bg = pd.DataFrame({
        "Topic": ['', input_text],
        "% value": [100, 0]
    })
      
    plot = alt.Chart(source).mark_arc(innerRadius=45, cornerRadius=25).encode(
        theta="% value",
        color= alt.Color("Topic:N",
                        scale=alt.Scale(
                            domain=[input_text, ''],
                            range=chart_color),
                        legend=None),
    ).properties(width=130, height=130)
      
    text = plot.mark_text(
        align='center',
        color="#29b5e8",
        font="Lato",
        fontSize=32,
        fontWeight=700,
        fontStyle="italic"
    ).encode(text=alt.value(f'{input_response:.0f} %'))
    
    plot_bg = alt.Chart(source_bg).mark_arc(innerRadius=45, cornerRadius=20).encode(
        theta="% value",
        color= alt.Color("Topic:N",
                        scale=alt.Scale(
                            domain=[input_text, ''],
                            range=chart_color),
                        legend=None),
    ).properties(width=130, height=130)
    
    return plot_bg + plot + text


# Convert population to text 
def format_number(num, is_percent=False):
    if is_percent:
        return f"{num:.2f} %"

    if num > 1000000:
        if not num % 1000000:
            return f'{num // 1000000} M'
        return f'{round(num / 1000000, 1)} M'
    return f'{num // 1000} K'


# Calculation year-over-year population migrations
def calculate_population_difference(input_df, input_year):
  selected_year_data = input_df[input_df['year'] == input_year].reset_index()
  previous_year_data = input_df[input_df['year'] == input_year - 1].reset_index()
  selected_year_data['population_difference'] = selected_year_data.population.sub(previous_year_data.population, fill_value=0)
  return pd.concat([selected_year_data.states, selected_year_data.id, selected_year_data.population, selected_year_data.population_difference], axis=1).sort_values(by="population_difference", ascending=False)


#######################
# Dashboard Main Panel
st.title('🔬 Indonesia STEM Employment Dashboard 2024')
col = st.columns((1.5, 4.5, 2), gap='medium')

with col[0]:
    st.markdown('## Sex')
    selected_province ="Indonesia"
    sex_province_data = df_sex[df_sex["Province"] == selected_province].iloc[0]
    disability_province_data = df_disability[df_disability["Province"] == selected_province].iloc[0]

    st.metric(label="Male", value=format_number(sex_province_data["Male"], is_percent=True))
    st.metric(label="Female", value=format_number(sex_province_data["Female"], is_percent=True))
    
    st.markdown('##### Disability Condition')
    donut_chart_greater = make_donut(disability_province_data['Non-Disabled'], 'Non Disabled', 'green')
    donut_chart_less = make_donut(disability_province_data['Disabled'], 'Disabled', 'red')
    migrations_col = st.columns((0.2, 1, 0.2))
    with migrations_col[1]:
        st.write('Non Disabled')
        st.altair_chart(donut_chart_greater)
        st.write('Disabled')
        st.altair_chart(donut_chart_less)


with col[1]:
    st.markdown('#### Percentage STEM Graduates in STEM Jobs')
    
    fig = make_choropleth(df_edunocup, "Province", "STEM Graduates in STEM Jobs", "rdylgn")

    st.plotly_chart(fig, use_container_width=True)

    st.markdown('#### Percentage of STEM University Graduates by Sex')


    df_sex_exclude_indonesia = df_sex[df_sex["Province"] != "Indonesia"]
    chart = population_pyramid(df_sex_exclude_indonesia, "Province", "Male", "Female")
    st.altair_chart(chart, use_container_width=True)


    

with col[2]:

    st.markdown('#### Percentage of STEM University Graduates by Generation')
    df_ubah = df_gen.melt(id_vars="Province", 
                    value_vars=["Generation Z", "Millenials (Generation Y)", "Generation X", "Baby Boomer & Pre-Boomer"],
                    var_name="Generation", 
                    value_name="Percentage")
    heatmap = make_heatmap(
        input_df=df_ubah,
        input_y="Province",
        input_x="Generation",
        input_color="Percentage",
        input_color_theme="redyellowgreen"
    )
    st.altair_chart(heatmap, use_container_width=True)
    # st.markdown('#### Top States')


    # df_sex_exclude_indonesia = df_sex[df_sex["Province"] != "Indonesia"]
    # chart = population_pyramid(df_sex_exclude_indonesia, "Province", "Male", "Female")
    # st.altair_chart(chart, use_container_width=True)
    # st.dataframe(df_selected_year_sorted,
    #              column_order=("states", "population"),
    #              hide_index=True,
    #              width=None,
    #              column_config={
    #                 "states": st.column_config.TextColumn(
    #                     "States",
    #                 ),
    #                 "population": st.column_config.ProgressColumn(
    #                     "Population",
    #                     format="%f",
    #                     min_value=0,
    #                     max_value=max(df_selected_year_sorted.population),
    #                  )}
    #              )
    
    # with st.expander('About', expanded=True):
    #     st.write('''
    #         - Data: [U.S. Census Bureau](https://www.census.gov/data/datasets/time-series/demo/popest/2010s-state-total.html).
    #         - :orange[**Gains/Losses**]: states with high inbound/ outbound migration for selected year
    #         - :orange[**States Migration**]: percentage of states with annual inbound/ outbound migration > 50,000
    #         ''')
