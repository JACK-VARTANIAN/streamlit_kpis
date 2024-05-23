import pandas as pd
import numpy as np
from numpy import where
import io
import datetime
from datetime import datetime
import time
import requests
import streamlit as st
from st_aggrid import AgGrid, JsCode, GridUpdateMode, GridOptionsBuilder, ColumnsAutoSizeMode
from PIL import Image
import xlsxwriter
from xlsxwriter.utility import xl_range, xl_rowcol_to_cell


def vendas_capta():
    url = "https://jackvartanian.net/cms/wp-content/uploads/datasets/vendas_gzip.csv"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:66.0) Gecko/20100101 Firefox/66.0"
    }

    response = requests.get(url, headers=headers)
    df = pd.read_csv(
        io.BytesIO(response.content), sep=";", compression="gzip", low_memory=True
    )

    data = pd.to_datetime(df["Data"])
    df = df.assign(
        Data=data.dt.date,
        Ano=data.dt.year,
        Mes=data.dt.month,
        Ano_Mes=data.dt.strftime("%Y-%m"),
        Consultora_Nome=df["Consultora"].str.split(" ").str[0]
    )

    colunasStr = ["Cod. Barras", "No.Oper"]
    df[colunasStr] = df[colunasStr].astype("str")
    df["Consultora_Nome"] = df["Consultora"].str.split(" ").str[0]
    df = df[df["Grande Grupo"] != "AD"]
    return df


def clientes():
    url = "https://jackvartanian.net/cms/wp-content/uploads/datasets/clientes_gzip.csv"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:66.0) Gecko/20100101 Firefox/66.0"
    }
    response = requests.get(url, headers=headers)
    df = pd.read_csv(
        io.BytesIO(response.content), sep=";", compression="gzip", low_memory=True)
    
    dateColumns = ['Data Nascimento', 'Data Casamento']
    for col in dateColumns:
        df[col] = pd.to_datetime(df[col])
        
    df['Mes_Nascimento'] = df['Data Nascimento'].dt.month
    df['Dia_Nascimento'] = df['Data Nascimento'].dt.day
    
    df['Mes_Casamento'] = df['Data Casamento'].dt.month
    df['Dia_Casamento'] = df['Data Casamento'].dt.day
    
    df.fillna(0, inplace=True)
    
    colunasInt = ['Mes_Nascimento', 'Dia_Nascimento', 'Mes_Casamento', 'Dia_Casamento', 'Idade']
    df[colunasInt] = df[colunasInt].astype(int)
    
    df['Idade'] = where(df['Data Nascimento'] == 0, 0, df['Idade'])
        
    df['Regiao'] = where(df['Regiao'] == 0, 'Nao Informado', df['Regiao'])
    df['Estado'] = where(df['Estado'] == 0, 'Nao Informado', df['Estado'])
    df['Cidade'] = where(df['Cidade'] == 0, 'Nao Informado', df['Cidade'])
    df['Bairro'] = where(df['Bairro'] == 0, 'Nao Informado', df['Bairro'])
    
    df['Consultora'] = where(df['Consultora'] == 0, 'WEB', df['Consultora'])
    
    df["Cidade"] = df["Cidade"].str.normalize("NFKD").str.encode("ascii", errors="ignore").str.decode("utf-8")
    df["Bairro"] = df["Bairro"].str.normalize("NFKD").str.encode("ascii", errors="ignore").str.decode("utf-8")
    
    return df


def produtos():
    url = "https://jackvartanian.net/cms/wp-content/uploads/datasets/produtos_gzip.csv"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:66.0) Gecko/20100101 Firefox/66.0"
    }
    response = requests.get(url, headers=headers)
    df = pd.read_csv(
        io.BytesIO(response.content), sep=";", compression="gzip", low_memory=True
    )
    return df


