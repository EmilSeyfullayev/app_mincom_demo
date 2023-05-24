import pandas as pd
import numpy as np
import sqlite3
import datetime
import streamlit as st

path = 'ady_For_App_all_regimes_2017_2023_April.db'


@st.cache(allow_output_mutation=True)
def read_ady_db(path_to_db=path):

    con = sqlite3.connect(path_to_db)
    df = pd.read_sql(''' select * from 'table' ''', con)
    try:
        df = df.drop('index', axis=1)
    except KeyError:
        pass

    try:
        df = df.drop('level_0', axis=1)
    except KeyError:
        pass

    monthes = {1: 'Yanvar', 2: 'Fevral', 3: 'Mart', 4: 'Aprel', 5: "May", 6: "İyun", 7: "İyul", 8: "Avqust", 9: "Sentyabr", 10: "Oktyabr", 11: "Noyabr", 12: "Dekabr"}
    df['Month'] = df['Tarix Hierarchy - Ay']
    for key, value in monthes.items():
        df['Month'] = df['Month'].replace(value, key)

    # if [i for i in df['Month'].unique().tolist() if i not in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]] != []:
    #   df = '''Error in df['Month']'''

    # list comprehension creating date
    df['Date'] = [datetime.date(int(df.loc[i, 'Tarix Hierarchy - İl']),
                                  int(df.loc[i, 'Month']),
                                  22)
                                  for i in df.index]
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date')
    df['Tarix Hierarchy - İl'] = df['Tarix Hierarchy - İl'].apply(lambda x: str(x))
    df['Tarix'] = df['Tarix Hierarchy - Ay'] + " " + df['Tarix Hierarchy - İl']

    df['Göndərən (az)'] = df['Göndərən (az)'].replace('Rusiya Federasiyası', "Rusiya")
    df['Alan (az)'] = df['Alan (az)'].replace('Rusiya Federasiyası', "Rusiya")

    return df


@st.cache(allow_output_mutation=True)
def transit_ady_data():
    df = read_ady_db(path)
    return df[df['Rejim'] == 'Tranzit']


@st.cache()
def unique_country_names():
    unique_country_name_list = ['Türkiyə', 'Rusiya', 'Ukrayna',
    'Qazaxıstan', 'Gürcüstan', 'Türkmənistan', 'İran', 'Gürcüstan (tranzit)',
    'Çin', 'Hindistan', 'Amerika Birləşmiş Ştatları', 'Birləşmiş Ərəb Əmirlikləri',
    'Özbəkistan', 'Belarus Respublikasi', 'Almaniya', 'İtaliya', 'Yaponiya', 'İspaniya',
    'Yunanıstan',
    'Tacikistan',
    'Qırğızıstan']
    return unique_country_name_list
