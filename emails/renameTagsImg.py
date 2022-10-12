# Importing library
from bs4 import BeautifulSoup
from zipfile import ZipFile
import os
from os.path import basename

print("****************************************")
print("Bem-Vindx")
print("****************************************")

folder_root = input("O Caminho da pasta que contém os e-mails:")

for root, dirs, files in os.walk(folder_root, topdown=False):
    for folderName in dirs:

        # print(folderName)

        file = open("{}/{}/preview.html".format(folder_root, folderName), "r")
        contents = file.read()
        soup = BeautifulSoup(contents, 'html.parser')

        for element in soup.find_all('img'):
            element['src'] = "https://cielodigital.com.br/marketing/10-10-2022/3592A/3592_a_email_d_1_a_v2/{}".format(element['src'])

        with open("{}/{}/index.html".format(folder_root, folderName), "wb") as f_output:
            f_output.write(soup.prettify("utf-8"))

        # create a ZipFile object
        with ZipFile('sampleDir.zip', 'w') as zipObj:
            for folderNameEmail, subfoldersEmail, filenamesEmail in os.walk("{}/{}".format(folder_root, folderName)):
                for filename in filenamesEmail:

                    split_tup = os.path.splitext(filename)
                    file_extension = split_tup[1]

                    if file_extension != ".mjml" or file_extension != ".DS_Store":
                        filePath = os.path.join(folderNameEmail, filename)
                        zipObj.write(filePath, basename(filePath))
