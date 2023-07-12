import sqlite3
import pandas as pd
import streamlit as st


@st.cache(allow_output_mutation=True)
def read_db():
    # connection = sqlite3.connect('data_for_app_2019_2023_May.db')
    # connection = sqlite3.connect('TIR_Data_for_app.db')
    # df = pd.read_sql('''select * from 'table' ''', connection)
    df = pd.read_excel("TIR_2019_2023_June_similar_to_app_data.xlsx", sheet_name='Sheet1')
    df = df[df['CONS_NAME_x'] != 'Digər azad olmalar']
    df = df[df['CUST_NAME_x'].isin(
        ['Qırmızı körpü', 'BDT Limanı', 'Mazımçay', 'Samur', 'Biləsuvar', 'Eyvazlı', 'Sədərək', 'Astara', 'Şirvanlı',
         'Xanoba', 'Culfa', 'Şahtaxtı'])]
    df = df[df['CUST_NAME_y'].isin(
        ['Qırmızı körpü', 'BDT Limanı', 'Mazımçay', 'Samur', 'Biləsuvar', 'Eyvazlı', 'Sədərək', 'Astara', 'Şirvanlı',
         'Xanoba', 'Culfa', 'Şahtaxtı'])]

    # these filters will be removed

    return df


@st.cache()
def country_names():
    return ['Türkiyə', "Gürcüstan", "İran", "Rusiya",
            "Qazaxıstan", "Türkmənistan", "Qırğızıstan", "Çin", "Özbəkistan",
            "Macarıstan", "İtaliya", "Niderland", "Serbiya", "Polşa", "Əfqanıstan"]


@st.cache()
def max_year_month_pre_year():
    df = read_db()
    max_year = int(df['Year_x'].max())
    max_month = int(df[df['Year_x'] == max_year]['Month_x'].max())
    previous_year = max_year-1
    month_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    unique_monthes = [i for i in month_numbers if i <= max_month]
    return [max_year, max_month, previous_year, unique_monthes]


@st.cache()
def data_for_metrics():
    df = read_db()
    max_year = max_year_month_pre_year()[0]
    max_month = max_year_month_pre_year()[1]
    previous_year = max_year_month_pre_year()[2]

    dehlizler = ["Ümumi", 'Şərq-Qərb', 'Şimal-Qərb', 'Şimal-Cənub', 'Şimal-Şərq',
                 'Cənub-Qərb', 'Cənub-Şərq', 'Naxçıvan', 'Eyvazlı']
    metrics_dict = {}

    for dehliz in dehlizler:

        last_year_indicator = df[
                (df['Year_x'] == max_year) &
                (df['Month_x'] <= max_month) &
                (df['Dəhliz (istiqamətsiz)'] == dehliz)
            ]['Weight_K_tons'].sum().round(2)

        previous_year_indicator = df[
            (df['Year_x'] == previous_year) &
            (df['Month_x'] <= max_month) &
            (df['Dəhliz (istiqamətsiz)'] == dehliz)
        ]['Weight_K_tons'].sum().round(2)

        change = str(round((last_year_indicator / previous_year_indicator - 1) * 100, 1)) + " %"

        metrics_dict[dehliz] = [last_year_indicator, change]

    umumi_last_year = df[
                (df['Year_x'] == max_year) &
                (df['Month_x'] <= max_month)
            ]['Weight_K_tons'].sum().round(2)

    umumi_previous_year = df[
                (df['Year_x'] == previous_year) &
                (df['Month_x'] <= max_month)
            ]['Weight_K_tons'].sum().round(2)

    umumi_change = str(round((umumi_last_year / umumi_previous_year - 1) * 100, 1)) + " %"

    metrics_dict["Ümumi"] = [umumi_last_year, umumi_change]

    return metrics_dict



