import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objs as go
from pyecharts import options as opts
from pyecharts.charts import Gauge
from pyecharts.globals import ThemeType
import random
import time
from pyecharts.render import make_snapshot
from snapshot_selenium import snapshot
import time
from streamlit_echarts import st_echarts
import math
import random
from pyecharts import options as opts
from pyecharts.charts import Gauge
from pyecharts.globals import ThemeType


from warnings import simplefilter
simplefilter(action='ignore', category=FutureWarning)
simplefilter(action='ignore', category=Warning)


def chart_total_loja(df):

    df = df.groupby(['Empresa'])['Total Liq.'].sum().reset_index()
    df = df.sort_values(by=['Total Liq.'], ascending=False)

    x = df['Empresa'].tolist()
    z = df['Total Liq.'].tolist()

    fig = px.bar(df, x=x, y=z, color='Empresa', title='Total Liquido por Loja', 
                        labels={'Total_Liq':'Total Liquido'}, text_auto=',.0f')
    fig.update_xaxes(title=None, showticklabels=True)
    fig.update_yaxes(title=None, tickformat = ',.0f', showticklabels=False)
    fig.update_traces(textfont_size=13, textposition='outside', cliponaxis=False)
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', 
    xaxis_showgrid=False, yaxis_showgrid=False, xaxis_gridcolor='midnightblue', showlegend=False)

    st.plotly_chart(fig, use_container_width=True, config= dict(displayModeBar = False))


def chart_total_mes(df):
    
    # Agrupe os dados por ano e mês
    df_grouped = df.groupby(['Ano', 'Mes']).sum()

    # Crie uma lista com os anos únicos em seus dados
    anos = df['Ano'].unique()

    # Crie uma lista vazia para armazenar os botões de drilldown
    botões = []

    # Crie um loop para iterar sobre os anos únicos em seus dados
    for ano in anos:
        
        # Filtrar o DataFrame pelos dados do ano atual
        df_filtrado = df_grouped.loc[ano]
        
        # Criar um objeto de gráfico de barras para o ano atual
        trace = go.Bar(
            x=df_filtrado.index.get_level_values('Mes'),
            y=df_filtrado['Total Liq.'],
            name=str(ano)
        )
        
        # Adicionar o objeto de gráfico à lista de dados
        botões.append(trace)
        
    # Criar o layout do gráfico
    layout = go.Layout(
        barmode='group',
        updatemenus=[{
            'buttons': [{
                'label': str(ano),
                'method': 'update',
                'args': [{'visible': [ano == t.name for t in botões]}, {'title': 'Ano ' + str(ano)}]
            } for ano in anos],
            'direction': 'down',
            'showactive': True
        }],
        title='Total Liq por Ano e Mes',
        xaxis={'title': 'Ano e Mes'},
        yaxis={'title': 'Total Liq.'}
    )

    # Criar um objeto de figura para o gráfico
    fig = go.Figure(data=botões, layout=layout)

    # Exibir o gráfico
    fig.show()


def chart_total_consultora(df):

    df = df.groupby(['Consultora_Nome'])['Total Liq.'].sum().reset_index()
    df = df.sort_values(by=['Total Liq.'], ascending=False)

    x = df['Consultora_Nome'].tolist()
    z = df['Total Liq.'].tolist()

    fig = px.bar(df, x=x, y=z, color='Consultora_Nome', title='Total Liquido por Consultora', 
                        labels={'Total Liq.':'Total Liquido'}, text_auto=',.0f')
    fig.update_xaxes(title=None, showticklabels=True)
    fig.update_yaxes(title=None, tickformat = ',.0f', showticklabels=False)
    fig.update_traces(textfont_size=13, textposition='outside', cliponaxis=False)
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', 
    xaxis_showgrid=False, yaxis_showgrid=False, xaxis_gridcolor='midnightblue', showlegend=False)

    st.plotly_chart(fig, use_container_width=True, config= dict(displayModeBar = False))


def chart_total_meta_consultora(df):

    df = df.groupby(['Consultora'])[['Total Liq.', 'Meta']].sum().reset_index()
    df = df.sort_values(by=['Total Liq.'], ascending=False)

    fig = px.bar(df, x='Consultora', y=['Total Liq.', 'Meta'], 
                 barmode='group', title='Total Liquido e Meta por Consultora', 
                 labels={'value':'Valor', 'variable':'Tipo', 'Consultora':'Consultora'}, 
                 )
    
    # fig.update_xaxes(title=None, showticklabels=True)
    # fig.update_yaxes(title=None, tickformat=',.0f', showticklabels=True)
    # fig.update_traces(marker_color=['rgb(31, 119, 180)', 'rgb(214, 39, 40)'], textfont_size=13,
    #                   texttemplate='%{text:,.0f}', cliponaxis=False)
    # fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', 
    # xaxis_showgrid=False, yaxis_showgrid=False, xaxis_gridcolor='midnightblue', showlegend=True,
    # legend_title_text='Tipo')
    
    st.plotly_chart(fig, use_container_width=True, config=dict(displayModeBar=False))

