import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from a_read_db import read_db


def data_for_trend_line_country_based(selected_country, aggregated_column):
    df = read_db()
    f = df[(df['From'] == selected_country) | (df['To'] == selected_country)].groupby(
        ["Year_x", "Month_x", 'Tarix']).agg({'Count': 'count',
                                             # 'PERMISSION_PRICE_x': 'sum',
                                             'Weight_K_tons': 'sum'}).reset_index()[["Year_x", "Month_x", 'Tarix',
                                                                                     aggregated_column]].sort_values(["Year_x", "Month_x"])
    if aggregated_column == 'Count':
        f.columns = ["Year_x", "Month_x", "Tarix", "TİR-ların sayı"]
        fig = px.line(f, x='Tarix', y="TİR-ların sayı", markers=True, line_shape='spline')
    elif aggregated_column == 'Weight_K_tons':
        f.columns = ["Year_x", "Month_x", "Tarix", "Çəki (min ton)"]
        f["Çəki (min ton)"] = f["Çəki (min ton)"].apply(lambda x: round(x))
        fig = px.line(f, x='Tarix', y="Çəki (min ton)", markers=True, line_shape='spline')
    # fig.update_yaxes(showgrid=False)
    fig.update_xaxes(nticks=4, showgrid=False)
    fig.update_traces(line_color='#075586', line_width=2, marker=dict(size=5))
    # fig.update_layout({
    #     'plot_bgcolor': 'rgba(0, 0, 0, 0)',
    #     'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    # })
    return fig


def data_for_country_flow_by_year_and_countries(selected_country, direction):
    df = read_db()
    if direction == "From":
        f = df[df['To'] == selected_country].groupby(['Year_x', 'From']).sum().reset_index()[
            ['Year_x', 'From', 'Weight_K_tons']].sort_values(['Year_x', 'Weight_K_tons'], ascending=False)
        f['Weight_K_tons'] = f['Weight_K_tons'].apply(lambda x: round(x, 2))
        f = f[f['Weight_K_tons'] != 0]
        f.columns = ['İl', 'İstiqamətin başlanğıcı', 'Çəki (min tonla)']
        fig = px.sunburst(f, path=['İl', 'İstiqamətin başlanğıcı'], values='Çəki (min tonla)',
                          color='Çəki (min tonla)', color_continuous_scale='blues')
        fig.update_traces(hovertemplate='Çəki (min tonla) = %{value}')

    elif direction == 'To':
        f = df[df['From'] == selected_country].groupby(['Year_x', 'To']).sum().reset_index()[
            ['Year_x', 'To', 'Weight_K_tons']].sort_values(['Year_x', 'Weight_K_tons'], ascending=False)
        f['Weight_K_tons'] = f['Weight_K_tons'].apply(lambda x: round(x, 2))
        f = f[f['Weight_K_tons'] != 0]
        f.columns = ['İl', 'İstiqamətin təyintaı', 'Çəki (min tonla)']
        fig = px.sunburst(f, path=['İl', 'İstiqamətin təyintaı'], values='Çəki (min tonla)',
                          color='Çəki (min tonla)', color_continuous_scale='blues')
        fig.update_traces(hovertemplate='Çəki (min tonla) = %{value}')

    return fig


@st.cache(allow_output_mutation=True)
def data_for_sankey():
    df = read_db()
    df['CUST_NAME_y'] = df['CUST_NAME_y'].replace('Şahtaxtı', "Şahtaxtı və ya Culfa")
    df['CUST_NAME_y'] = df['CUST_NAME_y'].replace('Culfa', "Şahtaxtı və ya Culfa")
    df = df[~(df['CUST_NAME_x'].isin(["Şimal Ərazi BGİ", "DGK", "ERDN BGİ"]))]
    df = df[~(df['CUST_NAME_y'].isin(["Şimal Ərazi BGİ", "DGK", "ERDN BGİ"]))]
    df['Compass_point_x'] = df['Compass_point_x'].replace('Naxçıvan Cənub', "Naxçıvan")
    df['Compass_point_y'] = df['Compass_point_y'].replace('Naxçıvan Cənub', "Naxçıvan")
    df['Compass_point_x'] = df['Compass_point_x'].replace('Naxçıvan Qərb', "Naxçıvan")
    df['Compass_point_y'] = df['Compass_point_y'].replace('Naxçıvan Qərb', "Naxçıvan")
    return df


def sankey_figure_for_tir(selected_year):
    df = data_for_sankey()
    df = df[df['Year_x'] == selected_year]
    f = df.groupby(['Compass_point_x', 'CUST_NAME_x', 'CUST_NAME_y', 'Compass_point_y']).sum().reset_index()[
        ['Compass_point_x', 'CUST_NAME_x', 'CUST_NAME_y', 'Compass_point_y', 'Count']]
    f = f.sort_values(['Count', ], ascending=False)
    f.columns = ['Ölkəyə daxil olduğu ərazi', 
                 # 'Ölkəyə daxil olduğu post', 
                 # 'Ölkədən çıxdığı post',
                 'Ölkədən çıxdığı ərazi', 
                 'Tırların sayı']
    f_dict = {}
    for i in f.columns.values[:-1]:
        f_dict[i] = f[i].values.tolist()
    f_dict_list = []
    for key, value in f_dict.items():
        f_dict_list.append({'label': key,
                            'values': value})
    color = [(x - f['Tırların sayı'].min()) / (f['Tırların sayı'].max() - f['Tırların sayı'].min()) for x in
             f['Tırların sayı']]
    colorscale = [[0.0, 'skyblue'],
                  [0.5, 'tomato'],
                  [1.0, 'salmon']]
    fig = go.Figure(go.Parcats(
        dimensions=f_dict_list,
        counts=f['Tırların sayı'].values.tolist(),
        line={'color': color, 'colorscale': colorscale, "shape": "hspline"}
    ))
    fig.update_layout(margin=dict(l=30, r=30, t=40, b=40))

    return fig


def trend_figure_acording_to_post_in_out_flow_count_or_weight(selected_post, flow, indicator):
    df = data_for_sankey()

    if flow == "Ölkəyə daxil olan TIR-lar üzrə":
        flow = 'CUST_NAME_x'
    elif flow == 'Ölkədən çıxan TIR-lar üzrə':
        flow = 'CUST_NAME_y'

    f = df[df[flow] == selected_post]
    f = f.sort_values(['Year_x', 'Month_x'])
    pt = f.groupby(['Year_x', 'Month_x', 'Tarix']).sum().reset_index()[['Tarix', "Weight_K_tons", "Count"]]
    pt.columns = ['Tarix', "Çəki (min ton)", "TİR-ların sayı"]
    pt["Çəki (min ton)"] = pt["Çəki (min ton)"].apply(lambda x: round(x))
    fig = px.line(pt, x='Tarix', y=indicator, markers=True, line_shape='spline')
    fig.update_xaxes(nticks=6, showgrid=False)
    fig.update_traces(line_color='#075586', line_width=2, marker=dict(size=5))

    return fig












