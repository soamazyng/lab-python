import subprocess

cmd="aws s3 cp D:\\www\\NovaCodigo\\cielo-emkts\\2022\\20-10-2022 s3://cielodigital-com-br-prd-2l30tw/marketing/20-10-2022/ --profile cielo --exclude '*.mjml' --exclude '*.zip' --exclude '*.html' --recursive"
push=subprocess.Popen(cmd, shell=True, stdout = subprocess.PIPE)
print(push.errors)
