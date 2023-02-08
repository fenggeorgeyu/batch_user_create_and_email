#!/usr/bin/python3

import smtplib
import config
import pandas as pd
import random
import string
import subprocess

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText



#if __name__=="__main__":
input= pd.read_csv('input.csv')
#print(input)
a_username = config.username
a_password = config.password
mail_from = config.username
for i in range(0,len(input)):
    userid= input[' email'][i].split('@')[0]
    emailid= input[' email'][i]
    username = input['name'][i]
    print(username)
    passd = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    print(passd)
    print(userid)
    #subprocess.run('useradd -m "{userid}"' , shell=True)
    subprocess.run(['useradd', '-m', userid ])
    cmd = f"echo {userid}:{passd} | chpasswd"
    subprocess.call(cmd,shell=True)
    #os.system('echo userid:,'passd', | chpasswd')
    mail_to = emailid
    mail_subject = "Data Lab Server User Credential"
    mail_body = f"Hi {username}, please find your login credentials for linux account in Data Lab Credential. user name {userid} and password {passd}."
    print(mail_from)
    mimemsg = MIMEMultipart()
    mimemsg['From']=mail_from
    mimemsg['To']=mail_to
    mimemsg['Subject']=mail_subject
    mimemsg.attach(MIMEText(mail_body, 'plain'))
    connection = smtplib.SMTP(host='smtp.gmail.com', port=587)
    connection.starttls()
    connection.login(a_username,a_password)
    connection.send_message(mimemsg)
    connection.quit()
    reset=f"passwd -e {userid}"
    subprocess.Popen(reset, shell=True)
