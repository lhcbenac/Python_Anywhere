
from datetime import datetime
from datetime import timedelta
import time
import timedelta
import MetaTrader5 as mt5
import pandas as pd
import mplfinance as mpl
import yfinance as yf
import openpyxl
# Itens para fazer o request dos dados do Mt5
from pandas import DataFrame
import requests


def super_screening(ativos) :

    try:
        url = 'https://www.dadosdemercado.com.br/bolsa/acoes/' + ativos + '/resultados'

        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36"}
        r = requests.get(url, headers=header)
        dados_lucro = pd.read_html(r.text)
        dados_lucro_1 = dados_lucro[0]
        dados_lucro_2 = dados_lucro_1.iloc[10]
        tamanho = len(dados_lucro_2)
        Lucro_Final = dados_lucro_2[tamanho - 4:tamanho]  # informação do lucro

        lucro_2019 = Lucro_Final[0]
        lucro_2020 = Lucro_Final[1]
        lucro_2021 = Lucro_Final[2]
        lucro_2022 = Lucro_Final[3]

        url2 = 'https://www.dadosdemercado.com.br/bolsa/acoes/' + ativos + '/balancos'
        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36"}
        r = requests.get(url2, headers=header)
        dados_caixa = pd.read_html(r.text)
        dados_caixa_1 = dados_caixa[0]
        dados_caixa_2 = dados_caixa_1.iloc[2]
        tamanho_caixa = len(dados_caixa_2)
        Caixa_final = dados_caixa_2[tamanho_caixa - 4:tamanho_caixa]  # informação do lucro

        caixa_2019 = Caixa_final[0]
        caixa_2020 = Caixa_final[1]
        caixa_2021 = Caixa_final[2]
        caixa_2022 = Caixa_final[3]

    except:
        lucro_2019 = 0
        lucro_2022 = 0
        caixa_2019 = 0
        caixa_2022 = 0
        pass


    try:
        nome = ativos + '.SA'
        tick = yf.download(tickers=nome, start="2020-02-10", end="2020-02-11")  # download pre/post market hours data?
        valor_precovid = round(tick.Close[-1], 2)
    except:
        valor_precovid = 0
        pass

    try:
        url = 'http://www.fundamentus.com.br/detalhes.php?papel=' + ativos
        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36"}
        r = requests.get(url, headers=header)
        df = pd.read_html(r.text)

        # Primeiro Bloco de Informações
        df1 = pd.DataFrame(df[1])
        v_firma = df1[1].iloc[0]
        v_mercado = df1[1].iloc[1]
        n_acao = df1[3].iloc[1]

        # Informação do segundo Bloco
        df2 = pd.DataFrame(df[2])
        div_yield = df2[3].iloc[8]
        p_l = int(df2[3].iloc[1]) / 100
        roic = str(df2[5].iloc[7])
    except:
        v_firma = 0
        v_mercado = 0
        n_acao = 0
        div_yield = 0
        p_l = 0
        roic = 0
        pass

    return ativos  , v_firma , v_mercado ,  n_acao , div_yield , p_l , roic , lucro_2019 , lucro_2022 , caixa_2019 , caixa_2022 ,  valor_precovid


col1 = []
col2 = []
col3 = []
col4 = []
col5 = []
col6 = []
col7 = []
col8 = []
col9 = []
col10 = []
col11 = []
col12 = []

dados_ativos = pd.read_excel('2023_Benac_Fundamentus.xlsx', sheet_name="Planilha1")
nome_ativos = dados_ativos.ativos

for i in range(1, len(nome_ativos) - 1):
    saida = pd.DataFrame(super_screening(nome_ativos[i]))
    col1.append(saida[0].iloc[0])
    col2.append(saida[0].iloc[1])
    col3.append(saida[0].iloc[2])
    col4.append(saida[0].iloc[3])
    col5.append(saida[0].iloc[4])
    col6.append(saida[0].iloc[5])
    col7.append(saida[0].iloc[6])
    col8.append(saida[0].iloc[7])
    col9.append(saida[0].iloc[8])
    col10.append(saida[0].iloc[9])
    col11.append(saida[0].iloc[10])
    col12.append(saida[0].iloc[11])
    print( i / len(nome_ativos) )


Dados = pd.DataFrame({  'ativos': col1,
                        'v_firma': col2,
                        'v_mercado': col3,
                        'n_acao': col4,
                        'div_yield': col5,
                        'p_l': col6,
                        'roic': col7,
                        'lucro_2019': col8,
                        'lucro_2022': col9,
                        'caixa_2019': col10,
                        'caixa_2022': col11,
                        'valor_precovid': col12   })

Dados.to_excel('2023_Benac_Fundamentus.xlsx', sheet_name="Planilha1")



from ftplib import FTP
import ftplib


def Envio_ftp(base_screening):
    try:
        # Entrando no Servidor do Site
        f = ftplib.FTP()
        # Fill Required Information

        # FTP server details
        ftp_server_host = 'ftp.localenergia.com.br'
        ftp_username = 'u842337702.localenergia.com.br'
        ftp_password = 'FTP_Local#2022'
        # Remote directory on the FTP server where you want to upload the file
        remote_directory = '/public_html/wp-content/uploads/2023/Arquivos_FTP'
        ftp_server = FTP(ftp_server_host)
        # Log in to the FTP server
        ftp_server.login(user=ftp_username, passwd=ftp_password)
        # Change to the remote directory
        ftp_server.cwd(remote_directory)

        base_screening.to_csv('./Screening_Ativos.csv')
        filename = './Screening_Ativos.csv'

        valor_horario = str(datetime.now())

        valordia = pd.DataFrame({"Horario": valor_horario}, index=[0])
        valordia.to_csv('./horario_Screening.csv')
        file_horario = './horario_Screening.csv'

        with open(filename, "rb") as file:
            # Command for Uploading the file "STOR filename"
            ftp_server.storbinary(f"STOR {filename}", file)

        with open(file_horario, "rb") as file:
            # Command for Uploading the file "STOR filename"
            ftp_server.storbinary(f"STOR {file_horario}", file)

            resultado = "Conexão bem Sucedida com o Servidor"
    except:
        resultado = "Erro de Conexão com o Servidor"

    print(resultado)
    return resultado


retorno_ftp = Envio_ftp(Dados)

