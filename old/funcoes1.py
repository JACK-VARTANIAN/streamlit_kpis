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

@st.cache_data(ttl=60 * 60 * 2, show_spinner=True)
def vendas_capta():
    url = "https://jvphotos.com.br/cms/wp-content/uploads/datasets/vendas_gzip.csv"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:66.0) Gecko/20100101 Firefox/66.0"
    }

    response = requests.get(url, headers=headers)
    df = pd.read_csv(
        io.BytesIO(response.content), sep=";", compression="gzip", low_memory=True
    )

    df["Data"] = pd.to_datetime(df["Data"])
    df["Ano"] = df["Data"].dt.year
    df["Mes"] = df["Data"].dt.month
    df["Ano_Mes"] = df["Data"].dt.strftime("%Y-%m")
    # df['Ano_Mes'] = pd.to_datetime(df['Data'], format='%Y-%m').dt.date
    df["Data"] = df["Data"].dt.date
    colunasInt = ["Qtd", "Total Liq.", "Desconto", "Custo", "Total Brt"]
    colunasStr = ["Cod. Barras", "No.Oper"]
    df[colunasStr] = df[colunasStr].astype("str")
    df["Consultora_Nome"] = df["Consultora"].str.split(" ").str[0]
    df = df[df["Grande Grupo"] != "AD"]
    return df


@st.cache_data(ttl=60 * 60 * 2, show_spinner=True)
def clientes():
    url = "https://jvphotos.com.br/cms/wp-content/uploads/datasets/clientes_gzip.csv"
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


@st.cache_data(ttl=60 * 60 * 2, show_spinner=True)
def clientes_rfv():
    url = "https://jvphotos.com.br/cms/wp-content/uploads/datasets/clientes_rfv_gzip.csv"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:66.0) Gecko/20100101 Firefox/66.0"
    }
    response = requests.get(url, headers=headers)
    df = pd.read_csv(
        io.BytesIO(response.content), sep=";", compression="gzip", low_memory=True)
    
    df.drop(columns=['Proxima Compra', 'Recencia', 'Frequencia', 'Valor'], inplace=True)
    df.fillna(0, inplace=True)

    dateColumns = ['Primeira compra', 'Ultima compra']
    df[dateColumns] = df[dateColumns].apply(pd.to_datetime, format='%Y-%m-%d')

    df['Ano_ultima_compra'] = df['Ultima compra'].dt.year
    df['Mes_ultima_compra'] = df['Ultima compra'].dt.month
    df['Anos_Marca'] = (datetime.now() - df['Primeira compra']).dt.days / 365
    df["Primeira compra"] = df["Primeira compra"].dt.strftime("%Y-%m-%d")
    df["Ultima compra"] = df["Ultima compra"].dt.strftime("%Y-%m-%d")

    intColumns = ['Total liq.', 'Qtd tickets', 'Ticket medio', 'Dias ultima compra', 'Media entre compras', 'Anos_Marca']
    for col in intColumns:
        df[col] = df[col].astype(int)
    
    return df


@st.cache_data(ttl=60 * 60 * 2, show_spinner=True)
def produtos():
    url = "https://jvphotos.com.br/cms/wp-content/uploads/datasets/produtos_gzip.csv"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:66.0) Gecko/20100101 Firefox/66.0"
    }
    response = requests.get(url, headers=headers)
    df = pd.read_csv(
        io.BytesIO(response.content), sep=";", compression="gzip", low_memory=True
    )
    return df


@st.cache_data(ttl=60 * 60 * 2, show_spinner=True)
def eletroformacao():
    url = "https://jvphotos.com.br/cms/wp-content/uploads/datasets/eletroformacao_gzip.csv"
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:66.0) Gecko/20100101 Firefox/66.0"}
    response = requests.get(url, headers=headers)
    df = pd.read_csv(io.BytesIO(response.content), sep=';', compression='gzip', low_memory=False)
    
    produto = produtos()
    
    produtos_eletro = produto.join(df.set_index('cpros'), on='Cod. Prod.', how='inner')
    
    return produtos_eletro


@st.cache_data(ttl=60 * 60 * 2, show_spinner=True)
def estoque_venda():
    url = (
        "https://jvphotos.com.br/cms/wp-content/uploads/datasets/estoque_venda_gzip.csv"
    )
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:66.0) Gecko/20100101 Firefox/66.0"
    }
    response = requests.get(url, headers=headers)
    
    df = pd.read_csv(
        io.BytesIO(response.content), sep=";", compression="gzip", low_memory=True
    )
    df = df.groupby("Cod. Prod.")['Qtd'].sum().reset_index()
    df.rename(columns={"Cod. Prod.": "Cod_Prod", "Qtd": "Estoque"}, inplace=True)
    
    return df


@st.cache_data(ttl=60 * 60 * 2, show_spinner=True)
def metas():
    url = "https://jvphotos.com.br/cms/wp-content/uploads/datasets/METAS.xlsx"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:66.0) Gecko/20100101 Firefox/66.0"
    }
    response = requests.get(url, headers=headers)
    df = pd.read_excel(io.BytesIO(response.content), sheet_name="Metas")
    colunas = ["Loja", "Data", "Cod_Vend", "Consultor", "Meta"]
    df.rename(columns=dict(zip(df.columns, colunas)), inplace=True)
    df.drop(columns=["METAL PROPORCIONAL"], inplace=True)
    df["Meta"] = df["Meta"].astype("int")
    df["Ano_Mes"] = df["Data"].dt.strftime("%Y-%m")
    df["Data"] = pd.to_datetime(df["Data"]).dt.date
    return df


@st.cache_data(ttl=60 * 60 * 2, show_spinner=True)
def producao_iniciada():
    
    url = "https://jvphotos.com.br/cms/wp-content/uploads/datasets/ultima_fase_producao_gzip.csv"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:66.0) Gecko/20100101 Firefox/66.0"
    }
    response = requests.get(url, headers=headers)
    df = pd.read_csv(
        io.BytesIO(response.content), sep=";", compression="gzip", low_memory=True
    )
    df = df[~df['Fase'].str.contains('ENCERRA')]
    df = df[(df['Peso_Fase'] != 10)]
    df = df[df['Fase'] != 'ORDEM DE PRODUÇÃO']
    df['Abertura_Pedido'] = pd.to_datetime(df['Abertura_Pedido'], format='%Y-%m-%d')
    df['Processamento_op'] = pd.to_datetime(df['Processamento_op'], format='%Y-%m-%d')
    df['Data'] = pd.to_datetime(df['Data'], format='%Y-%m-%d')
    df['Ano_Processamento'] = df['Processamento_op'].dt.year
    df = df[df['Ano_Processamento'] > 2021]
    
    df = (
        df.rename(columns={"Qtd": "Producao Iniciada"})
        .groupby(["Cod_Prod"], as_index=False)["Producao Iniciada"]
        .sum())
    
    df = df[df["Producao Iniciada"] > 0].reset_index(drop=True)
    
    return df


@st.cache_data(ttl=60 * 60 * 2, show_spinner=True)
def producao_nao_iniciada():
    url = "https://jvphotos.com.br/cms/wp-content/uploads/datasets/ultima_fase_producao_gzip.csv"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:66.0) Gecko/20100101 Firefox/66.0"
    }
    response = requests.get(url, headers=headers)
    df = pd.read_csv(io.BytesIO(response.content), sep=";", compression="gzip", low_memory=True)
    
    df = df[~df['Fase'].str.contains('ENCERRA')]
    df = df[(df['Peso_Fase'] != 10)]
    df = df[(df["Fase"] == "ORDEM DE PRODUÇÃO")]
    df['Abertura_Pedido'] = pd.to_datetime(df['Abertura_Pedido'], format='%Y-%m-%d')
    df['Processamento_op'] = pd.to_datetime(df['Processamento_op'], format='%Y-%m-%d')
    df['Data'] = pd.to_datetime(df['Data'], format='%Y-%m-%d')
    df['Ano_Processamento'] = df['Processamento_op'].dt.year
    df = df[df['Ano_Processamento'] > 2021]
    
    df = (
        df.rename(columns={"Qtd": "Producao Nao Iniciada"})
        .groupby(["Cod_Prod"], as_index=False)["Producao Nao Iniciada"]
        .sum()
    )
    df = df[df["Producao Nao Iniciada"] > 0].reset_index(drop=True)
    return df


@st.cache_data(ttl=60 * 60 * 2, show_spinner=True)
def fNumbers(valor):
    value = "{:,}".format(int(valor)).replace(",", ".")
    return value


@st.cache_data(ttl=60 * 60 * 2, show_spinner=True)
def fPerc(number):
    value = "{:.0%}".format(number)
    return value


