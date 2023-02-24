import streamlit as st
from ady_1_read_db import read_ady_db
from ady_1_read_db import transit_ady_data, unique_country_names
from ady_2_functions_to_create_tables_by_country import pivot_tables_by_country


country_names = unique_country_names()
tr = transit_ady_data()
try:
    c1, c2, c3 = st.columns((1, 2, 1))

    with c1:
        selected_country = st.selectbox("Seçilmiş ölkə", country_names, 0)
    with c2:
        selected_years_list = sorted(tr['Tarix Hierarchy - İl'].unique().tolist())
        selected_years = st.multiselect('Seçilmiş illər', selected_years_list,
                                        # selected_years_list[-2:],
                                        selected_years_list,
                                        )
    with c3:
        monthes = sorted(
            tr[tr['Tarix Hierarchy - İl'] == max(selected_years)]['Month'].unique().tolist()
        )
        selected_max_month = st.selectbox("İlk neçə ay?", monthes, len(monthes)-1)

    pt = pivot_tables_by_country(tr, selected_country, selected_years,
                                 selected_max_month).style.format(precision=0)
    pt_from = pivot_tables_by_country(tr, selected_country,
                                      selected_years, selected_max_month, type='from').style.format(precision=0)
    pt_to = pivot_tables_by_country(tr, selected_country,
                                    selected_years, selected_max_month, type='to').style.format(precision=0)

    pt1 = pivot_tables_by_country(tr, selected_country, selected_years, selected_max_month)
    pt1 = pt1.style.format(precision=0)

    st.markdown(f'## {selected_country}, ilk {selected_max_month} ay')
    st.markdown('### Dəmir yolu ilə daşınmış tranzit yükün dəhlizlər üzrə həcmi, dövriyyə, min tonla')
    st.dataframe(pt, width=700)
    st.markdown('### Seçilmiş ÖLKƏDƏN dəmir yolu ilə daşınmış tranzit yükün növü üzrə həcmi, min tonla')
    st.dataframe(pt_from, width=700)
    st.markdown('### Seçilmiş ÖLKƏYƏ dəmir yolu ilə daşınmış tranzit yükün növü üzrə həcmi, min tonla')
    st.dataframe(pt_to, width=700)
except:
    st.info('Seçilmiş parametrlər üzrə məlumat tapılmadı')
