import streamlit as st
import pandas as pd
from a_read_db import country_names
from a_data_for_visualisations_of_TİR_data_by_country import data_for_trend_line_country_based, \
    data_for_country_flow_by_year_and_countries

st.markdown("<h6 style='text-align: right; color: #075586;'>©Nəqliyyat siyasəti şöbəsi - Tranzit yükdaşımalar</h6>",
        unsafe_allow_html=True)

country_names = country_names()
selected_country = st.sidebar.selectbox("Seçilmiş ölkə", country_names, 0)

figure_count = data_for_trend_line_country_based(selected_country, aggregated_column='Count')
figure_weight = data_for_trend_line_country_based(selected_country, aggregated_column='Weight_K_tons')

figure_from = data_for_country_flow_by_year_and_countries(selected_country, direction='From')
figure_to = data_for_country_flow_by_year_and_countries(selected_country, direction='To')

st.write(f'### {selected_country}')

tab1, tab2, tab3 = st.tabs(["Seçilmiş ölkə üzrə dövriyyənin trend təsviri", "Seçilmiş ölkədən", "Seçilmiş ölkəyə"])
with tab1:
    c1, c2 = st.columns((5, 5))
    with c1:
        st.plotly_chart(figure_count, use_container_width=True)
    with c2:
        st.plotly_chart(figure_weight, use_container_width=True)
with tab2:
    st.plotly_chart(figure_from, use_container_width=True)
with tab3:
    st.plotly_chart(figure_to, use_container_width=True)