def calcular_reposicao_prata(metal, start_date_12m, start_date_6m, start_date_3m, start_date_2m, start_date_1m, start_date_45d, end_date, year_month):
    
    column_mapping = {
        "Cod. Modelo": "Colecao",
        "Cod. Prod.": "Cod_Prod",
        "Foto": "Foto",
        "Desc. Produto": "Desc_Produto",
        "Pr Venda unit": "Pr Venda",
        "Peso": "Peso",
    }
    
    column_list = list(column_mapping.values())

    produtos_prata = produtos()
    produtos_prata = produtos_prata[produtos_prata["Metal"] == metal]
    produtos_prata = produtos_prata[produtos_prata['STATUS_FINAL'] == 'ATIVO']
    
    
    deletarColuna = ['Estoque', 'Colecao']
    produtos_prata.drop(deletarColuna, axis=1, inplace=True)
    
    eletro = eletroformacao()
    
    produtos_prata = produtos_prata.rename(columns=column_mapping)
    produtos_prata = produtos_prata[~produtos_prata["Cod_Prod"].isin(eletro["Cod. Prod."])]
    
    producao_ini = producao_iniciada()
    producao_nao_ini = producao_nao_iniciada()
    estoque_vendas = estoque_venda()

    vendas = vendas_capta()
    vendas_mm = mediaMovel(vendas, year_month)
        
    vendas_12m = vendas[vendas["Data"].between(start_date_12m, end_date)]
    vendas_12m = vendas_12m[["Cod. Prod.", "Qtd"]].rename(columns={"Cod. Prod.": "Cod_Prod", "Qtd": "Vendas_12m"})
    vendas_12m = vendas_12m.groupby(["Cod_Prod"]).sum().sort_values(by="Vendas_12m", ascending=False).reset_index()

    vendas_6m = vendas[vendas["Data"].between(start_date_6m, end_date)]
    vendas_6m = vendas_6m[["Cod. Prod.", "Qtd"]].rename(columns={"Cod. Prod.": "Cod_Prod", "Qtd": "Vendas_6m"})
    vendas_6m = vendas_6m.groupby(["Cod_Prod"]).sum().sort_values(by="Vendas_6m", ascending=False).reset_index()

    vendas_3m = vendas[vendas["Data"].between(start_date_3m, end_date)]
    vendas_3m = vendas_3m[["Cod. Prod.", "Qtd"]].rename(columns={"Cod. Prod.": "Cod_Prod", "Qtd": "Vendas_3m"})
    vendas_3m = vendas_3m.groupby(["Cod_Prod"]).sum().sort_values(by="Vendas_3m", ascending=False).reset_index()

    vendas_2m = vendas[vendas["Data"].between(start_date_2m, end_date)]
    vendas_2m = vendas_2m[["Cod. Prod.", "Qtd"]].rename(columns={"Cod. Prod.": "Cod_Prod", "Qtd": "Vendas_2m"})
    vendas_2m = vendas_2m.groupby(["Cod_Prod"]).sum().sort_values(by="Vendas_2m", ascending=False).reset_index()

    vendas_1m = vendas[vendas["Data"].between(start_date_1m, end_date)]
    vendas_1m = vendas_1m[["Cod. Prod.", "Qtd"]].rename(columns={"Cod. Prod.": "Cod_Prod", "Qtd": "Vendas_1m"})
    vendas_1m = vendas_1m.groupby(["Cod_Prod"]).sum().sort_values(by="Vendas_1m", ascending=False).reset_index()

    vendas_45d = vendas[vendas["Data"].between(start_date_45d, end_date)]
    vendas_45d = vendas_45d[["Cod. Prod.", "Qtd"]].rename(columns={"Cod. Prod.": "Cod_Prod", "Qtd": "Vendas_45d"})
    vendas_45d = vendas_45d.groupby(["Cod_Prod"]).sum().sort_values(by="Vendas_45d", ascending=False).reset_index()

    reposicao_prata = produtos_prata.join(vendas_12m.set_index("Cod_Prod"), on="Cod_Prod", how="inner").reset_index(drop=True).sort_values(by="Vendas_12m", ascending=False)
    reposicao_prata = reposicao_prata.join(vendas_6m.set_index("Cod_Prod"), on="Cod_Prod", how="left").reset_index(drop=True).sort_values(by="Vendas_6m", ascending=False)
    reposicao_prata = reposicao_prata.join(vendas_3m.set_index("Cod_Prod"), on="Cod_Prod", how="left").reset_index(drop=True)
    reposicao_prata = reposicao_prata.join(vendas_2m.set_index("Cod_Prod"), on="Cod_Prod", how="left").reset_index(drop=True)
    reposicao_prata = reposicao_prata.join(vendas_1m.set_index("Cod_Prod"), on="Cod_Prod", how="left").reset_index(drop=True)
    reposicao_prata = reposicao_prata.join(vendas_45d.set_index("Cod_Prod"), on="Cod_Prod", how="left").reset_index(drop=True)    
    reposicao_prata = reposicao_prata.join(vendas_mm.set_index("Cod_Prod"), on="Cod_Prod", how="left").reset_index(drop=True)
    reposicao_prata = reposicao_prata.join(estoque_vendas.set_index("Cod_Prod"), on="Cod_Prod", how="left", lsuffix='rep', rsuffix='0_').reset_index(drop=True)
    
    reposicao_prata["Estoque"] = reposicao_prata["Estoque"].fillna(0)
    reposicao_prata = reposicao_prata.join(producao_nao_ini.set_index("Cod_Prod"), on="Cod_Prod", how="left").reset_index(drop=True)
    reposicao_prata = reposicao_prata.join(producao_ini.set_index("Cod_Prod"), on="Cod_Prod", how="left").reset_index(drop=True)
    
    estoque = reposicao_prata["Estoque"]
    
    condicoes = [
        estoque <= 0,
        reposicao_prata["Vendas_2m"] > 0,
        reposicao_prata["Vendas_3m"] > 0,
    ]

    valores = [
        0,
        estoque / (reposicao_prata["Vendas_2m"] * 0.5),
        estoque / (reposicao_prata["Vendas_3m"] * (1/3)),
        ]

    reposicao_prata["Cobertura_Meses"] = np.select(condicoes, valores, default=0)

    cobertura_meses = reposicao_prata["Cobertura_Meses"]
    estoque = reposicao_prata["Estoque"]
    
    
    
    condicao_1_sugestao = cobertura_meses >= 2.5
    condicao_2_sugestao = (reposicao_prata['Vendas_2m'] - estoque) > 0
    condicao_3_sugestao = (reposicao_prata['Vendas_3m'] - estoque) > 0
    condicao_4_sugestao = (reposicao_prata['Vendas_6m'] - estoque) > 0
    condicao_5_sugestao = (reposicao_prata['Vendas_2m'] - estoque) == ''
    condicao_6_sugestao = (reposicao_prata['Vendas_3m'] - estoque) == ''
    
    valor_1_sugestao = 0
    valor_2_sugestao = reposicao_prata['Vendas_2m'] - estoque
    valor_3_sugestao = reposicao_prata['Vendas_3m'] - estoque
    valor_4_sugestao = reposicao_prata['Vendas_6m'] - estoque
    valor_5_sugestao = reposicao_prata['Vendas_2m'] - estoque
    valor_6_sugestao = reposicao_prata['Vendas_3m'] - estoque
    
    reposicao_prata['Sugestao_BI'] = (
        where(condicao_1_sugestao, valor_1_sugestao,
        where(condicao_2_sugestao, valor_2_sugestao,
        where(condicao_3_sugestao, valor_3_sugestao,
        where(condicao_4_sugestao, valor_4_sugestao,
        where(condicao_5_sugestao, valor_5_sugestao,
        where(condicao_6_sugestao, valor_6_sugestao, 0)))))))
    
    reposicao_prata['Sugestao_BI'] = (
        where(reposicao_prata['Sugestao_BI'] == 1, 3, reposicao_prata['Sugestao_BI']))
    
    sugestao_bi = reposicao_prata["Sugestao_BI"]
    producao_ini = reposicao_prata["Producao Iniciada"]
    
    # condicao_1 = (cobertura_meses >= 2.5) 
    # condicao_2 = (cobertura_meses >= 2) & (cobertura_meses < 2.5) & (reposicao_prata["Vendas_1m"] > 0) 
    # condicao_3 = (cobertura_meses < 2) & (reposicao_prata["Vendas_2m"] > 0) & (sugestao_bi > producao_ini)
    # condicao_4 = (cobertura_meses < 2) & (reposicao_prata["Vendas_3m"] > 0) & (sugestao_bi > producao_ini)
    # condicao_5 = (estoque <= 2) & (reposicao_prata["Vendas_6m"] >= 4) & (sugestao_bi > producao_ini)
    # condicao_6 = (estoque >= reposicao_prata["Vendas_2m"]) 
    # condicao_7 = (estoque >= reposicao_prata["Vendas_1m"]) & (sugestao_bi > producao_ini)
    # condicao_8 = (estoque >= reposicao_prata["Vendas_6m"])
    # condicao_9 = (estoque > 1) & (reposicao_prata["Vendas_2m"] == "")
    # condicao_10 = (sugestao_bi <= producao_ini)
    
    
    # valor_1 = "OK"
    # valor_2 = "Validar"
    # valor_3 = "Repor"
    # valor_4 = ""
    # valor_5 = "Acompanhar"
    
    # reposicao_prata["O_Que_Fazer"] = (
    #     where(condicao_1, valor_1,
    #     where(condicao_2, valor_2,
    #     where(condicao_3, valor_3,
    #     where(condicao_4, valor_3,
    #     where(condicao_5, valor_3,
    #     where(condicao_6, valor_1,
    #     where(condicao_7, valor_1,
    #     where(condicao_8, valor_1,
    #     where(condicao_10, valor_5,
    #     where(condicao_9, valor_1, valor_4)))))))))))
    
    reposicao_prata['Pedido'] = ''

    return reposicao_prata


