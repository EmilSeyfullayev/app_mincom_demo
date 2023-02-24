import streamlit as st
import pandas as pd
import numpy as np
from ady_1_read_db import read_ady_db, transit_ady_data


@st.cache()
def read_ady_data():
    df = transit_ady_data()
    df['Ay_sirasi'] = pd.to_numeric(df['Month'])
    df['Həcm (min ton)'] = pd.to_numeric(df['Həcm'])
    df['Həcm (min ton)'] = df['Həcm (min ton)']/1000
    df['Tarix Hierarchy - İl'] = pd.to_numeric(df['Tarix Hierarchy - İl'])
    df['Dəhliz'] = df['Koridor']
    # df['Ay_sirasi'] = df['Tarix Hierarchy - Ay']
    # monthes_dict = {1: 'Yanvar', 2: 'Fevral', 3: 'Mart', 4: 'Aprel', 5: "May", 6: "İyun", 7: "İyul", 8: "Avqust",
    #                 9: "Sentyabr", 10: "Oktyabr", 11: "Noyabr", 12: "Dekabr"}
    # for key, value in monthes_dict.items():
    #     df['Ay_sirasi'] = df['Ay_sirasi'].replace(value, key)
    # df['Ay_sirasi'] = pd.to_numeric(df['Ay_sirasi'])
    return df


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


def iller_uzre_pivot_table(selected_country, index, direction='Dövriyyə'):
    df = read_ady_data()
    max_year = df['Tarix Hierarchy - İl'].max()
    previous_year = max_year - 1
    max_month = df[df['Tarix Hierarchy - İl'] == max_year]['Ay_sirasi'].max()
    tmp = df[
        (df['Göndərən (az)'] == selected_country) |
        (df['Alan (az)'] == selected_country)
        ]
    if direction == 'Dövriyyə':
        pass
    elif direction == "Seçilmiş ölkədən":
        tmp = df[df['Göndərən (az)'] == selected_country]
    elif direction == "Seçilmiş ölkəyə":
        tmp = df[df['Alan (az)'] == selected_country]

    try:
        pt1 = pd.pivot_table(
            tmp,
            values='Həcm (min ton)',
            index=index,
            columns='Tarix Hierarchy - İl',
            aggfunc='sum'
        ).sort_values(max_year, ascending=False)

        pt1.columns = pt1.columns.values

        if (pt1.columns.values[-2] == previous_year) & (pt1.columns.values[-1] == max_year):
            pt2 = pd.pivot_table(
                tmp[tmp['Ay_sirasi'] <= max_month],
                values='Həcm (min ton)',
                index=index,
                columns='Tarix Hierarchy - İl',
                aggfunc='sum'
            ).sort_values(max_year, ascending=False)
            pt2.columns = pt2.columns.values
            pt2_column_names = pt2.columns.values
            pt2_modified_column_names = [f'{i}*' for i in pt2_column_names]
            pt2.columns = pt2_modified_column_names
            pt1.loc['Cəmi:'] = pt1.sum()
            pt2.loc['Cəmi:'] = pt2.sum()
            pt1 = round(pt1, 2)
            pt2 = round(pt2, 2)

            pt1 = pt1[[*pt1.columns.values[:-1]]]
            pt2 = pt2[[*pt2.columns.values[-2:]]]

            # pt = pd.merge(pt1, pt2, how='left', on=pt1.index)
            pt = pd.concat([pt1, pt2], axis=1)
            # pt.index = pt.iloc[:, 0]
            pt = pt.iloc[:, 1:]
            pt.index = pt.index.values
            pt['Dəyişiklik'] = round((pt[f'{max_year}*'] / pt[f'{previous_year}*'] - 1) * 100, 1)
            pt = pt.fillna("")
            pt = pt.replace([0, np.inf, -np.inf], "")
            pt['Dəyişiklik'] = pt['Dəyişiklik'].apply(lambda x: f"{x} %" if x != "" else x)
            pt.style.format(precision=2)


    except:
        pt = "Seçilmiş ölkənin məlumatları az olduğu üçün tərtib edilmiş formata uyğun deyil"

    return pt, max_month

#
# def iller_uzre_pivot_table(selected_country, index, direction='Dövriyyə'):
#     df = read_ady_data()
#     max_year = df['Tarix Hierarchy - İl'].max()
#     previous_year = max_year - 1
#     max_month = df[df['Tarix Hierarchy - İl'] == max_year]['Ay_sirasi'].max()
#     tmp = df[
#         (df['Göndərən (az)'] == selected_country) |
#         (df['Alan (az)'] == selected_country)
#         ]
#     if direction == 'Dövriyyə':
#         pass
#     elif direction == "Seçilmiş ölkədən":
#         tmp = df[df['Göndərən (az)'] == selected_country]
#     elif direction == "Seçilmiş ölkəyə":
#         tmp = df[df['Alan (az)'] == selected_country]
#
#     pt1 = pd.pivot_table(
#         tmp,
#         values='Həcm (min ton)',
#         index=index,
#         columns='Tarix Hierarchy - İl',
#         aggfunc='sum'
#     ).sort_values(max_year, ascending=False)
#
#     pt1.columns = pt1.columns.values
#
#     if (pt1.columns.values[-2] == previous_year) & (pt1.columns.values[-1] == max_year):
#         pt2 = pd.pivot_table(
#             tmp[tmp['Ay_sirasi'] <= max_month],
#             values='Həcm (min ton)',
#             index=index,
#             columns='Tarix Hierarchy - İl',
#             aggfunc='sum'
#         ).sort_values(max_year, ascending=False)
#         pt2.columns = pt2.columns.values
#         pt2_column_names = pt2.columns.values
#         pt2_modified_column_names = [f'{i}*' for i in pt2_column_names]
#         pt2.columns = pt2_modified_column_names
#         pt1.loc['Cəmi:'] = pt1.sum()
#         pt2.loc['Cəmi:'] = pt2.sum()
#         pt1 = round(pt1, 2)
#         pt2 = round(pt2, 2)
#     #     print(pt2)
#     #
#         pt1 = pt1[[*pt1.columns.values[:-1]]]
#         pt2 = pt2[[*pt2.columns.values[-2:]]]
#         print(pt1.index)
#         print(pt2.index)
#     #
#         # pt = pd.merge(pt1, pt2, how='left', on=pt1.index)
#         pt = pd.concat([pt1, pt2], axis=1)
#     #     pt.index = pt.iloc[:, 0]
#     #     pt = pt.iloc[:, 1:]
#     #     pt.index = pt.index.values
#     #     pt['Dəyişiklik'] = round((pt[f'{max_year}*'] / pt[f'{previous_year}*'] - 1) * 100, 1)
#     #     pt = pt.fillna("")
#     #     pt = pt.replace([0, np.inf, -np.inf], "")
#     #     pt['Dəyişiklik'] = pt['Dəyişiklik'].apply(lambda x: f"{x} %" if x != "" else x)
#     #     pt.style.format(precision=2)
#     #
#     #     print(pt1)
#
#     return pt
#
#
# print(iller_uzre_pivot_table('Türkiyə', "Dəhliz", "Seçilmiş ölkəyə"))
