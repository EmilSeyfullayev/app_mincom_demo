import streamlit as st
from tir_data_for_visualisations_of_data_by_country import data_for_sankey, sankey_figure_for_tir, \
    trend_figure_acording_to_post_in_out_flow_count_or_weight
from tir_map_functions import map_plot, return_df, data_for_map_plot

# st.set_page_config(layout="wide")
st.markdown("<h6 style='text-align: right; color: #075586;'>©Nəqliyyat siyasəti şöbəsi - Tranzit yükdaşımalar</h6>",
        unsafe_allow_html=True)
df = data_for_sankey()
db = return_df()

tab1, tab2, tab3 = st.tabs(["Xəritədə postlar üzrə göstəricilər", 'Ərazi və postlar üzrə', 'Postların trend təsviri'])


with tab1:
    c1, c2, c3, c4 = st.columns((1, 2, 1, 1))
    with st.form("my_form"):
        with c1:
            selected_category = st.selectbox('Kateqoriya üzrə', ["Ölkəyə daxilolma postu", "Ölkədən xaricolma postu"],
                                             0)
        with c2:
            selected_value = st.selectbox('Aqreqat olunmuş dəyər', ['Çəki (min tonla)', "TIR sayı",
                                                                    "Ölkəyə daxiloduqda ödənilən məbləğ (ABŞ dolları)"],
                                          0)
        with c3:
            selected_year = st.selectbox('Seçilmiş il', options=sorted(db['Year_x'].unique().tolist()), index=0)
        with c4:
            list_of_monthes = sorted(db[db['Year_x'] == selected_year]['Month_x'].unique().tolist())
            selected_max_month = st.selectbox('İlk neçə ay?',
                                              options=list_of_monthes,
                                              index=list_of_monthes.index(max(list_of_monthes)))

        # Every form must have a submit button.
        submitted = st.form_submit_button("Xəritədə göstər")
        if submitted:
            final_df = data_for_map_plot(selected_category=selected_category, selected_value=selected_value, df=db,
                                         max_year=selected_year,
                                         max_month=selected_max_month,
                                         )
            st.plotly_chart(
                map_plot(final_df=final_df,
                         selected_category=selected_category,
                         selected_value=selected_value),
                use_container_width=True)
with tab2:
    st.write('### Tranzit keçən TİR-ların ərazi və postlar üzrə marşrutu, say ilə')
    c1, c2 = st.columns((1, 3))
    with c1:
        selected_year = st.selectbox('Seçilmiş il',
                                             df['Year_x'].unique().tolist(),
                                             df['Year_x'].unique().tolist().index(df['Year_x'].max()))
    figure_sankey = sankey_figure_for_tir(selected_year)
    st.plotly_chart(figure_sankey, use_container_width=True)
with tab3:
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