def calcular_reposicao_eletro(metal, start_date_12m, start_date_6m, start_date_3m, start_date_2m, start_date_1m, start_date_45d, end_date, year_month):
    
    column_mapping = {
        "Cod. Modelo": "Colecao",
        "Cod. Prod.": "Cod_Prod",
        "Foto": "Foto",
        "Desc. Produto": "Desc_Produto",
        "Pr Venda unit": "Pr Venda",
        "Peso": "Peso",
    }
    
    column_list = list(column_mapping.values())

    produtos_prata = eletroformacao()
    produtos_prata = produtos_prata[produtos_prata["Metal"] == metal]
    produtos_prata = produtos_prata[produtos_prata['STATUS_FINAL'] == 'ATIVO']
    
    deletarColuna = ['Estoque', 'Colecao']
    produtos_prata.drop(deletarColuna, axis=1, inplace=True)
    
    produtos_prata = produtos_prata.rename(columns=column_mapping)
    # produtos_prata = produtos_prata[~produtos_prata["Cod_Prod"].isin(eletro["Cod. Prod."])]
    
    
    
    producao_ini = producao_iniciada()
    producao_nao_ini = producao_nao_iniciada()
    estoque_vendas = estoque_venda()

    vendas = vendas_capta()
    vendas_mm = mediaMovel(vendas, year_month)
        
    vendas_12m = vendas[vendas["Data"].between(start_date_12m, end_date)]
    vendas_12m = vendas_12m[["Cod. Prod.", "Qtd"]].rename(columns={"Cod. Prod.": "Cod_Prod", "Qtd": "Vendas_12m"})
    vendas_12m = vendas_12m.groupby(["Cod_Prod"]).sum().sort_values(by="Vendas_12m", ascending=False).reset_index()

    vendas_6m = vendas[vendas["Data"].between(start_date_6m, end_date)]
    vendas_6m = vendas_6m[["Cod. Prod.", "Qtd"]].rename(columns={"Cod. Prod.": "Cod_Prod", "Qtd": "Vendas_6m"})
    vendas_6m = vendas_6m.groupby(["Cod_Prod"]).sum().sort_values(by="Vendas_6m", ascending=False).reset_index()

    vendas_3m = vendas[vendas["Data"].between(start_date_3m, end_date)]
    vendas_3m = vendas_3m[["Cod. Prod.", "Qtd"]].rename(columns={"Cod. Prod.": "Cod_Prod", "Qtd": "Vendas_3m"})
    vendas_3m = vendas_3m.groupby(["Cod_Prod"]).sum().sort_values(by="Vendas_3m", ascending=False).reset_index()

    vendas_2m = vendas[vendas["Data"].between(start_date_2m, end_date)]
    vendas_2m = vendas_2m[["Cod. Prod.", "Qtd"]].rename(columns={"Cod. Prod.": "Cod_Prod", "Qtd": "Vendas_2m"})
    vendas_2m = vendas_2m.groupby(["Cod_Prod"]).sum().sort_values(by="Vendas_2m", ascending=False).reset_index()

    vendas_1m = vendas[vendas["Data"].between(start_date_1m, end_date)]
    vendas_1m = vendas_1m[["Cod. Prod.", "Qtd"]].rename(columns={"Cod. Prod.": "Cod_Prod", "Qtd": "Vendas_1m"})
    vendas_1m = vendas_1m.groupby(["Cod_Prod"]).sum().sort_values(by="Vendas_1m", ascending=False).reset_index()

    vendas_45d = vendas[vendas["Data"].between(start_date_45d, end_date)]
    vendas_45d = vendas_45d[["Cod. Prod.", "Qtd"]].rename(columns={"Cod. Prod.": "Cod_Prod", "Qtd": "Vendas_45d"})
    vendas_45d = vendas_45d.groupby(["Cod_Prod"]).sum().sort_values(by="Vendas_45d", ascending=False).reset_index()

    reposicao_prata = produtos_prata.join(vendas_12m.set_index("Cod_Prod"), on="Cod_Prod", how="inner").reset_index(drop=True).sort_values(by="Vendas_12m", ascending=False)
    reposicao_prata = reposicao_prata.join(vendas_6m.set_index("Cod_Prod"), on="Cod_Prod", how="left").reset_index(drop=True).sort_values(by="Vendas_6m", ascending=False)
    reposicao_prata = reposicao_prata.join(estoque_vendas.set_index("Cod_Prod"), on="Cod_Prod", how="left").reset_index(drop=True)
    reposicao_prata["Estoque"] = reposicao_prata["Estoque"].fillna(0)
    reposicao_prata = reposicao_prata.join(producao_nao_ini.set_index("Cod_Prod"), on="Cod_Prod", how="left").reset_index(drop=True)
    reposicao_prata = reposicao_prata.join(producao_ini.set_index("Cod_Prod"), on="Cod_Prod", how="left").reset_index(drop=True)
    reposicao_prata = reposicao_prata.join(vendas_mm.set_index("Cod_Prod"), on="Cod_Prod", how="left").reset_index(drop=True)
    reposicao_prata = reposicao_prata.join(vendas_3m.set_index("Cod_Prod"), on="Cod_Prod", how="left").reset_index(drop=True)
    reposicao_prata = reposicao_prata.join(vendas_2m.set_index("Cod_Prod"), on="Cod_Prod", how="left").reset_index(drop=True)
    reposicao_prata = reposicao_prata.join(vendas_1m.set_index("Cod_Prod"), on="Cod_Prod", how="left").reset_index(drop=True)
    reposicao_prata = reposicao_prata.join(vendas_45d.set_index("Cod_Prod"), on="Cod_Prod", how="left").reset_index(drop=True)

    estoque = reposicao_prata["Estoque"]
    
    condicoes = [
        estoque <= 0,
        reposicao_prata["Vendas_3m"] > 0,
        reposicao_prata["Vendas_6m"] > 0
    ]

    valores = [
        0,
        estoque / (reposicao_prata["Vendas_3m"] * (1/3)),
        estoque / (reposicao_prata["Vendas_6m"] * (1/6))
        ]

    reposicao_prata["Cobertura_Meses"] = np.select(condicoes, valores, default=0)

    cobertura_meses = reposicao_prata["Cobertura_Meses"]
    estoque = reposicao_prata["Estoque"]
    
    condicao_1 = cobertura_meses >= 3
    condicao_2 = (cobertura_meses >= 2) & (cobertura_meses < 3) & (reposicao_prata["Vendas_1m"] > 0)
    condicao_3 = (cobertura_meses < 2) & (reposicao_prata["Vendas_2m"] > 0)
    condicao_4 = (cobertura_meses < 2) & (reposicao_prata["Vendas_3m"] > 0)
    condicao_5 = (estoque <= 2) & (reposicao_prata["Vendas_6m"] >= 4)
    condicao_6 = (estoque >= reposicao_prata["Vendas_3m"])
    condicao_7 = (estoque >= reposicao_prata["Vendas_2m"])
    condicao_8 = (estoque >= reposicao_prata["Vendas_1m"])
    condicao_9 = (estoque > 1) & (reposicao_prata["Vendas_1m"] == "")
    
    valor_1 = "OK"
    valor_2 = "Validar"
    valor_3 = "Repor"
    valor_4 = ""
    
    reposicao_prata["O_Que_Fazer"] = (
        where(condicao_1, valor_1,
        where(condicao_2, valor_2,
        where(condicao_3, valor_3,
        where(condicao_4, valor_3,
        where(condicao_5, valor_3,
        where(condicao_6, valor_1,
        where(condicao_7, valor_1,
        where(condicao_8, valor_1,
        where(condicao_9, valor_1, valor_4))))))))))
    
    condicao_1_sugestao = cobertura_meses >= 3
    condicao_2_sugestao = (reposicao_prata['Vendas_2m'] - estoque) > 0
    condicao_3_sugestao = (reposicao_prata['Vendas_3m'] - estoque) > 0
    condicao_4_sugestao = (reposicao_prata['Vendas_6m'] - estoque) > 0
    condicao_5_sugestao = (reposicao_prata['Vendas_2m'] - estoque) == ''
    condicao_6_sugestao = (reposicao_prata['Vendas_3m'] - estoque) == ''
    
    valor_1_sugestao = 0
    valor_2_sugestao = reposicao_prata['Vendas_2m'] - estoque
    valor_3_sugestao = reposicao_prata['Vendas_3m'] - estoque
    valor_4_sugestao = reposicao_prata['Vendas_6m'] - estoque
    valor_5_sugestao = reposicao_prata['Vendas_2m'] - estoque
    valor_6_sugestao = reposicao_prata['Vendas_3m'] - estoque
    
    reposicao_prata['Sugestao_BI'] = (
        where(condicao_1_sugestao, valor_1_sugestao,
        where(condicao_2_sugestao, valor_2_sugestao,
        where(condicao_3_sugestao, valor_3_sugestao,
        where(condicao_4_sugestao, valor_4_sugestao,
        where(condicao_5_sugestao, valor_5_sugestao,
        where(condicao_6_sugestao, valor_6_sugestao, 0 )))))))
    
    reposicao_prata['Sugestao_BI'] = (
        where(reposicao_prata['Sugestao_BI'] == 1, 3, reposicao_prata['Sugestao_BI']))
    
    reposicao_prata['Pedido'] = ''

    return reposicao_prata


