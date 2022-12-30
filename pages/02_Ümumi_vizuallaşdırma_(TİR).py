import streamlit as st
from a_data_for_visualisations_of_TİR_data_by_country import data_for_sankey, sankey_figure_for_tir, trend_figure_acording_to_post_in_out_flow_count_or_weight

st. set_page_config(layout="wide")

df = data_for_sankey()

tab1, tab2 = st.tabs(['Ərazi və postlar üzrə', 'Postların trend təsviri'])

with tab1:
    st.write('### Tranzit keçən TİR-ların ərazi və postlar üzrə marşrutu, say ilə')
    c1, c2 = st.columns((1,3))
    with c1:
        selected_year = st.selectbox('Seçilmiş il',
                                             df['Year_x'].unique().tolist(),
                                             df['Year_x'].unique().tolist().index(df['Year_x'].max()))
    figure_sabkey = sankey_figure_for_tir(selected_year)
    st.plotly_chart(figure_sabkey, use_container_width=True)
with tab2:
    c1, c2, c3 = st.columns((4, 3, 3))
    with c1:
        selected_flow = st.selectbox('İstiqamət', ["Ölkəyə daxil olan TIR-lar üzrə", 'Ölkədən çıxan TIR-lar üzrə'], 0)
    if selected_flow == "Ölkəyə daxil olan TIR-lar üzrə":
        with c2:
            selected_post = st.selectbox("Seçilmiş post",
                                     ['Qırmızı körpü', 'Samur', 'BDT Limanı', 'Mazımçay', 'Biləsuvar',
                                       'Eyvazlı', 'Sədərək', 'Astara', 'Şirvanlı', 'Xanoba', 'Şahtaxtı', 'Culfa'],
                                     0, key='selected_post')
    elif selected_flow == "Ölkədən çıxan TIR-lar üzrə":
        with c2:
            selected_post = st.selectbox("Seçilmiş post",
                                     ['BDT Limanı', 'Qırmızı körpü', 'Astara', 'Biləsuvar', 'Eyvazlı',
                                       'Samur', 'Şahtaxtı və ya Culfa', 'Mazımçay', 'Şirvanlı', 'Xanoba', 'Sədərək'],
                                     0, key='selected_post')
    with c3:
        indicator = st.selectbox('Seçilmiş göstərici', ["Çəki (min ton)", "TİR-ların sayı"], 0)

    st.write(f'### {selected_post}')
    figure_trend_posts = trend_figure_acording_to_post_in_out_flow_count_or_weight(selected_post, selected_flow, indicator)
    st.plotly_chart(figure_trend_posts, use_container_width=True)



