import plotly.express as px
import pandas as pd
import streamlit as st
from tir_1_read_db import read_db


@st.cache(allow_output_mutation=True)
def return_df():
    data = read_db()
    data = data.rename(columns={'CUST_NAME_x': "Ölkəyə daxilolma postu",
                            'CUST_NAME_y': "Ölkədən xaricolma postu",
                            'Weight_K_tons': 'Çəki (min tonla)',
                            'Count': "TIR sayı",
                            'PERMISSION_PRICE_x': "Ölkəyə daxiloduqda ödənilən məbləğ (ABŞ dolları)"})
    return data


# @st.cache(allow_output_mutation=True)
# def return_times(data):
#     return data.sort_values(['Year_x', 'Month_x'])['Tarix'].unique()


@st.cache()
def lats_longs():
    postlar_long_lat = {'Qırmızı körpü': [41.328535, 45.071148],
                        'Mazımçay': [41.791336, 46.309789],
                        'Samur': [41.637499, 48.418],
                        'Şirvanlı': [41.706865, 48.475607],
                        'Xanoba': [41.781766, 48.555877],
                        'BDT Limanı': [39.977711, 49.446351],
                        'Biləsuvar': [39.389668, 48.361487],
                        'Astara': [38.441115, 48.875787],
                        'Şahtaxtı': [39.361079, 45.070958],
                        'Culfa': [38.945613, 45.632566],
                        'Sədərək': [39.655905, 44.803632],
                        'Eyvazlı': [39.429299, 46.385027]
                        }
    return postlar_long_lat


lats_longs = lats_longs()


def data_for_map_plot(selected_category, selected_value, df, max_year=2019, max_month=12, postlar_lats_lon=lats_longs):
    df = df[df['Year_x'] <= max_year]
    df = df[df['Month_x'] <= max_month]
    long_lat = pd.DataFrame(postlar_lats_lon).T.reset_index()
    group_by_post = df.groupby([selected_category]).sum()[selected_value].reset_index()
    group_by_post[selected_value] = group_by_post[selected_value].apply(lambda x: round(x))
    long_lat.columns = ['index', 'Enlik', 'Uzunluq']
    final_df = pd.merge(group_by_post, long_lat, how='left', left_on=selected_category, right_on='index')

    return final_df


def map_plot(final_df, selected_category, selected_value):
    token = 'pk.eyJ1IjoiZW1pbG1pbmNvbSIsImEiOiJjbGQ5c21mcngwYnkzM3BvMmdibHRoN2RoIn0.UD-bUU4VEFBmRsxprEclgA'
    style = 'mapbox://styles/emilmincom/clda8i8yo003z01oc4rp7fmp1'
    fig = px.scatter_mapbox(final_df,
                            lat="Enlik",
                            lon="Uzunluq",
                            color=final_df[selected_category],
                            size=final_df[selected_value],
                            hover_data={"Enlik": False, "Uzunluq": False},
                            color_continuous_scale=px.colors.cyclical.IceFire,
                            size_max=100,
                            zoom=6.5,
                            width=1200,
                            height=900)
    fig.update_layout(mapbox_accesstoken=token, mapbox_style=style)
    fig.update_layout(title_font_size=24, title="Xəritədə seçilən parametrlər üzrə vizuallaşdırma")
    return fig
