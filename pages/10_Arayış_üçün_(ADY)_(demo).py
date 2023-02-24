import pandas as pd
import streamlit as st
from ady_functions import iller_uzre_pivot_table, unique_country_names

st.markdown("<h6 style='text-align: right; color: #075586;'>©Nəqliyyat siyasəti şöbəsi - Tranzit yükdaşımalar</h6>",
        unsafe_allow_html=True)

unique_country_names_list = unique_country_names()
selected_country = st.sidebar.selectbox("Seçilmiş ölkə",
                                        unique_country_names_list,
                                        unique_country_names_list.index("Türkiyə"))
index = st.sidebar.selectbox("Göstərici", ["Dəhliz", "Yük qrupu (ADY)"], 0)
direction = st.sidebar.selectbox("İstiqamət", ["Dövriyyə", "Seçilmiş ölkədən", "Seçilmiş ölkəyə"], 0)


pt, max_month = iller_uzre_pivot_table(selected_country, index, direction)

st.markdown(f"### {selected_country} - dəmiryolu ilə tranzit daşımalar")
st.write(f'**Göstərici:** {index}; **İstiqamət:** {direction}, (Həcm, min ton, ilk {max_month}* ay)')
st.write(f"")


try:
    st.dataframe(pt, use_container_width=True)
except:
    st.write(pt)



