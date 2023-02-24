import pandas as pd
import numpy as np
import streamlit as st


def pivot_tables_by_country(df, selected_country, selected_years, selected_max_month, type='dehlizle'):
    if type == 'dehlizle':
        df = df[
            (df['Göndərən (az)'] == selected_country) |
            (df['Alan (az)'] == selected_country)
        ]
        index = 'Koridor'
    elif type == 'from':
        df = df[df['Göndərən (az)'] == selected_country]
        index = 'Yük qrupu (ADY)'
    elif type == 'to':
        df = df[df['Alan (az)'] == selected_country]
        index = 'Yük qrupu (ADY)'

    df = df[df['Tarix Hierarchy - İl'].isin(selected_years)]
    df = df[df['Month'] <= selected_max_month]

    pt = pd.pivot_table(
        df,
        index=index,
        values='Həcm',
        columns='Tarix Hierarchy - İl',
        aggfunc='sum'
    )/1000

    try:
        columns = pt.columns.values
        pt = pt.sort_values(columns[-1], ascending=False)
        pt = pt.fillna(0)
    except:
        pt = st.info('Seçilmiş parametrlər üzrə məlumat tapılmadı')

    return pt


