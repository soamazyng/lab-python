# Importing library
from time import sleep
from datetime import datetime

from bs4 import BeautifulSoup
from zipfile import ZipFile
import os
from os.path import basename
import codecs
import config
import subprocess

print("****************************************")
print("Bem-Vindx")
print("****************************************")

data_hoje = datetime.today().strftime('%d-%m-%Y')

folder_date_today = input("Deseja utilizar a data de hoje na pasta? " + data_hoje + "s ou n: ")

if folder_date_today == 's':
    folder_date = data_hoje
else:
    folder_date = input("Insira a data da pasta exemplo: 20-10-2022: ")

envio_aws = input("Você deseja enviar os arquivos pelo job? s ou n:")
# last = folder_root.rsplit('\\', 1)[-1]
base_caminho_img = "http://cielodigital.com.br/marketing/{}".format(folder_date)
UTF8Writer = codecs.getwriter('utf8')

folder_root = config.baseDirectory + folder_date

print("Pasta base que contém os e-mails: {}".format(print(config.baseDirectory)))

print("Dia dos e-mails que serão finalizados: {}".format(folder_date))

qtde_arquivos_pasta = len(list(os.walk(folder_root)))

for root, dirs, files in os.walk(folder_root, topdown=False):

    for folderName in dirs:

        print("Finalizando o e-mail da pasta: {}".format(folderName))

        caminho_img = "{}/{}".format(base_caminho_img, folderName)

        if envio_aws == 's':
            # executa o envio dos dados para o bucket s3
            print("Enviando os arquivos da pasta: {} para o S3 da Cielo".format(folder_date))
            cmd = "aws s3 cp {0}{1} s3://cielodigital-com-br-prd-2l30tw/marketing/{1}/ --profile cielo --exclude '*.mjml' --exclude '*.zip' --exclude '*.html' --recursive".format(config.baseDirectory, folder_date)
            push = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
            print("Status code de retorno da AWS: {} erros".format(push.returncode))
            sleep(qtde_arquivos_pasta)

        file = open("{}/{}/preview.html".format(folder_root, folderName), "r", encoding='cp1252', errors='ignore')
        contents = file.read()
        soup = BeautifulSoup(contents, 'html.parser')

        for element in soup.find_all('img'):
            element['src'] = "{}/{}".format(caminho_img, element['src'])

        with open("{}/{}/index.html".format(folder_root, folderName), "w") as f_output:
            f_output.write(soup.prettify(formatter="minimal"))

        # create a ZipFile object
        with ZipFile('{}/{}.zip'.format(folder_root, folderName), 'w') as zipObj:
            for folderNameEmail, subfoldersEmail, filenamesEmail in os.walk("{}/{}".format(folder_root, folderName)):
                for filename in filenamesEmail:

                    split_tup = os.path.splitext(filename)
                    file_extension = split_tup[1]

                    if file_extension != ".mjml":
                        filePath = os.path.join(folderNameEmail, filename)
                        zipObj.write(filePath, basename(filePath))
