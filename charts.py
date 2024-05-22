import pandas as pd
import numpy as np
import streamlit as st
# import plotly.express as px
# import plotly.graph_objs as go
from streamlit_echarts import st_echarts
# from streamlit_echarts import st_pyecharts
import streamviz as sv

from warnings import simplefilter
simplefilter(action='ignore', category=FutureWarning)
simplefilter(action='ignore', category=Warning)

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
                    "icon": "path://M12.8,0.7l12,40.1H0.7L12.8,0.7z",
                    # 'icon': 'path://M2.9,0.7L2.9,0.7c1.4,0,2.6,1.2,2.6,2.6v115c0,1.4-1.2,2.6-2.6,2.6l0,0c-1.4,0-2.6-1.2-2.6-2.6V3.3C0.3,1.9,1.4,0.7,2.9,0.7z',
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
                # "radius": '80%',
                # "center": ['50%', '80%'],
                "radius": 150,  # Increase radius of gauge
                "detail": {
                    "width": 40,  # Increase width of detail
                    "height": 14,  # Increase height of detail
                    "fontSize": 14,  # Increase font size of detail
                    "color": "#fff",
                    "backgroundColor": "inherit",
                    "borderRadius": 3,
                    "formatter": "{value}%",  # Change format of detail value
                },
            }
        ]
    }
    
    # st_pyecharts(chart='Pie', height='500px', width='100%')
    st_echarts(options=option, height='300px', key='gauge')

def gauge_streamviz():
    # Create a gauge chart
    gauge_chart = sv.GaugeChart(
        title="Gauge Chart",
        value=0.75,
        min_value=0,
        max_value=1,
        description="This is a gauge chart",
    )
    gauge_chart.show()