import pandas as pd

from ady_1_read_db import read_ady_db, transit_ady_data
import plotly_express as px

df = read_ady_db()
tr = transit_ady_data()


def regime_trend_line(data=df, rejim='Tranzit'):
    f = data[['Tarix', 'Date', 'Həcm', 'Rejim']].groupby(['Tarix', 'Date', 'Rejim']).sum().reset_index()
    f = f.sort_values('Date')
    f['Həcm (min ton)'] = round(f['Həcm']/1000)
    # İdxal  İxrac Daxili
    fig = px.line(f[f['Rejim'] == rejim], x='Tarix', y="Həcm (min ton)", markers=True, line_shape='spline')
    # fig.update_yaxes(showgrid=False)
    fig.update_xaxes(nticks=6, showgrid=False)
    # fig.update_layout({
    #     'plot_bgcolor': 'rgba(0, 0, 0, 0)',
    #     'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    #     })
    fig.update_traces(line_color='#075586', line_width=2)
    return fig


def dehliz_trend_line(data=tr, dehliz='Şimal-Cənub'):
    f = data[['Tarix', 'Date', 'Həcm', 'Koridor']].groupby(['Tarix', 'Date', 'Koridor']).sum().reset_index()
    f = f.sort_values('Date')
    f['Həcm (min ton)'] = round(f['Həcm']/1000)
    fig = px.line(f[f['Koridor'] == dehliz], x='Tarix', y="Həcm (min ton)", markers=True, line_shape='spline')
    fig.update_xaxes(nticks=6, showgrid=False)
    fig.update_traces(line_color='#075586', line_width=2)
    return fig


def olkeler_uzre_trend_line(data=df, selected_country='Türkiyə', regimes=['İdxal', 'İxrac', 'Tranzit dövriyyəsi']):
    idxal = data[
        (data['Rejim'] == 'İdxal') &
        (data['Göndərən (az)'] == selected_country)
        ][['Rejim', 'Göndərən (az)', "Date", 'Tarix', 'Həcm']].groupby(["Date", 'Tarix', 'Rejim']).sum().reset_index()

    ixrac = data[
        (data['Rejim'] == 'İxrac') &
        (data['Alan (az)'] == selected_country)
        ][['Rejim', 'Alan (az)', "Date", 'Tarix', 'Həcm']].groupby(["Date", 'Tarix', 'Rejim']).sum().reset_index()

    tranzit = data[
        (data['Rejim'] == 'Tranzit') &
        ((data['Alan (az)'] == selected_country) | (data['Göndərən (az)'] == selected_country))
        ][['Rejim', 'Göndərən (az)', 'Alan (az)', "Date", 'Tarix', 'Həcm']].groupby(
        ["Date", 'Tarix']).sum().reset_index()
    tranzit['Rejim'] = 'Tranzit dövriyyəsi'

    tranzit_secilmis_olkeden = data[
        (data['Rejim'] == 'Tranzit') &
        (data['Göndərən (az)'] == selected_country)
        ][['Rejim', 'Göndərən (az)', 'Alan (az)', "Date", 'Tarix', 'Həcm']].groupby(
        ["Date", 'Tarix']).sum().reset_index()
    tranzit_secilmis_olkeden['Rejim'] = 'Tranzit (seçilmiş ölkədən)'

    tranzit_secilmis_olkeye = data[
        (data['Rejim'] == 'Tranzit') &
        (data['Alan (az)'] == selected_country)
        ][['Rejim', 'Göndərən (az)', 'Alan (az)', "Date", 'Tarix', 'Həcm']].groupby(
        ["Date", 'Tarix']).sum().reset_index()
    tranzit_secilmis_olkeye['Rejim'] = 'Tranzit (seçilmiş ölkəyə)'

    data_for_line_chart = pd.concat([idxal, ixrac, tranzit, tranzit_secilmis_olkeden, tranzit_secilmis_olkeye])

    data_for_line_chart = data_for_line_chart[data_for_line_chart['Rejim'].isin(regimes)]

    data_for_line_chart["Həcm (min ton)"] = data_for_line_chart['Həcm'].apply(lambda x: round(x / 1000, 1))
    fig = px.line(data_for_line_chart, x="Date", y="Həcm (min ton)", color='Rejim', markers=True, line_shape='spline')
    fig.update_yaxes(showgrid=False)
    # fig.update_xaxes(nticks=6, showgrid=False)
    # fig.update_layout({
    # 'plot_bgcolor': 'rgba(0, 0, 0, 0)',
    # 'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    # })
    fig.update_traces(  # line_color='#075586',
        line_width=2)
    fig

    return fig