def calcular_reposicao_ouro(metal, start_date_12m, start_date_6m, start_date_3m, start_date_2m, start_date_1m, start_date_45d, end_date, year_month):
    
    column_mapping = {
        "Cod. Modelo": "Colecao",
        "Cod. Prod.": "Cod_Prod",
        "Foto": "Foto",
        "Desc. Produto": "Desc_Produto",
        "Pr Venda unit": "Pr Venda",
        "Peso": "Peso",
    }
    
    column_list = list(column_mapping.values())

    produtos_ouro = produtos()
    produtos_ouro = produtos_ouro[produtos_ouro["Metal"] == metal]
    produtos_ouro = produtos_ouro[produtos_ouro['STATUS_FINAL'] == 'ATIVO']
    
    deletarColuna = ['Estoque', 'Colecao']
    produtos_ouro.drop(deletarColuna, axis=1, inplace=True)
    
    eletro = eletroformacao()
    
    produtos_ouro = produtos_ouro.rename(columns=column_mapping)
    produtos_ouro = produtos_ouro[~produtos_ouro["Cod_Prod"].isin(eletro["Cod. Prod."])]
    
    producao_ini = producao_iniciada()
    producao_nao_ini = producao_nao_iniciada()
    estoque_vendas = estoque_venda()

    vendas = vendas_capta()
    vendas_mm = mediaMovel(vendas, year_month)
        
    vendas_12m = vendas[vendas["Data"].between(start_date_12m, end_date)]
    vendas_12m = vendas_12m[["Cod. Prod.", "Qtd"]].rename(columns={"Cod. Prod.": "Cod_Prod", "Qtd": "Vendas_12m"})
    vendas_12m = vendas_12m.groupby(["Cod_Prod"]).sum().sort_values(by="Vendas_12m", ascending=False).reset_index()

    vendas_6m = vendas[vendas["Data"].between(start_date_6m, end_date)]
    vendas_6m = vendas_6m[["Cod. Prod.", "Qtd"]].rename(columns={"Cod. Prod.": "Cod_Prod", "Qtd": "Vendas_6m"})
    vendas_6m = vendas_6m.groupby(["Cod_Prod"]).sum().sort_values(by="Vendas_6m", ascending=False).reset_index()

    vendas_3m = vendas[vendas["Data"].between(start_date_3m, end_date)]
    vendas_3m = vendas_3m[["Cod. Prod.", "Qtd"]].rename(columns={"Cod. Prod.": "Cod_Prod", "Qtd": "Vendas_3m"})
    vendas_3m = vendas_3m.groupby(["Cod_Prod"]).sum().sort_values(by="Vendas_3m", ascending=False).reset_index()

    vendas_2m = vendas[vendas["Data"].between(start_date_2m, end_date)]
    vendas_2m = vendas_2m[["Cod. Prod.", "Qtd"]].rename(columns={"Cod. Prod.": "Cod_Prod", "Qtd": "Vendas_2m"})
    vendas_2m = vendas_2m.groupby(["Cod_Prod"]).sum().sort_values(by="Vendas_2m", ascending=False).reset_index()

    vendas_1m = vendas[vendas["Data"].between(start_date_1m, end_date)]
    vendas_1m = vendas_1m[["Cod. Prod.", "Qtd"]].rename(columns={"Cod. Prod.": "Cod_Prod", "Qtd": "Vendas_1m"})
    vendas_1m = vendas_1m.groupby(["Cod_Prod"]).sum().sort_values(by="Vendas_1m", ascending=False).reset_index()

    vendas_45d = vendas[vendas["Data"].between(start_date_45d, end_date)]
    vendas_45d = vendas_45d[["Cod. Prod.", "Qtd"]].rename(columns={"Cod. Prod.": "Cod_Prod", "Qtd": "Vendas_45d"})
    vendas_45d = vendas_45d.groupby(["Cod_Prod"]).sum().sort_values(by="Vendas_45d", ascending=False).reset_index()

    reposicao_ouro = produtos_ouro.join(vendas_12m.set_index("Cod_Prod"), on="Cod_Prod", how="inner").reset_index(drop=True).sort_values(by="Vendas_12m", ascending=False)
    reposicao_ouro = reposicao_ouro.join(vendas_6m.set_index("Cod_Prod"), on="Cod_Prod", how="left").reset_index(drop=True).sort_values(by="Vendas_6m", ascending=False)
    reposicao_ouro = reposicao_ouro.join(estoque_vendas.set_index("Cod_Prod"), on="Cod_Prod", how="left").reset_index(drop=True)
    reposicao_ouro["Estoque"] = reposicao_ouro["Estoque"].fillna(0)
    reposicao_ouro = reposicao_ouro.join(producao_nao_ini.set_index("Cod_Prod"), on="Cod_Prod", how="left").reset_index(drop=True)
    reposicao_ouro = reposicao_ouro.join(producao_ini.set_index("Cod_Prod"), on="Cod_Prod", how="left").reset_index(drop=True)
    reposicao_ouro = reposicao_ouro.join(vendas_mm.set_index("Cod_Prod"), on="Cod_Prod", how="left").reset_index(drop=True)
    reposicao_ouro = reposicao_ouro.join(vendas_3m.set_index("Cod_Prod"), on="Cod_Prod", how="left").reset_index(drop=True)
    reposicao_ouro = reposicao_ouro.join(vendas_2m.set_index("Cod_Prod"), on="Cod_Prod", how="left").reset_index(drop=True)
    reposicao_ouro = reposicao_ouro.join(vendas_1m.set_index("Cod_Prod"), on="Cod_Prod", how="left").reset_index(drop=True)
    reposicao_ouro = reposicao_ouro.join(vendas_45d.set_index("Cod_Prod"), on="Cod_Prod", how="left").reset_index(drop=True)

    estoque = reposicao_ouro["Estoque"]
    
    condicoes = [
        estoque <= 0,
        reposicao_ouro["Vendas_45d"] > 0,
        reposicao_ouro["Vendas_2m"] > 0,
        reposicao_ouro["Vendas_3m"] > 0,
        reposicao_ouro["Vendas_6m"] > 0,
    ]

    valores = [
        0,
        estoque / (reposicao_ouro["Vendas_45d"] / 1.5),
        estoque / (reposicao_ouro["Vendas_2m"] / 2),
        estoque / (reposicao_ouro["Vendas_3m"] / 3),
        estoque / (reposicao_ouro["Vendas_6m"] / 6),
        ]

    reposicao_ouro["Cobertura_Meses"] = np.select(condicoes, valores, default=0)

    cobertura_meses = reposicao_ouro["Cobertura_Meses"]
    estoque = reposicao_ouro["Estoque"]
    
    condicao_1 = cobertura_meses >= 2
    condicao_2 = (cobertura_meses > 1) & (cobertura_meses < 2)
    condicao_3 = (cobertura_meses <= 1) & (reposicao_ouro["Vendas_45d"] > 0)
    condicao_4 = (cobertura_meses <= 1) & (reposicao_ouro["Vendas_2m"] > 0)
    condicao_5 = (cobertura_meses <= 1) & (reposicao_ouro["Vendas_3m"] > 0)
    condicao_6 = (estoque >= reposicao_ouro["Vendas_45d"])
    condicao_7 = (estoque >= reposicao_ouro["Vendas_2m"])
    condicao_8 = (estoque >= reposicao_ouro["Vendas_3m"])
    condicao_9 = (estoque > 1) & (reposicao_ouro["Vendas_2m"] == "")
    
    valor_1 = "OK"
    valor_2 = "Validar"
    valor_3 = "Repor"
    valor_4 = ""
    
    reposicao_ouro["O_Que_Fazer"] = (
        where(condicao_1, valor_1,
        where(condicao_2, valor_2,
        where(condicao_3, valor_3,
        where(condicao_4, valor_3,
        where(condicao_5, valor_3,
        where(condicao_6, valor_1,
        where(condicao_7, valor_1,
        where(condicao_8, valor_1,
        where(condicao_9, valor_1, valor_4))))))))))
    
    
    condicao_1_sugestao = cobertura_meses >= 2
    condicao_2_sugestao = (reposicao_ouro['Vendas_45d'] - estoque) > 0
    condicao_3_sugestao = (reposicao_ouro['Vendas_2m'] - estoque) > 0
    condicao_4_sugestao = (reposicao_ouro['Vendas_3m'] - estoque) > 0
    condicao_5_sugestao = (reposicao_ouro['Vendas_45d'] - estoque) == ''
    condicao_6_sugestao = (reposicao_ouro['Vendas_2m'] - estoque) == ''
    
    valor_1_sugestao = 0
    valor_2_sugestao = reposicao_ouro['Vendas_45d'] - estoque
    valor_3_sugestao = reposicao_ouro['Vendas_2m'] - estoque
    valor_4_sugestao = reposicao_ouro['Vendas_3m'] - estoque
    valor_5_sugestao = reposicao_ouro['Vendas_2m'] - estoque
    valor_6_sugestao = reposicao_ouro['Vendas_3m'] - estoque
    
    reposicao_ouro['Sugestao_BI'] = (
        where(condicao_1_sugestao, valor_1_sugestao,
        where(condicao_2_sugestao, valor_2_sugestao,
        where(condicao_3_sugestao, valor_3_sugestao,
        where(condicao_4_sugestao, valor_4_sugestao,
        where(condicao_5_sugestao, valor_5_sugestao,
        where(condicao_6_sugestao, valor_6_sugestao, 0)))))))
    
    reposicao_ouro['Sugestao_BI'] = (
        where(reposicao_ouro['Sugestao_BI'] == 1, 2, reposicao_ouro['Sugestao_BI']))

    reposicao_ouro['Pedido'] = ''
    
    return reposicao_ouro


