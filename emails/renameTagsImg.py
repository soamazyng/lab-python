# Importing library
from bs4 import BeautifulSoup
from zipfile import ZipFile
import os
from os.path import basename

print("****************************************")
print("Bem-Vindx")
print("****************************************")

folder_root = input("O Caminho da pasta que contém os e-mails: ")
last = folder_root.rsplit('\\', 1)[-1]
base_caminho_img = "http://cielodigital.com.br/marketing/{}".format(last)

for root, dirs, files in os.walk(folder_root, topdown=False):
    for folderName in dirs:

        # print(folderName)

        caminho_img = "{}/{}".format(base_caminho_img, folderName)

        file = open("{}/{}/preview.html".format(folder_root, folderName), "r")
        contents = file.read()
        soup = BeautifulSoup(contents, 'html.parser')

        for element in soup.find_all('img'):
            element['src'] = "{}/{}".format(caminho_img, element['src'])

        with open("{}/{}/index.html".format(folder_root, folderName), "wb") as f_output:
            f_output.write(soup.prettify("utf-8"))

        # create a ZipFile object
        with ZipFile('{}/{}.zip'.format(folder_root, folderName), 'w') as zipObj:
            for folderNameEmail, subfoldersEmail, filenamesEmail in os.walk("{}/{}".format(folder_root, folderName)):
                for filename in filenamesEmail:

                    split_tup = os.path.splitext(filename)
                    file_extension = split_tup[1]

                    if file_extension != ".mjml":
                        filePath = os.path.join(folderNameEmail, filename)
                        zipObj.write(filePath, basename(filePath))
