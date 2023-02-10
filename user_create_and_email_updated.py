#!/usr/bin/python3

import smtplib
import os
import config
import pandas as pd
import random
import string
import subprocess
import sys

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

if __name__ == '__main__':
    input= pd.read_csv(sys.argv[1])
    a_username = config.username
    a_password = config.password
    mail_from = config.username
    for i in range(0,len(input)):
        userid= input['email'][i].split('@')[0]
        emailid= input['email'][i]
        username = input['First_Name'][i]
        last_name = input['Last_name'][i]
        YSU_ID = input['YSU_ID'][i]
        result = subprocess.run(['id', '-u', userid], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            print('user does not exists. creating the user : ',username)
            passd = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
            print(passd)
            print(userid)
            subprocess.run(['useradd', '-m', userid ])
            cmd = f"echo {userid}:{passd} | chpasswd"
            subprocess.call(cmd,shell=True)
        #os.system('echo userid:,'passd', | chpasswd')
            mail_to = emailid
            mail_subject = "LINUX USERID AND PASSWORD"
            mail_body = f"Greetings,\
            \n \
            \n Your account on a server in Data Lab has been created. Please use ssh on Linux or Putty on Windows to login to the server terminal. Let me know how it works.\
            \n \
            \n* Server IP: xxx (you may need to login YSU VPN when off campus)\
            \n* Username: {userid} (Your YSU email initial. e.g. If your email is [abc@ysu.edu](mailto:abc@ysu.edu), your username is abc.)\
            \n* Temporary Password: {passd} (you will be asked to change your password during your first time login)\
            \n \
            \nReminders:\
            \n \
            \n* Please note that the data may not be backed up on this server and backup your data periodically.\
            \n* For security purpose, please allow me to remind you that this server is for teaching/research only. Please comply with the YSU and CSIS rules and security policies when using this server. You will be responsible for any unauthorized misuse of this server. The best practice is to check with me when there is a question on this.\
            \n \
            \nBest wishes,\
            \nFeng George Yu, Ph.D.\
            \nAssociate Professor\
            \nSchool of Computer Science, Information, and Engineering Technology\
            \nYoungstown State University, OH 44555\
            \nOffice: Meshel 316\
            \nLandline: 330.941.1775"
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
            output = f" echo '{YSU_ID}','{username}','{last_name}','{userid}','{passd}','New' >> output.csv"
            subprocess.run(output, shell=True)
        else:
            print('The User', userid, 'already exists')