def table_aggrid_prata(df)  -> AgGrid:
    
    render_image = JsCode(
        """
        function renderImage(params) {
        var img = new Image();
        img.src = params.value;
        img.width = 50;
        img.height = 50;
        return img;
        }
        """
        )
        
    thumbnail_renderer = JsCode("""
        class ThumbnailRenderer {
            init(params) {
            this.eGui = document.createElement('img');
            this.eGui.setAttribute('src', params.value);
            this.eGui.setAttribute('width', '50px');
            this.eGui.setAttribute('height', '50px');
            }
            getGui() {
            return this.eGui;
            }
            }
        """)    
    
    rowstyle_js = JsCode("""
        function(params) {
            if (params.data.Estoque === 1) {
                return {
                    color: 'white',
                    backgroundColor: 'darkred'
                };
            } else {
                return {
                    color: 'white',
                    backgroundColor: 'darkblue'
                };
            }
        }
        """)
    
    cell_style_js = JsCode("""
        function(params) {
        if (params.colDef.field == 'Estoque') {
            if (params.value == 0) {
                return {
                    'fontWeight': 'bold',
                    'backgroundColor': '#c4554d',
                    'color': '#ffffff',
                };
            }

            else if (params.value <= 3) {
                return {
                    'fontWeight': 'bold',
                    
                    'color': 'white',
                };
            }

            else if (params.value <= 99) {
                return {
                    'fontWeight': 'bold',
                    
                    'color': 'white',
                };
            } else {
                return {
                    'fontWeight': 'bold',
                    'color': 'white',
                };
            }
        }
    }""")
    
    oQueFazer_style_js = JsCode("""
        function(params) {
            if (params.colDef.field == 'O_Que_Fazer') {
                if (params.value == 'Repor') {
                    return {
                        'fontWeight': 'bold',
                        'color': '#e03838',
                    };}
                    else if (params.value == 'Validar') {
                        return {
                            'fontWeight': 'bold',
                            'color': '#cadb30',
                        };
                    } else {
                        return {
                            'fontWeight': 'bold',
                            'color': '#4fc94b',
                        };
                }
            }
        }""")
    
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_default_column(
        wrapHeaderText=True,
        autoHeaderHeight=True,
        wrapText=True,
        resizable=True,
        editable=True,
        selectable=False,
        headerClass="text-center",
        cellClass="text-center")

    gb.configure_grid_options(
        domLayout='normal',
        rowHeight=55)

    # gb.configure_pagination(enabled=True, paginationPageSize=5)
    gb.configure_side_bar()
    gb.configure_selection(selection_mode="single", use_checkbox=True)
    grid_options = gb.build()

    grid_options["columnDefs"] = [
        {
            "headerName": "Colecao",
            "field": "Colecao",
            "selection_mode": "single",
            "checkboxSelection": True,
            'useCheckbox': True,
            "width": "100px",
            'headerTooltip': 'Colecao',
        },
        {
            "headerName": "Cod_Prod",
            "field": "Cod_Prod",
            "width": "90px",
            # "checkboxSelection": True,
            # 'useCheckbox': True
        },
        {
            "headerName": "Foto", 
            "field": "Foto",
            "width": "55px",
            "height": "55px",
            "cellRenderer": thumbnail_renderer,
        },
        {
            "headerName": "Desc_Produto",
            "field": "Desc_Produto",
            "width": "100px",
        },
        {
            "headerName": "Pr Venda",
            "field": "Pr Venda",
            "width": "70px",
        },
        {
            "headerName": "Vendas",
            "field": "Vendas_6m",
            "width": "70px",
        },
        {
            "headerName": "Peso",
            "field": "Peso",
            "hide": True,
        },
        {
            "headerName": "Estoque",
            "field": "Estoque",
            "width": "70px",
            "cellStyle": cell_style_js,
        },
        {
            "headerName": "Sugestao BI",
            "field": "Sugestao_BI",
            "width": "80px",
        },
        {
            "headerName": "Pedido",
            "field": "Pedido",
            "width": "60px",
        },
        {
            "headerName": "Producao Nao Iniciada",
            "field": "Producao Nao Iniciada",
            "width": "90px",
        },
        {
            "headerName": "Producao Iniciada",
            "field": "Producao Iniciada",
            "width": "90px",
        },
        {
            "headerName": "Media_Movel",
            "field": "Media_Movel",
            "width": "100px",
            "hide": True,
        },
        {
            "headerName": "Vendas_12m",
            "field": "Vendas_12m",
            "width": "100px",
            "hide": True,
        },
        {
            "headerName": "Vendas_6m",
            "field": "Vendas_6m",
            "width": "100px",
            "hide": True,
        },
        {
            "headerName": "Vendas_3m",
            "field": "Vendas_3m",
            "width": "100px",
            "hide": True,
        },
        {
            "headerName": "Vendas_2m",
            "field": "Vendas_2m",
            "width": "100px",
            "hide": True,
        },
        {
            "headerName": "Vendas_1m",
            "field": "Vendas_1m",
            "width": "100px",
            "hide": True,
        },
        {
            "headerName": "Vendas_45d",
            "field": "Vendas_45d",
            "width": "100px",
            "hide": True,
        },
        {
            "headerName": "Cobertura_Meses",
            "field": "Cobertura_Meses",
            "width": "100px",
            "hide": True,
        },
                {
            "headerName": "O Que Fazer",
            "field": "O_Que_Fazer",
            "width": "90px",
            "cellStyle": oQueFazer_style_js,
        }]

    grid = AgGrid(
        df,
        gridOptions=grid_options,
        allow_unsafe_jscode=True,
        columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS,
        update_mode=GridUpdateMode.FILTERING_CHANGED,
        fit_columns_on_grid_load=True,
        reload_data=True,
        height=450,
        width='100%',
        theme="streamlit",
        key='dataframe'
    )

    return grid


