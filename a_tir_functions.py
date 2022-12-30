import pandas as pd
from a_read_db import read_db


def data_for_selected_country(selected_country, previous_year, max_year, selected_month, aggregated_column):
    df = read_db()
    full_previous_year_from = round(df[(df['From'] == selected_country) &
                            (df['Year_x'] == previous_year)][aggregated_column].sum(), 2)
    full_previous_year_to = round(df[(df['To'] == selected_country) &
                            (df['Year_x'] == previous_year)][aggregated_column].sum(), 2)

    previous_year_from = round(df[(df['From'] == selected_country) &
                            (df['Year_x'] == previous_year) &
                            (df['Month_x'] <= selected_month)][aggregated_column].sum(), 2)
    previous_year_to = round(df[(df['To'] == selected_country) &
                            (df['Year_x'] == previous_year) &
                            (df['Month_x'] <= selected_month)][aggregated_column].sum(), 2)

    current_year_from = round(df[(df['From'] == selected_country) &
                            (df['Year_x'] == max_year) &
                            (df['Month_x'] <= selected_month)][aggregated_column].sum(), 2)
    current_year_to = round(df[(df['To'] == selected_country) &
                            (df['Year_x'] == max_year) &
                            (df['Month_x'] <= selected_month)][aggregated_column].sum(), 2)

    sum_full_previous_year = round((full_previous_year_from + full_previous_year_to), 2)
    sum_previous_year = round((previous_year_from + previous_year_to), 2)
    sum_current_year = round((current_year_from + current_year_to), 2)

    if previous_year_from != 0.:
        change_from = round(((current_year_from/previous_year_from)-1)*100, 1)
        change_from_percent = f'{change_from} %'
    elif previous_year_from == 0.0:
        change_from_percent = "-"

    if previous_year_to != 0.:
        change_to = round(((current_year_to/previous_year_to)-1)*100, 1)
        change_to_percent = f'{change_to} %'
    elif previous_year_to != 0.:
        change_to_percent = "-"

    if sum_previous_year != 0.:
        change_sum = round(((sum_current_year/sum_previous_year)-1)*100, 1)
        change_sum_percent = f'{change_sum} %'
    elif sum_previous_year != 0.:
        change_sum_percent = "-"

    tmp = pd.DataFrame()
    tmp[f'{previous_year}'] = [full_previous_year_from, full_previous_year_to, sum_full_previous_year]
    tmp[f'{previous_year}*'] = [previous_year_from, previous_year_to, sum_previous_year]
    tmp[f'{max_year}*'] = [current_year_from, current_year_to, sum_current_year]
    tmp['Dəyişiklik'] = [change_from_percent, change_to_percent, change_sum_percent]

    tmp = tmp.rename(index={0: "Seçilmiş ölkədən",
                            1: "Seçilmiş ölkəyə",
                            2: "Cəmi:"})
    return tmp
