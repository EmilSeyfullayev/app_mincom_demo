import streamlit as st
from ady_3_visualisation_functions import regime_trend_line, dehliz_trend_line, olkeler_uzre_trend_line
from ady_1_read_db import unique_country_names

country_names = unique_country_names()

# trend_line_chart = regime_trend_line()

st.markdown("<h6 style='text-align: right; color: #075586;'>©Nəqliyyat siyasəti şöbəsi</h6>",
        unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["Rejimlər üzrə trend təsvir", "Dəhlizlər üzrə trend təsvir", "Ölkələr üzrə"])
with tab1:
    c1, c2, c3 = st.columns((3, 3, 4))
    with c1:
        regime = st.selectbox("Seçilmiş daşınma rejimi", ['İdxal', "İxrac", "Tranzit", "Daxili"], 2)
        st.markdown("<h6>Seçilmiş rejim üzrə trend təsvir</h6>", unsafe_allow_html=True)
    st.plotly_chart(regime_trend_line(rejim=regime), use_container_width=True)

with tab2:
    c1, c2, c3 = st.columns((3, 3, 4))
    with c1:
        dehliz = st.selectbox("Seçilmiş dəhliz", ['Şimal-Qərb', 'Şərq-Qərb', 'Şimal-Şərq',
                                               'Şimal-Cənub', 'Cənub-Qərb', 'Cənub-Şərq'], 3)
        st.markdown("<h6>Seçilmiş dəhliz üzrə tranzit daşımaların trend təsviri</h6>", unsafe_allow_html=True)

    st.plotly_chart(dehliz_trend_line(dehliz=dehliz), use_container_width=True)

with tab3:
    c1, c2, c3 = st.columns((2, 5, 1))
    with c1:
        country_name = st.selectbox("Seçilmiş ölkə", country_names, 3)

    with c2:
        regimes = st.multiselect('Seçilmiş rejimlər', ['İdxal', 'İxrac',
                                                       'Tranzit dövriyyəsi',
                                                       'Tranzit (seçilmiş ölkədən)',
                                                       'Tranzit (seçilmiş ölkəyə)'],
                                                     ['İdxal', 'İxrac',
                                                      'Tranzit dövriyyəsi'])
    st.markdown("<h6>Seçilmiş ölkə və rejimlər üzrə daşımaların trend təsviri</h6>", unsafe_allow_html=True)
    st.plotly_chart(olkeler_uzre_trend_line(selected_country=country_name,
                                            regimes=regimes
                                            ), use_container_width=True)