def table_aggrid_eletro(df)  -> AgGrid:
    
    thumbnail_renderer = JsCode("""
        class ThumbnailRenderer {
            init(params) {
            this.eGui = document.createElement('img');
            this.eGui.setAttribute('src', params.value);
            this.eGui.setAttribute('width', '50px');
            this.eGui.setAttribute('height', '50px');
            }
            getGui() {
            return this.eGui;
            }
            }
        """)    
    
    cell_style_js = JsCode("""
        function(params) {
        if (params.colDef.field == 'Estoque') {
            if (params.value == 0) {
                return {
                    'fontWeight': 'bold',
                    'backgroundColor': '#c4554d',
                    'color': '#ffffff',
                };
            }

            else if (params.value <= 3) {
                return {
                    'fontWeight': 'bold',
                    
                    'color': 'white',
                };
            }

            else if (params.value <= 99) {
                return {
                    'fontWeight': 'bold',
                    
                    'color': 'white',
                };
            } else {
                return {
                    'fontWeight': 'bold',
                    'color': 'white',
                };
            }}}""")
    
    oQueFazer_style_js = JsCode("""
        function(params) {
            if (params.colDef.field == 'O_Que_Fazer') {
                if (params.value == 'Repor') {
                    return {
                        'fontWeight': 'bold',
                        'color': '#e03838',
                    };}
                    else if (params.value == 'Validar') {
                        return {
                            'fontWeight': 'bold',
                            'color': '#cadb30',
                        };
                    } else {
                        return {
                            'fontWeight': 'bold',
                            'color': '#4fc94b',
                        };
                }
            }
        }""")
    
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_default_column(
        wrapHeaderText=True,
        autoHeaderHeight=True,
        wrapText=True,
        resizable=True,
        editable=True,
        selectable=False,
        font_size=10,
        headerClass="text-center",
        cellClass="text-center")

    gb.configure_grid_options(
        domLayout='normal',
        rowHeight=55)

    # gb.configure_pagination(enabled=True, paginationPageSize=5)
    gb.configure_side_bar()
    gb.configure_selection(selection_mode="single", use_checkbox=True)
    grid_options = gb.build()

    grid_options["columnDefs"] = [
        {
            "headerName": "Colecao",
            "field": "Colecao",
            "checkboxSelection": True,
            "width": "100px",
        },
        {
            "headerName": "Cod_Prod",
            "field": "Cod_Prod",
            "width": "80px",
        },
        {
            "headerName": "Foto", 
            "field": "Foto",
            "width": "65px",
            "cellRenderer": thumbnail_renderer
        },
        {
            "headerName": "Desc_Produto",
            "field": "Desc_Produto",
            "width": "100px",
        },
        {
            "headerName": "Pr Venda",
            "field": "Pr Venda",
            "width": "70px",
        },
        {
            "headerName": "Vendas",
            "field": "Vendas_12m",
            "width": "70px",
        },
        {
            "headerName": "Peso",
            "field": "Peso",
            "hide": True,
        },
        {
            "headerName": "Estoque",
            "field": "Estoque",
            "width": "70px",
            "cellStyle": cell_style_js,
        },
        {
            "headerName": "Sugestao BI",
            "field": "Sugestao_BI",
            "width": "80px",
        },
        {
            "headerName": "Pedido",
            "field": "Pedido",
            "width": "70px",
        },
        {
            "headerName": "Producao Nao Iniciada",
            "field": "Producao Nao Iniciada",
            "width": "90px",
        },
        {
            "headerName": "Producao Iniciada",
            "field": "Producao Iniciada",
            "width": "90px",
        },
        {
            "headerName": "Media_Movel",
            "field": "Media_Movel",
            "width": "100px",
            "hide": True,
        },
        {
            "headerName": "Vendas_12m",
            "field": "Vendas_12m",
            "width": "100px",
            "hide": True,
        },
        {
            "headerName": "Vendas_6m",
            "field": "Vendas_6m",
            "width": "100px",
            "hide": True,
        },
        {
            "headerName": "Vendas_3m",
            "field": "Vendas_3m",
            "width": "100px",
            "hide": True,
        },
        {
            "headerName": "Vendas_2m",
            "field": "Vendas_2m",
            "width": "100px",
            "hide": True,
        },
        {
            "headerName": "Vendas_1m",
            "field": "Vendas_1m",
            "width": "100px",
            "hide": True,
        },
        {
            "headerName": "Vendas_45d",
            "field": "Vendas_45d",
            "width": "100px",
            "hide": True,
        },
        {
            "headerName": "Cobertura_Meses",
            "field": "Cobertura_Meses",
            "width": "100px",
            "hide": True,
        },
        {
            "headerName": "O Que Fazer",
            "field": "O_Que_Fazer",
            "width": "90px",
            "cellStyle": oQueFazer_style_js,
        },
    ]

    grid = AgGrid(
        df,
        gridOptions=grid_options,
        allow_unsafe_jscode=True,
        columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS,
        update_mode=GridUpdateMode.FILTERING_CHANGED,
        fit_columns_on_grid_load=True,
        reload_data=True,
        height=450,
        width='100%',
        theme="streamlit",
        # key='dataframe'
    )

    return grid


