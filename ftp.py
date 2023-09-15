
from ftplib import FTP
import ftplib
from datetime import datetime
import pandas as pd


dados_ativos = pd.read_excel('2023_Benac_Fundamentus.xlsx', sheet_name="Planilha1")
nome_ativos = dados_ativos.ativos
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

dados_ativos = str(dados_ativos)
print(dados_ativos)
retorno_ftp = Envio_ftp(dados_ativos)