def chart_total_colecoes_prata(df, tile):
    
    df = df[df['Metal'] == 'PRATA']
    df = df.groupby(['Cod. Modelo'])['Total Liq.'].sum().sort_values(ascending=False).reset_index()
    df = df.sort_values(by=['Total Liq.'], ascending=False)
    
    df['Cod. Modelo'] = df['Cod. Modelo'].apply(lambda x: x if x in df['Cod. Modelo'].head(10).values else 'Outras')
    x = df['Cod. Modelo'].tolist()
    y = df['Total Liq.'].tolist()

    fig = px.bar(df, x=x, y=y, color='Cod. Modelo', title=tile, 
                hover_data=['Total Liq.'], labels={'Total Liq.':'Total Liquido'}, height=600, text_auto=',.0f' )
    fig.update_traces(textfont_size=13, textposition="outside", cliponaxis=False)
    fig.update_yaxes(title=None, tickformat = ',.0f', showticklabels=False)
    fig.update_xaxes(title=None) 
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', 
    xaxis_showgrid=False, yaxis_showgrid=False, xaxis_gridcolor='midnightblue', showlegend=False)
    st.plotly_chart(fig, use_container_width=True, config= dict(displayModeBar = False))
    
    
def chart_total_colecoes_ouro(df, tile):
    
    df = df[df['Metal'] == 'OURO']
    df = df.groupby(['Cod. Modelo'])['Total Liq.'].sum().sort_values(ascending=False).reset_index()
    df = df.sort_values(by=['Total Liq.'], ascending=False)
    
    df['Cod. Modelo'] = df['Cod. Modelo'].apply(lambda x: x if x in df['Cod. Modelo'].head(10).values else 'Outras')
    x = df['Cod. Modelo'].tolist()
    y = df['Total Liq.'].tolist()

    fig = px.bar(df, x=x, y=y, color='Cod. Modelo', title=tile, 
                hover_data=['Total Liq.'], labels={'Total Liq.':'Total Liquido'}, height=600, text_auto=',.0f' )
    fig.update_traces(textfont_size=13, textposition="outside", cliponaxis=False)
    fig.update_yaxes(title=None, tickformat = ',.0f', showticklabels=False)
    fig.update_xaxes(title=None) 
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', 
    xaxis_showgrid=False, yaxis_showgrid=False, xaxis_gridcolor='midnightblue', showlegend=False)
    st.plotly_chart(fig, use_container_width=True, config= dict(displayModeBar = False))


def gauge(meta_aline, total_liq_aline, valorEquilibrio_aline):
    
    meta_aline['Meta'] = meta_aline['Meta'].astype(int)
    
    gaugeData = [
        {"value": int((100/int(meta_aline['Meta']))*int(total_liq_aline)), "name": "Realizado",     
        'title': {
            'offsetCenter': ['-30%', '80%']},
        'detail': {
            'offsetCenter': ['-30%', '95%']},
        'itemStyle': {
            'color': '#679f5a'
            }
        },

        {"value": int((100/meta_aline['Meta'])*int(valorEquilibrio_aline)), "name": "Esperado",    
        'title': {
            'offsetCenter': ['30%', '80%']},
        'detail': {
            'offsetCenter': ['30%', '95%']},
        'itemStyle': {
            'color': '#FAC858'
            }
        },
    
        # {"value": 50, "name": "Falta",    
        # 'title': {
        #     'offsetCenter': ['40%', '80%']},
        # 'detail': {
        #     'offsetCenter': ['40%', '95%']},
        # 'itemStyle': {
        #     'color': '#FF0000'
        #     }
        # },
    ]

    option = {
        # "backgroundColor": "#fcfafa",
        "series": [
            {
                "type": "gauge",
                'anchor': {
                'show': True,
                'showAbove': True,
                'size': 18,
                'itemStyle': {
                'color': '#FAC858'
                }
            },
                'pointer': {
                    'icon': 'path://M2.9,0.7L2.9,0.7c1.4,0,2.6,1.2,2.6,2.6v115c0,1.4-1.2,2.6-2.6,2.6l0,0c-1.4,0-2.6-1.2-2.6-2.6V3.3C0.3,1.9,1.4,0.7,2.9,0.7z',
                    'width': 8,
                    'length': '75%',
                    'offsetCenter': [0, '8%']
                },
                
                'progress': {
                    'show': True,
                    'overlap': True,
                    'roundCap': True,
                },
                'axisLine': {
                    'roundCap': True
                },
                "data": gaugeData,
                "title": {"fontSize": 15},  # Increase font size of title
                "radius": 180,  # Increase radius of gauge
                "detail": {
                    "width": 40,  # Increase width of detail
                    "height": 14,  # Increase height of detail
                    "fontSize": 14,  # Increase font size of detail
                    "color": "#fff",
                    "backgroundColor": "inherit",
                    # "borderRadius": 3,
                    "formatter": "{value}%",  # Change format of detail value
                },
            }
        ]
    }
    
    st_echarts(options=option, height='500px', renderer='svg', width='100%')