def table_aggrid_ouro(df)  -> AgGrid:
    
    render_image = JsCode(
        """         
        function renderImage(params) {
        var img = new Image();
        img.src = params.value;
        img.width = 50;
        img.height = 50;
        return img;
        }
        """
        )
    
    thumbnail_renderer = JsCode("""
        class ThumbnailRenderer {
            init(params) {
            this.eGui = document.createElement('img');
            this.eGui.setAttribute('src', params.value);
            this.eGui.setAttribute('width', '50px');
            this.eGui.setAttribute('height', '50px');
            }
            getGui() {
            return this.eGui;
            }
            }
        """)    
    
    rowstyle_js = JsCode("""
        function(params) {
            if (params.data.Estoque === 1) {
                return {
                    color: 'white',
                    backgroundColor: 'darkred'
                };
            } else {
                return {
                    color: 'white',
                    backgroundColor: 'darkblue'
                };
            }
        }
        """)
    
    cell_style_js = JsCode("""
        function(params) {
        if (params.colDef.field == 'Estoque') {
            if (params.value == 0) {
                return {
                    'fontWeight': 'bold',
                    'backgroundColor': '#c4554d',
                    'color': '#ffffff',
                };
            }

            else if (params.value <= 3) {
                return {
                    'fontWeight': 'bold',
                    'color': 'white',
                };
            }

            else if (params.value <= 99) {
                return {
                    'fontWeight': 'bold',
                    'color': 'white',
                };
            } else {
                return {
                    'fontWeight': 'bold',
                    'color': 'white',
                };
            }
        }
    }""")
    
    oQueFazer_style_js = JsCode("""
        function(params) {
            if (params.colDef.field == 'O_Que_Fazer') {
                if (params.value == 'Repor') {
                    return {
                        'fontWeight': 'bold',
                        'color': '#e03838',
                    };}
                    else if (params.value == 'Validar') {
                        return {
                            'fontWeight': 'bold',
                            'color': '#cadb30',
                        };
                    } else {
                        return {
                            'fontWeight': 'bold',
                            'color': '#4fc94b',
                        };
                }
            }
        }""")
    
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_default_column(
        wrapHeaderText=True,
        autoHeaderHeight=True,
        wrapText=True,
        resizable=True,
        editable=True,
        # height='55px',
        # filterable=True,
        headerClass="text-center",
        cellClass="text-center")
    
    # gb.configure_pagination()
    # gb.configure_side_bar()
    gb.configure_grid_options(rowHeight=55)
    # gb.configure_column("Pr Venda", type="numericColumn", editable=True)
    # gb.configure_grid_options(**dict(getRowStyle=rowstyle_js))
    # gb.configure_column('Estoque', cellStyle=cell_style_js)
    # gb.configure_column("Foto", cellRenderer=render_image)
    # gb.configure_column("Peso", type="numericColumn", hide=True)
    # gb.configure_column("Cod_Prod", header_name="Cod_Prod")
    gb.configure_selection(selection_mode="single", use_checkbox=True)
    grid_options = gb.build()

    grid_options["columnDefs"] = [
        {
            "headerName": "Colecao",
            "field": "Colecao",
            "checkboxSelection": True,
            "width": "100px",
            'headerTooltip': 'Colecao',
        },
        {
            "headerName": "Cod_Prod",
            "field": "Cod_Prod",
            "width": "90px",
        },
        {
            "headerName": "Foto", 
            "field": "Foto",
            "width": "65px",
            "cellRenderer": thumbnail_renderer
        },
        {
            "headerName": "Desc_Produto",
            "field": "Desc_Produto",
            "width": "100px",
        },
        {
            "headerName": "Pr Venda",
            "field": "Pr Venda",
            "width": "70px",
        },
        {
            "headerName": "Vendas",
            "field": "Vendas_6m",
            "width": "70px",
        },
        {
            "headerName": "Peso",
            "field": "Peso",
            "hide": True,
        },
        {
            "headerName": "Estoque",
            "field": "Estoque",
            "width": "70px",
            "cellStyle": cell_style_js,
        },
        {
            "headerName": "Sugestao BI",
            "field": "Sugestao_BI",
            "width": "80px",
        },
        {
            "headerName": "Pedido",
            "field": "Pedido",
            "width": "70px",
        },
        {
            "headerName": "Producao Nao Iniciada",
            "field": "Producao Nao Iniciada",
            "width": "90px",
        },
        {
            "headerName": "Producao Iniciada",
            "field": "Producao Iniciada",
            "width": "90px",
        },
        {
            "headerName": "Media_Movel",
            "field": "Media_Movel",
            "width": "100px",
            "hide": True,
        },
        {
            "headerName": "Vendas_12m",
            "field": "Vendas_12m",
            "width": "100px",
            "hide": True,
        },
        {
            "headerName": "Vendas_6m",
            "field": "Vendas_6m",
            "width": "100px",
            "hide": True,
        },
        {
            "headerName": "Vendas_3m",
            "field": "Vendas_3m",
            "width": "100px",
            "hide": True,
        },
        {
            "headerName": "Vendas_2m",
            "field": "Vendas_2m",
            "width": "100px",
            "hide": True,
        },
        {
            "headerName": "Vendas_1m",
            "field": "Vendas_1m",
            "width": "100px",
            "hide": True,
        },
        {
            "headerName": "Vendas_45d",
            "field": "Vendas_45d",
            "width": "100px",
            "hide": True,
        },
        {
            "headerName": "Cobertura_Meses",
            "field": "Cobertura_Meses",
            "width": "100px",
            "hide": True,
        },
                {
            "headerName": "O Que Fazer",
            "field": "O_Que_Fazer",
            "width": "90px",
            "cellStyle": oQueFazer_style_js,
        },
    ]

    grid = AgGrid(
        df,
        gridOptions=grid_options,
        allow_unsafe_jscode=True,
        columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS,
        update_mode=GridUpdateMode.VALUE_CHANGED,
        fit_columns_on_grid_load=True,
        # height='500px',
        width="100%",
        theme="streamlit",
    )

    return grid


def table_aggrid_padrao(df)  -> AgGrid:
        
    thumbnail_renderer = JsCode("""
        class ThumbnailRenderer {
            init(params) {
            this.eGui = document.createElement('img');
            this.eGui.setAttribute('src', params.value);
            this.eGui.setAttribute('width', '50px');
            this.eGui.setAttribute('height', '50px');
            }
            getGui() {
            return this.eGui;
            }
            }
        """)    
    
    cell_style_js = JsCode("""
        function(params) {
        if (params.colDef.field == 'Estoque') {
            if (params.value == 0) {
                return {
                    'fontWeight': 'bold',
                    'backgroundColor': '#c4554d',
                    'color': '#ffffff',
                };
            }

            else if (params.value <= 3) {
                return {
                    'fontWeight': 'bold',
                    
                    'color': 'white',
                };
            }

            else if (params.value <= 99) {
                return {
                    'fontWeight': 'bold',
                    
                    'color': 'white',
                };
            } else {
                return {
                    'fontWeight': 'bold',
                    'color': 'white',
                };
            }}}""")
    
    oQueFazer_style_js = JsCode("""
        function(params) {
            if (params.colDef.field == 'O_Que_Fazer') {
                if (params.value == 'Repor') {
                    return {
                        'fontWeight': 'bold',
                        'color': '#e03838',
                    };}
                    else if (params.value == 'Validar') {
                        return {
                            'fontWeight': 'bold',
                            'color': '#cadb30',
                        };}
                    else if (params.value == 'Acompanhar') {
                        return {
                            'fontWeight': 'bold',
                            'color': '#5353ec',
                        };}                    
                    else {
                        return {
                            'fontWeight': 'bold',
                            'color': '#4fc94b',
                        };
                }
            }
        }""")
    
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_default_column(
        wrapHeaderText=True,
        autoHeaderHeight=True,
        wrapText=True,
        resizable=True,
        editable=True,
        selectable=False,
        headerClass="text-center",
        cellClass="text-center")

    gb.configure_grid_options(
        domLayout='normal',
        rowHeight=55)

    # gb.configure_pagination(enabled=True, paginationPageSize=5)
    gb.configure_side_bar()
    gb.configure_selection(selection_mode="single", use_checkbox=True)
    grid_options = gb.build()

    grid_options["columnDefs"] = [
        {
            "headerName": "Colecao",
            "headerClass": "text-center",
            "field": "Colecao",
            "width": "100px",
            },
        {
            "headerName": "Cod_Prod",
            "field": "Cod_Prod",
            "width": "80px",
        },
        {
            "headerName": "Foto", 
            "field": "Foto",
            "width": "65px",
            "height": "65px",
            "cellRenderer": thumbnail_renderer,
        },
        {
            "headerName": "Desc_Produto",
            "field": "Desc_Produto",
            "width": "100px",
        },
        {
            "headerName": "Pr Venda",
            "field": "Pr Venda",
            "width": "70px",
        },
        {
            "headerName": "Vendas",
            "field": "Vendas_6m",
            "width": "70px",
        },
        {
            "headerName": "Peso",
            "field": "Peso",
            "hide": True,
        },
        {
            "headerName": "Estoque",
            "field": "Estoque",
            "width": "70px",
            "cellStyle": cell_style_js,
        },
        {
            "headerName": "Sugestao BI",
            "field": "Sugestao_BI",
            "width": "80px",
        },
        {
            "headerName": "Pedido",
            "headerClass": "text-center",
            "field": "Pedido",
            "width": "65px",
        },
        {
            "headerName": "Producao Nao Iniciada",
            "field": "Producao Nao Iniciada",
            "width": "90px",
        },
        {
            "headerName": "Producao Iniciada",
            "field": "Producao Iniciada",
            "width": "90px",
        },
        {
            "headerName": "Media_Movel",
            "field": "Media_Movel",
            "width": "100px",
            "hide": True,
        },
        {
            "headerName": "Vendas_12m",
            "field": "Vendas_12m",
            "width": "100px",
            "hide": True,
        },
        {
            "headerName": "Vendas_6m",
            "field": "Vendas_6m",
            "width": "100px",
            "hide": True,
        },
        {
            "headerName": "Vendas_3m",
            "field": "Vendas_3m",
            "width": "100px",
            "hide": True,
        },
        {
            "headerName": "Vendas_2m",
            "field": "Vendas_2m",
            "width": "100px",
            "hide": True,
        },
        {
            "headerName": "Vendas_1m",
            "field": "Vendas_1m",
            "width": "100px",
            "hide": True,
        },
        {
            "headerName": "Vendas_45d",
            "field": "Vendas_45d",
            "width": "100px",
            "hide": True,
        },
        {
            "headerName": "Cobertura_Meses",
            "field": "Cobertura_Meses",
            "width": "100px",
            "hide": True,
        },
                {
            "headerName": "O Que Fazer",
            "field": "O_Que_Fazer",
            "width": "80px",
            "cellStyle": oQueFazer_style_js,
        }]

    grid = AgGrid(
        df,
        gridOptions=grid_options,
        allow_unsafe_jscode=True,
        columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS,
        update_mode=GridUpdateMode.FILTERING_CHANGED,
        fit_columns_on_grid_load=True,
        reload_data=True,
        height=450,
        width='100%',
        theme="streamlit",
        # key='dataframe'
    )

    return grid