def metas():
    url = "https://jackvartanian.net/cms/wp-content/uploads/datasets/METAS.xlsx"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:66.0) Gecko/20100101 Firefox/66.0"
    }
    response = requests.get(url, headers=headers)
    df = pd.read_excel(io.BytesIO(response.content), sheet_name="Metas")
    colunas = ["Loja", "Data", "Cod_Vend", "Consultor", "Meta"]
    df.rename(columns=dict(zip(df.columns, colunas)), inplace=True)
    df.drop(columns=["METAL PROPORCIONAL"], inplace=True)
    # df["Meta"] = df["Meta"].astype("int")
    df["Ano_Mes"] = df["Data"].dt.strftime("%Y-%m")
    df["Data"] = pd.to_datetime(df["Data"]).dt.date
    return df


def fNumbers(valor):
    value = "{:,}".format(int(valor)).replace(",", ".")
    return value


def fPerc(number):
    value = "{:.0%}".format(number)
    return value


def tickets_a(df):
    tkts_a = np.unique(df["ID_Venda"])
    return len(tkts_a)


def tickets_y(df):
    tkts_y = np.unique(df["ID_Venda"])
    tkts_y = 0 if tkts_y is None else tkts_y
    return len(tkts_y)


def totalLiq_a(df):
    totalLiq = int(np.sum(df["Total Liq."]))
    return totalLiq


def totalLiq_y(df):
    totalLiq_y = int(np.sum(df["Total Liq."]))
    totalLiq_y = 0 if totalLiq_y is None else totalLiq_y
    return totalLiq_y


def meta_a(df):
    meta = int(np.sum(df["Meta"]))
    return meta


def meta_dia(meta, month_days):
    metaDia = meta / month_days
    return metaDia


def valorEquilibrio(metaDia, end_date):
    valorEquilibrio = metaDia * end_date
    return valorEquilibrio


def saldoEquilibrio(totalLiq, valorEquilibrio):
    saldoEquilibrio = totalLiq - valorEquilibrio
    return saldoEquilibrio


def totalSaldo(totalLiq, valorEquilibrio):
    total_saldo = (totalLiq / valorEquilibrio) - 1
    return total_saldo


def yoyTotal(totalLiq, totalLiq_y):
    if totalLiq_y == 0:
        yoy_total = 0
    else:
        yoy_total = (totalLiq / totalLiq_y) - 1
    return yoy_total


def yoyTickets(Qtd_tkts, Qtd_tkts_y):
    if Qtd_tkts_y == 0:
        yoy_tickets = 0
    else:
        yoy_tickets = (Qtd_tkts / Qtd_tkts_y) - 1
    return yoy_tickets


def ticketMedio(totalLiq, Qtd_tkts):
    if totalLiq == 0:
        ticket_medio = 0
    else:
        ticket_medio = ( totalLiq / Qtd_tkts )
     
    # ticket_medio = totalLiq / Qtd_tkts
    return ticket_medio


def ticketMedio_y(totalLiq_y, Qtd_tkts_y):
    
    if Qtd_tkts_y == 0:
        ticket_medio_y = 0
    else:
        ticket_medio_y = totalLiq_y / Qtd_tkts_y
        
    return ticket_medio_y


def yoyTkm(ticket_medio, ticket_medio_y):
    
    if ticket_medio_y == 0:
        yoy_tkm = 0
    else:
        yoy_tkm = (ticket_medio / ticket_medio_y) - 1
        
        
    return yoy_tkm


def saldoMeta(meta, totalLiq):
    saldo_meta = meta - totalLiq
    return saldo_meta


def percMeta(totalLiq, meta):
    perc_meta = totalLiq / meta
    return perc_meta


def percVendaDia(realizado, valorEquilibrio):
    perc_equilibrio = 100 / valorEquilibrio * realizado
    perc_equilibrio = int(perc_equilibrio)
    perc_equilibrio = 100 - perc_equilibrio
    perc_equilibrio = (perc_equilibrio / 100) * -1
    # value = "{:.0%}".format(perc_equilibrio)
    return perc_equilibrio


def mediaDia(totalLiq, end_date):
    mediaDia = totalLiq / end_date
    return mediaDia


def mediaDiaRest(totalLiq, mediaDia, days_left):
    mediaDiaDiasRestantes = totalLiq + (mediaDia * days_left)
    return mediaDiaDiasRestantes