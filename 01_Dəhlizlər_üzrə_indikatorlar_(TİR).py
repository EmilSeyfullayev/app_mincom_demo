import streamlit as st
from a_read_db import data_for_metrics, max_year_month_pre_year


st.set_page_config(layout='wide', initial_sidebar_state='expanded')

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

data_for_metrics = data_for_metrics()
max_year = max_year_month_pre_year()[0]
max_month = max_year_month_pre_year()[1]

# Row A
# st.markdown('## Dəhlizlər üzrə tranzit yüklərin həcmi, min ton')
st.markdown(f'## Dəhlizlər üzrə cari ilin {max_month} ayı ilə ötən ilin analoji dövrü ilə müqayisəsi, ümumi həcm, min ton ilə')
col1, col2, col3 = st.columns(3)
col1.metric(list(data_for_metrics.keys())[0], data_for_metrics[list(data_for_metrics.keys())[0]][0],
                                              data_for_metrics[list(data_for_metrics.keys())[0]][1])

col2.metric(list(data_for_metrics.keys())[1], data_for_metrics[list(data_for_metrics.keys())[1]][0],
                                              data_for_metrics[list(data_for_metrics.keys())[1]][1])

col3.metric(list(data_for_metrics.keys())[2], data_for_metrics[list(data_for_metrics.keys())[2]][0],
                                              data_for_metrics[list(data_for_metrics.keys())[2]][1])

# st.markdown('### Dəhlizlər üzrə indikatorlar')
col1, col2, col3 = st.columns(3)
col1.metric(list(data_for_metrics.keys())[3], data_for_metrics[list(data_for_metrics.keys())[3]][0],
                                              data_for_metrics[list(data_for_metrics.keys())[3]][1])

col2.metric(list(data_for_metrics.keys())[4], data_for_metrics[list(data_for_metrics.keys())[4]][0],
                                              data_for_metrics[list(data_for_metrics.keys())[4]][1])

col3.metric(list(data_for_metrics.keys())[5], data_for_metrics[list(data_for_metrics.keys())[5]][0],
                                              data_for_metrics[list(data_for_metrics.keys())[5]][1])


col1, col2, col3 = st.columns(3)
col1.metric(list(data_for_metrics.keys())[6], data_for_metrics[list(data_for_metrics.keys())[6]][0],
                                              data_for_metrics[list(data_for_metrics.keys())[6]][1])

col2.metric(list(data_for_metrics.keys())[7], data_for_metrics[list(data_for_metrics.keys())[7]][0],
                                              data_for_metrics[list(data_for_metrics.keys())[7]][1])

col3.metric(list(data_for_metrics.keys())[8], data_for_metrics[list(data_for_metrics.keys())[8]][0],
                                              data_for_metrics[list(data_for_metrics.keys())[8]][1])
