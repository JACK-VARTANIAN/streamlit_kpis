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
import streamlit_authenticator as stauth
import bcrypt
import random

st.set_page_config(
    page_title="Jack Vartanian - KPIs",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed",
)

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# #criar variável com 6 números aleatórios
# digits = random.sample(range(10), 6)

# # Sort the digits in ascending order
# digits.sort()

# # Convert the list of digits into a single integer
# final_senha = int(''.join(map(str, digits)))


# hashed_passwords = fun.hash_passwords([str(final_senha)])


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
    cod_vendedora = config['credentials']['usernames'][username]['cod']
    nome_vendor = config['credentials']['usernames'][username]['name']
    foto_consultora = config['credentials']['usernames'][username]['foto']
    authenticator.logout('Logout', 'sidebar')
    
    vendas = fun.vendas_capta()
    metas = fun.metas()
    
    st.sidebar.image(foto_consultora, width=150)

    st.markdown(f'<h3 class="title-spacing">Olá, {nome_vendor}</h3>', unsafe_allow_html=True)
    st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)
    
    st.sidebar.divider()
    st.sidebar.write('Selecione o período desejado')
    start_date = st.sidebar.date_input('Data Inicial', datetime.date.today().replace(day=1))
    start_date_y = start_date - relativedelta(years=1)

    end_date = st.sidebar.date_input('Data Final', max_value=datetime.date.today())
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
    
    meta_da_consultora = fun.meta_consultora(cod_vendedora, year_month)
    
    
    vendas_igu = vendas_a[vendas_a['Empresa'] == 'IGU']
    vendas_bel = vendas_a[vendas_a['Empresa'] == 'BEL']
    vendas_web = vendas_a[vendas_a['Empresa'] == 'WEB']
    vendas_bat = vendas_a[vendas_a['Empresa'] == 'BAT']
    
    vendas_da_consultora = fun.vendas_consultora(start_date, end_date, cod_vendedora)
    vendas_da_consultora_y = fun.vendas_consultora_y(start_date_y, end_date_y, cod_vendedora)
    
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
    
    tkts_a = np.unique(vendas_da_consultora['ID_Venda'])
    Qtd_tkts = len(tkts_a)
    
    tkts_y = np.unique(vendas_da_consultora_y['ID_Venda'])
    Qtd_tkts_y = len(tkts_y)
    
    totalLiq = int(np.sum(vendas_da_consultora['Total Liq.']))
    totalLiq_y = int(np.sum(vendas_da_consultora_y['Total Liq.']))
    
    meta = int(np.sum( metas_loja['Meta'] ))
    metaDia = int(np.sum( metas_loja['Meta'] ) / month_days )
    
    valorEquilibrio = metaDia * end_date.day
    saldoEquilibrio = totalLiq - valorEquilibrio
    saldoEquilibrioTotal = (totalLiq - valorEquilibrio)
    
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
    
    total_liq_consultora = fun.totalLiq_a(vendas_da_consultora)
    total_liq_consultora_y = fun.totalLiq_y(vendas_da_consultora_y)
    
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
    
    metas_da_consultora = fun.meta_a(meta_da_consultora)
    meta_dia_consultora = fun.meta_dia(metas_da_consultora, month_days)
    saldo_meta_da_consultora = fun.saldoMeta(metas_da_consultora, total_liq_consultora)
    perc_meta_da_consultora = fun.percMeta(total_liq_consultora, metas_da_consultora)

    
    valorEquilibrio_igu = fun.valorEquilibrio(meta_dia_igu, end_date.day)
    saldoEquilibrio_igu = fun.saldoEquilibrio(total_liq_igu, valorEquilibrio_igu)
    totalSaldo_igu = fun.totalSaldo(total_liq_igu, valorEquilibrio_igu)
    
    valorEquilibrio_consultora = fun.valorEquilibrio(meta_dia_consultora, end_date.day)
    saldoEquilibrio_consultora = fun.saldoEquilibrio(total_liq_consultora, valorEquilibrio_consultora)
    totalSaldo_consultora = fun.totalSaldo(total_liq_consultora, valorEquilibrio_consultora)
    perc_equil_meta_da_consultora = fun.percVendaDia(total_liq_consultora, valorEquilibrio_consultora)
    venda_dia_consultora = valorEquilibrio_consultora - total_liq_consultora
    
    yoy_total_igu = fun.yoyTotal(total_liq_igu, total_liq_y_igu)
    yoy_tickets_igu = fun.yoyTickets(qtd_tickets_igu, qtd_tickets_y_igu)
    yoy_tkm_igu = fun.yoyTkm(ticket_medio_igu, ticket_medio_y_igu)
    
    yoy_total_consultora = fun.yoyTotal(total_liq_consultora, total_liq_consultora_y)
    
    if metas_da_consultora < total_liq_consultora:
        st.balloons()
        st.subheader("Parabéns, você atingiu a meta do mês!")
        col1, col2 = st.columns(2)
        with col1: 
            st.metric("Meta do mês", fun.fNumbers(metas_da_consultora))
            # st.metric("Realizado ", fun.fNumbers(total_liq_consultora), fun.fPerc(perc_equil_meta_da_consultora))
        with col2:
            st.metric("Realizado ", fun.fNumbers(total_liq_consultora))
        
        ch.gauge(meta_da_consultora, total_liq_consultora, valorEquilibrio_consultora)

    else:
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Meta do mês", fun.fNumbers(metas_da_consultora))
            st.metric("Realizado ", fun.fNumbers(total_liq_consultora), fun.fPerc(perc_equil_meta_da_consultora))
        with col2:
            st.metric("Meta do dia", fun.fNumbers(meta_dia_consultora))
            if venda_dia_consultora < 0:
                st.balloons()
                st.subheader("Parabéns, sua meta está em dia!")
            else:
                st.metric("Venda esperada para o dia", fun.fNumbers(venda_dia_consultora))        

        if valorEquilibrio_consultora > total_liq_consultora:
            st.markdown(
            """
            <style>
                .st-emotion-cache-keje6w:first-child .element-container:last-child .st-emotion-cache-1xarl3l{
                    color:red;
                }
            </style>
            """,
            unsafe_allow_html=True
        )
        
        # st.title('Analise as suas :rainbow[Metas:]')
        st.subheader('Acompanhe sua meta: ')
        
        ch.gauge(meta_da_consultora, total_liq_consultora, valorEquilibrio_consultora)

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