def table_aggrid(df):
    
    thumbnail_renderer = JsCode("""
        class ThumbnailRenderer {
            init(params) {
            this.eGui = document.createElement('img');
            this.eGui.setAttribute('src', params.value);
            this.eGui.setAttribute('width', '50px');
            this.eGui.setAttribute('height', '50px');
            }
            getGui() {
            return this.eGui;
            }
            }
        """)    
    
    options_builder = GridOptionsBuilder.from_dataframe(df)
    options_builder.configure_pagination()
    options_builder.configure_side_bar()
    # options_builder.configure_grid_options(rowHeight=55)
    options_builder.configure_columns("Desc_Produto", wrapText=True, min_column_width=5)
    options_builder.configure_columns("Desc_Produto", autoHeight=True)
    options_builder.configure_selection(selection_mode="single", use_checkbox=True)
    grid_options = options_builder.build()

    grid = AgGrid(
        df,
        gridOptions=grid_options,
        allow_unsafe_jscode=True,
        editable=True,
        columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS,
        height=500,
        width=500,
        theme="streamlit",
    )

    return grid


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


def mediaDia(totalLiq, end_date):
    mediaDia = totalLiq / end_date
    return mediaDia


def mediaDiaRest(totalLiq, mediaDia, days_left):
    mediaDiaDiasRestantes = totalLiq + (mediaDia * days_left)
    return mediaDiaDiasRestantes


def mediaMovel(df, year_month):
    
    vendas_mm = df.groupby(["Ano_Mes", "Cod. Prod."])["Qtd"].sum().reset_index()
    vendas_mm["Ano_Mes"] = pd.to_datetime(vendas_mm["Ano_Mes"]).dt.strftime("%Y-%m")

    ano_mes_hoje = vendas_mm["Ano_Mes"].max()
    
    vendas_mm["Media_Movel"] = (
        vendas_mm.groupby("Cod. Prod.")["Qtd"]
        .rolling(3)
        .mean()
        .reset_index(0, drop=True)
    )
    vendas_mm["Media_Movel"].fillna(0, inplace=True)
    vendas_mm["Media_Movel"] = (
        vendas_mm["Media_Movel"].astype(int).sort_values(ascending=True)
    )
    vendas_mm = vendas_mm.sort_values(by="Qtd", ascending=False)
    
    ano_mes_3_meses = (
        vendas_mm[vendas_mm["Ano_Mes"] < ano_mes_hoje]
        .sort_values(by="Ano_Mes", ascending=False)["Ano_Mes"]
        .unique()[2]
    )
    
    
    # ano_mes_3_meses = datetime.datetime.strptime(ano_mes_3_meses, "%Y-%m").date()
    
    vendas_mm = vendas_mm[vendas_mm["Ano_Mes"] >= ano_mes_3_meses]
    vendas_mm = vendas_mm[vendas_mm["Ano_Mes"] == year_month]
    vendas_mm = vendas_mm.groupby("Cod. Prod.")["Media_Movel"].mean().reset_index()
    vendas_mm = vendas_mm.rename(columns={"Cod. Prod.": "Cod_Prod"})
    return vendas_mm


def table_with_images(df: pd.DataFrame, url_columns):

    df_ = df.copy()

    # @st.experimental_singleton(show_spinner=True)
    def _path_to_image_html(path):
        return '<img src="' + path + '" width="55" >'

    for column in url_columns:
        df_[column] = df_[column].apply(_path_to_image_html)

    return df_.to_html(escape=False)


def export_excel(df, filename):
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        removeColunas = ['Foto', 'Media_Movel','Vendas_12m', 'Vendas_3m','Vendas_2m','Vendas_1m','Vendas_45d', 'Cobertura_Meses']
        df = df.drop(removeColunas, axis=1)
        df.to_excel(writer, sheet_name='Sheet1', index=False)
        workbook = writer.book
        worksheet = writer.sheets['Sheet1']
        
        reordenarColunas = ['Colecao', 'Cod_Prod', 'Desc_Produto', 'Pr Venda', 'Peso', 'Vendas_6m',
       'Sugestao_BI', 'Pedido', 'Estoque', 'Producao Nao Iniciada', 'Producao Iniciada', 'O_Que_Fazer']
        
        df = df[reordenarColunas]
        
        table_format = workbook.add_format({
            'font_name': 'Calibri',
            'font_size': 11,
            'align': 'center',
            'valign': 'vcenter',
        })
        
        estoque_format = workbook.add_format({'bg_color': '#69ff5e'})
        pedido_format = workbook.add_format({'bg_color': '#fab25f'})
        integer_format = workbook.add_format({'num_format': '0'})
        
        
        for i, col in enumerate(df.columns):
            column_len = df[col].astype(str).map(len).max()
            column_len = max(column_len, len(col))
            worksheet.set_column(i, i, column_len+1, table_format)
            cell_format = workbook.add_format({'align': 'center'})
            worksheet.set_column(i, i, column_len+1, cell_format)
            
        worksheet.set_column('G:G', None, estoque_format)
        worksheet.set_column('K:K', None, pedido_format)
        worksheet.set_column('D:I', None, integer_format)
    
        writer.save()
        
        button = st.download_button(
            label="Download Excel",
            data=buffer,
            file_name=filename+".xlsx",
            mime="application/vnd.ms-excel"
        )
        
    return button


def export_excel_aggrid(df, filename):
        
    buffer = io.BytesIO()
    writer = pd.ExcelWriter(buffer, engine='xlsxwriter')
    
    removeColunas = ['Foto', 'Media_Movel','Vendas_12m', 'Vendas_3m','Vendas_2m','Vendas_1m','Vendas_45d', 'Cobertura_Meses']
    df = df.drop(removeColunas, axis=1)
    
    df['Foto'] = ''
    reordenarColunas = ['Colecao', 'Cod_Prod', 'Foto', 'Desc_Produto', 'Pr Venda', 'Peso', 'Vendas_6m', 'Estoque',
       'Sugestao_BI', 'Pedido',  'Producao Nao Iniciada', 'Producao Iniciada', 'O_Que_Fazer']
    df = df[reordenarColunas]
    
    df = df.rename(columns={'Vendas_6m': 'Vendas'})
    
    qtdLinhas = df.shape[0]+1
    
    df.to_excel(writer, sheet_name='Sheet1', index=False)

    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    worksheet.set_default_row(15)
    worksheet.hide_gridlines(2)
    
    table_format = workbook.add_format({
        'font_name': 'Calibri',
        'font_size': 11,
        'align': 'center',
        'valign': 'vcenter',
        'border': 0
    })

    header_format = workbook.add_format({
        'bold': True,
        'bg_color': 'black',
        'font_color': 'white',
        'align': 'center',
        'valign': 'vcenter',
    })

    header = ['Coleção', 'Cod. Prod', 'Foto', 'Descrição', 'Preço', 'Peso', 'Vendas', 'Estoque',  'Sugestão BI', 'Pedido', 'Produção Não Iniciada', 'Produção Iniciada', 'O Que Fazer']
    
    for col, title in enumerate(header):
        worksheet.write(0, col, title, header_format)
    
    red_format = workbook.add_format({'bg_color': '#f5594e'})
    green_format = workbook.add_format({'bg_color': '#87f569'})
    pedido_format = workbook.add_format({'bg_color': '#f5c37d'})

    worksheet.conditional_format('G2:G'+str(qtdLinhas), {'type': 'cell', 'criteria': 'equal to', 'value': 0, 'format': red_format})
    worksheet.conditional_format('G2:G'+str(qtdLinhas), {'type': 'cell', 'criteria': 'not equal to', 'value': 0, 'format': green_format})
    
    worksheet.conditional_format('I2:I'+str(qtdLinhas), {'type': 'cell', 'criteria': 'not equal to', 'value': 0, 'format': pedido_format})
    worksheet.conditional_format('I2:I'+str(qtdLinhas), {'type': 'blanks', 'format': pedido_format})
    
    worksheet.set_column('I2:I'+str(qtdLinhas), None, workbook.add_format({'num_format': '0'}))
        
    font_format = workbook.add_format({'font_name': 'Calibri', 'font_size': 11})
    worksheet.set_column('A:XFD', None, font_format)
    
    cell_format = workbook.add_format({'align': 'center', 'valign': 'vcenter'})
    worksheet.set_column(0, 99, None, cell_format)
        
    for i, col in enumerate(df.columns):
        column_len = df[col].astype(str).map(len).max()
        column_len = max(column_len, len(col))
        worksheet.set_column(i, i, column_len+1, table_format)
        cell_format = workbook.add_format({'align': 'center', 'valign': 'vcenter'})
        worksheet.set_column(i, i, column_len+1, cell_format)
        
    workbook.close()   

    button = st.download_button(
        label="Download Excel",
        data= buffer,
        file_name=filename+".xlsx",
        mime="application/vnd.ms-excel"
    )
    return button