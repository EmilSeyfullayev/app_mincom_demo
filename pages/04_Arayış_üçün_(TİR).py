import streamlit as st
from a_tir_functions import data_for_selected_country
from a_read_db import country_names, max_year_month_pre_year

st.markdown("<h6 style='text-align: right; color: #075586;'>©Nəqliyyat siyasəti şöbəsi - Tranzit yükdaşımalar</h6>",
        unsafe_allow_html=True)
country_names = country_names()
max_year = max_year_month_pre_year()[0]
max_month = max_year_month_pre_year()[1]
previous_year = max_year_month_pre_year()[2]
unique_monthes = max_year_month_pre_year()[3]

##########################
selected_country = st.sidebar.selectbox("Seçilmiş ölkə", country_names, 0)
selected_month = st.sidebar.selectbox("Müqayisə üçün seçilmiş ayın sırası",
                                      unique_monthes, unique_monthes.index(max_month), key="ay_sirasi")


st.markdown(f'## {selected_country}, ilk {selected_month}* ay')
st.markdown('### Avtomobil yolu ilə daşınmış tranzit yükün həcmi, min tonla')
tmp_weight = data_for_selected_country(
                                selected_country=selected_country,
                                previous_year=previous_year,
                                max_year=max_year,
                                selected_month=selected_month,
                                aggregated_column='Weight_K_tons')
st.dataframe(tmp_weight, use_container_width=True)

st.markdown(f'### Avtomobil yolu ilə tranzit keçən TİR-ların sayı, ədəd ilə')
tmp_weight = data_for_selected_country(
                                selected_country=selected_country,
                                previous_year=previous_year,
                                max_year=max_year,
                                selected_month=selected_month,
                                aggregated_column='Count')
st.dataframe(tmp_weight, use_container_width=True)


