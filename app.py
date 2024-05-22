import pandas as pd
import numpy as np
import streamlit as st
from streamlit_authenticator import Authenticate
import yaml
from yaml import SafeLoader
import funcoes as fun
import charts as ch
import datetime
from dateutil.relativedelta import relativedelta
import calendar
import streamlit as st

st.set_page_config(
    page_title="Jack Vartanian - KPIs",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed",
)

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# hashed_passwords = stauth.Hasher(['123', '456']).generate()

with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized'])

#name, authentication_status, username = authenticator.login('Login', 'main')
name, authentication_status, username = authenticator.login('main', fields={'Form name': 'Login'})

if authentication_status:
    st.session_state.setdefault("authentication_status", True)
    
    username = st.session_state["username"]
    role = config['credentials']['usernames'][username]['roles'][0]
    st.session_state["role"] = role
    
    st.sidebar.write(f'Olá, {st.session_state["name"]}')
    authenticator.logout('Logout', 'sidebar')
    
    vendas = fun.vendas_capta()
    metas = fun.metas()
    produtos = fun.produtos()
    produtos_group = produtos[['Metal','Cod. Modelo', 'Cod. Prod.']]
    vendas = vendas.join(produtos_group.set_index('Cod. Prod.'), on='Cod. Prod.')

    # CSS para ajustar o espaço antes do título
    # st.markdown(
    #     """
    #     <style>
    #     .title-spacing {
    #         margin-top: 0px;
    #         margin-bottom: 10px;
    #     }
    #     .custom-divider {
    #         margin-top: -20px; /* Ajuste o valor conforme necessário */
    #         border-top: 2px solid #e0e0e0; /* Estilo do divisor */
    #     }
    #     @media (max-width: 640px){
    #         .st.emotion-cache-keje6w {
    #             min-width: 0px;
    #         }
    #     }
    #     </style>
    #     """,
    #     unsafe_allow_html=True
    # )

    # Aplicando a classe CSS personalizada ao título
    st.markdown('<h3 class="title-spacing">Olá, Aline</h3>', unsafe_allow_html=True)
    st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)
    
    # col1, col2, col3 = st.columns(3)
    # with col1:
    #     with st.expander("Filtros de Data"):
    #         st.sidebar.divider()
    #         st.sidebar.write('Selecione o período desejado')
    #         start_date = st.sidebar.date_input('Data Inicial', datetime.date.today().replace(day=1))
    #         # start_date = st.date_input('Data Inicial', datetime.date.today().replace(day=1))
    #         start_date_y = start_date - relativedelta(years=1)

    #         end_date = st.sidebar.date_input('Data Final', max_value=datetime.date.today())
    #         # end_date = st.date_input('Data Final', max_value=datetime.date.today())
    #         end_date_y = end_date - relativedelta(years=1)
            
    #         month = start_date.month
    #         year = start_date.year
    #         year_y = start_date_y.year
            
    #         month_days = calendar.monthrange(year, month)[1]
    #         days_left = month_days - end_date.day
            
    #         if month < 10:
    #             month = '0' + str(month)
    #         else:
    #             month = str(month)
            
    #         year_month = start_date.strftime('%Y-%m')
    #         year_month_y = start_date_y.strftime('%Y-%m')
            
    st.sidebar.divider()
    st.sidebar.write('Selecione o período desejado')
    start_date = st.sidebar.date_input('Data Inicial', datetime.date.today().replace(day=1))
    # start_date = st.date_input('Data Inicial', datetime.date.today().replace(day=1))
    start_date_y = start_date - relativedelta(years=1)

    end_date = st.sidebar.date_input('Data Final', max_value=datetime.date.today())
    # end_date = st.date_input('Data Final', max_value=datetime.date.today())
    end_date_y = end_date - relativedelta(years=1)
    
    month = start_date.month
    year = start_date.year
    year_y = start_date_y.year
    
    month_days = calendar.monthrange(year, month)[1]
    days_left = month_days - end_date.day
    
    if month < 10:
        month = '0' + str(month)
    else:
        month = str(month)
    
    year_month = start_date.strftime('%Y-%m')
    year_month_y = start_date_y.strftime('%Y-%m')
    
    vendas_a = vendas[vendas['Data'].between(start_date, end_date)]
    vendas_y = vendas[vendas['Data'].between(start_date_y, end_date_y)]

    metas_loja = metas.loc[metas['Ano_Mes'] == year_month]
    metas_consultora = metas.loc[metas['Ano_Mes'] == year_month]
    
    colunas_meta = ['Loja', 'Cod_Vend', 'Meta']
    metas_loja = metas_loja[colunas_meta]
    meta_igu = metas_loja[metas_loja['Loja'] == 'IGU']
    meta_bel = metas_loja[metas_loja['Loja'] == 'BEL']
    meta_web = metas_loja[metas_loja['Loja'] == 'WEB']
    meta_bat = metas_loja[metas_loja['Loja'] == 'BAT']
    
    meta_aline = metas_consultora[metas_consultora['Cod_Vend'] == '0729/2']
    meta_giovana = metas_consultora[metas_consultora['Cod_Vend'] == '0723/5']
    meta_lorena = metas_consultora[metas_consultora['Cod_Vend'] == 'LAMORIM']
    meta_poliane = metas_consultora[metas_consultora['Cod_Vend'] == '0573/7']
    
    vendas_igu = vendas_a[vendas_a['Empresa'] == 'IGU']
    vendas_bel = vendas_a[vendas_a['Empresa'] == 'BEL']
    vendas_web = vendas_a[vendas_a['Empresa'] == 'WEB']
    vendas_bat = vendas_a[vendas_a['Empresa'] == 'BAT']
    
    vendas_aline = vendas_a[vendas_a['Cod. Vend.'] == '0729/2']
    vendas_giovana = vendas_a[vendas_a['Cod. Vend.'] == '0723/5']
    vendas_lorena = vendas_a[vendas_a['Cod. Vend.'] == 'LAMORIM']
    vendas_poliane = vendas_a[vendas_a['Cod. Vend.'] == '0573/7']
    
    
    colunas_vendas = ['Cod. Vend.', 'Consultora', 'Total Liq.']
    vendas_meta_igu = vendas_igu[colunas_vendas]
    vendas_meta_igu = vendas_meta_igu.groupby(['Cod. Vend.', 'Consultora'])['Total Liq.'].sum().reset_index()
    vendas_meta_igu = vendas_meta_igu.join(meta_igu.set_index('Cod_Vend'), on='Cod. Vend.')
    vendas_meta_igu = vendas_meta_igu.drop(columns=['Loja'])
    
    vendas_meta_bel = vendas_bel[colunas_vendas]
    vendas_meta_bel = vendas_meta_bel.groupby(['Cod. Vend.', 'Consultora'])['Total Liq.'].sum().reset_index()
    vendas_meta_bel = vendas_meta_bel.join(meta_igu.set_index('Cod_Vend'), on='Cod. Vend.')
    vendas_meta_bel = vendas_meta_bel.drop(columns=['Loja'])
    
    vendas_meta_web = vendas_web[colunas_vendas]
    vendas_meta_web = vendas_meta_web.groupby(['Cod. Vend.', 'Consultora'])['Total Liq.'].sum().reset_index()
    vendas_meta_web = vendas_meta_web.join(meta_igu.set_index('Cod_Vend'), on='Cod. Vend.')
    vendas_meta_web = vendas_meta_web.drop(columns=['Loja'])
    
    vendas_meta_bat = vendas_bat[colunas_vendas]
    vendas_meta_bat = vendas_meta_bat.groupby(['Cod. Vend.', 'Consultora'])['Total Liq.'].sum().reset_index()
    vendas_meta_bat = vendas_meta_bat.join(meta_igu.set_index('Cod_Vend'), on='Cod. Vend.')
    vendas_meta_bat = vendas_meta_bat.drop(columns=['Loja'])
    
    
    vendas_igu_y = vendas_y[vendas_y['Empresa'] == 'IGU']
    vendas_bel_y = vendas_y[vendas_y['Empresa'] == 'BEL']
    vendas_web_y = vendas_y[vendas_y['Empresa'] == 'WEB']
    vendas_bat_y = vendas_y[vendas_y['Empresa'] == 'BAT']
    
    vendas_aline_y = vendas_y[vendas_y['Cod. Vend.'] == '0729/2']
    vendas_giovana_y = vendas_y[vendas_y['Cod. Vend.'] == '0723/5']
    vendas_lorena_y = vendas_y[vendas_y['Cod. Vend.'] == 'LAMORIM']
    vendas_poliane_y = vendas_y[vendas_y['Cod. Vend.'] == '0573/7']
    
    tkts_a = np.unique(vendas_a['ID_Venda'])
    Qtd_tkts = len(tkts_a)
    
    tkts_y = np.unique(vendas_y['ID_Venda'])
    Qtd_tkts_y = len(tkts_y)
    
    totalLiq = int(np.sum(vendas_a['Total Liq.']))
    totalLiq_y = int(np.sum(vendas_y['Total Liq.']))
    
    meta = int(np.sum( metas_loja['Meta'] ))
    metaDia = int(np.sum( metas_loja['Meta'] ) / month_days )
    
    valorEquilibrio = metaDia * end_date.day
    saldoEquilibrio = totalLiq - valorEquilibrio
    
    total_saldo = ((totalLiq / valorEquilibrio) - 1)
    
    yoy_total = ((totalLiq / totalLiq_y) - 1)
    yoy_tickets = ((Qtd_tkts / Qtd_tkts_y) - 1)
    
    ticket_medio = (totalLiq / Qtd_tkts)
    ticket_medio_y = (totalLiq_y / Qtd_tkts_y)
    
    yoy_tkm = ((ticket_medio / ticket_medio_y) - 1)
    
    saldo_meta = (meta - totalLiq)
    perc_meta = (totalLiq / meta)
    
    mediaDia = totalLiq / end_date.day
    
    mediaDiaDiasRestantes = totalLiq + (mediaDia * days_left)
    
    total_liq_igu = fun.totalLiq_a(vendas_igu)
    total_liq_y_igu = fun.totalLiq_y(vendas_igu_y)
    
    total_liq_aline = fun.totalLiq_a(vendas_aline)
    total_liq_y_aline = fun.totalLiq_y(vendas_aline_y)
    
    total_liq_giovana = fun.totalLiq_a(vendas_giovana)
    total_liq_y_giovana = fun.totalLiq_y(vendas_giovana_y)
    
    total_liq_lorena = fun.totalLiq_a(vendas_lorena)
    total_liq_y_lorena = fun.totalLiq_y(vendas_lorena_y)
    
    total_liq_poliane = fun.totalLiq_a(vendas_poliane)
    total_liq_y_poliane = fun.totalLiq_y(vendas_poliane_y)
    
    qtd_tickets_igu = fun.tickets_a(vendas_igu)
    qtd_tickets_y_igu = fun.tickets_y(vendas_igu_y)
    
    ticket_medio_igu = fun.ticketMedio(total_liq_igu, qtd_tickets_igu)
    ticket_medio_y_igu = fun.ticketMedio_y(total_liq_y_igu, qtd_tickets_y_igu)
    
    mediaDia_igu = fun.mediaDia(total_liq_igu, end_date.day)
    mediaDia_rest_igu = fun.mediaDiaRest(total_liq_igu, mediaDia_igu, days_left)
    
    metas_igu = fun.meta_a(meta_igu)
    meta_dia_igu = fun.meta_dia(metas_igu, month_days)
    saldo_meta_igu = fun.saldoMeta(metas_igu, total_liq_igu)
    perc_meta_igu = fun.percMeta(total_liq_igu, metas_igu)
    
    metas_aline = fun.meta_a(meta_aline)
    meta_dia_aline = fun.meta_dia(metas_aline, month_days)
    saldo_meta_aline = fun.saldoMeta(metas_aline, total_liq_aline)
    perc_meta_aline = fun.percMeta(total_liq_aline, metas_aline)
    
    metas_giovana = fun.meta_a(meta_giovana)
    meta_dia_giovana = fun.meta_dia(metas_giovana, month_days)
    saldo_meta_giovana = fun.saldoMeta(metas_giovana, total_liq_giovana)
    perc_meta_giovana = fun.percMeta(total_liq_giovana, metas_giovana)
    
    metas_lorena = fun.meta_a(meta_lorena)
    meta_dia_lorena = fun.meta_dia(metas_lorena, month_days)
    saldo_meta_lorena = fun.saldoMeta(metas_lorena, total_liq_lorena)
    perc_meta_lorena = fun.percMeta(total_liq_lorena, metas_lorena)
    
    metas_poliane = fun.meta_a(meta_poliane)
    meta_dia_poliane = fun.meta_dia(metas_poliane, month_days)
    saldo_meta_poliane = fun.saldoMeta(metas_poliane, total_liq_poliane)
    perc_meta_poliane = fun.percMeta(total_liq_poliane, metas_poliane)
    
    valorEquilibrio_igu = fun.valorEquilibrio(meta_dia_igu, end_date.day)
    saldoEquilibrio_igu = fun.saldoEquilibrio(total_liq_igu, valorEquilibrio_igu)
    totalSaldo_igu = fun.totalSaldo(total_liq_igu, valorEquilibrio_igu)
    
    valorEquilibrio_aline = fun.valorEquilibrio(meta_dia_aline, end_date.day)
    saldoEquilibrio_aline = fun.saldoEquilibrio(total_liq_aline, valorEquilibrio_aline)
    totalSaldo_aline = fun.totalSaldo(total_liq_aline, valorEquilibrio_aline)
    
    valorEquilibrio_giovana = fun.valorEquilibrio(meta_dia_giovana, end_date.day)
    saldoEquilibrio_giovana = fun.saldoEquilibrio(total_liq_giovana, valorEquilibrio_giovana)
    totalSaldo_giovana = fun.totalSaldo(total_liq_giovana, valorEquilibrio_giovana)
    
    valorEquilibrio_lorena = fun.valorEquilibrio(meta_dia_lorena, end_date.day)
    saldoEquilibrio_lorena = fun.saldoEquilibrio(total_liq_lorena, valorEquilibrio_lorena)
    totalSaldo_lorena = fun.totalSaldo(total_liq_lorena, valorEquilibrio_lorena)
    
    valorEquilibrio_poliane = fun.valorEquilibrio(meta_dia_poliane, end_date.day)
    saldoEquilibrio_poliane = fun.saldoEquilibrio(total_liq_poliane, valorEquilibrio_poliane)
    totalSaldo_poliane = fun.totalSaldo(total_liq_poliane, valorEquilibrio_poliane)
    
    yoy_total_igu = fun.yoyTotal(total_liq_igu, total_liq_y_igu)
    yoy_tickets_igu = fun.yoyTickets(qtd_tickets_igu, qtd_tickets_y_igu)
    yoy_tkm_igu = fun.yoyTkm(ticket_medio_igu, ticket_medio_y_igu)
    
    yoy_total_aline = fun.yoyTotal(total_liq_aline, total_liq_y_aline)
    yoy_total_giovana = fun.yoyTotal(total_liq_giovana, total_liq_y_giovana)
    yoy_total_lorena = fun.yoyTotal(total_liq_lorena, total_liq_y_lorena)
    yoy_total_poliane = fun.yoyTotal(total_liq_poliane, total_liq_y_poliane)
    
    col1, col2 = st.columns(2)
    with col1: 
        st.metric("Realizado " + str(year), fun.fNumbers(total_liq_aline), fun.fPerc(yoy_total_aline))
        st.metric("Saldo Meta", fun.fNumbers(saldo_meta_aline))
    with col2:
        st.metric("Valor Equilibrio", fun.fNumbers(valorEquilibrio_aline), fun.fPerc(totalSaldo_igu))
        st.metric("Meta", fun.fNumbers(meta_aline['Meta']), fun.fPerc(perc_meta_aline))
    
    # st.title('Analise as suas :rainbow[Metas:]')
    st.subheader('Acompanhe sua meta: ')
    
    ch.gauge(meta_aline, total_liq_aline, valorEquilibrio_aline)

    # st.title('')
    # st.title('')
    # st.title('')

elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None: 
    st.info('Digite seu usuario e senha')

# if st.button("Clear All"):
    # Clear values from *all* all in-memory and on-disk data caches:
    # i.e. clear values from both square and cube
    # st.cache_data.clear()
    # st.cache_resource.clear()
