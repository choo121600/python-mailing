import smtplib
import re
import markdown
import pandas as pd

from settings import *
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class EmailSender:
    def __init__(self, smtp_server, smtp_port, account, password):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.account = account
        self.password = password
        self.smtp = None

    def connect(self):
        self.smtp = smtplib.SMTP_SSL(self.smtp_server, self.smtp_port)
        self.smtp.login(self.account, self.password)

    def disconnect(self):
        if self.smtp:
            self.smtp.quit()

    def send_email(self, recipients, subject, cc, bcc, content):
        for recipient in recipients:

            message = MIMEMultipart()
            message["Subject"] = subject
            message["From"] = self.account
            message["To"] = recipient

            if cc:
                cc_mail = ', '.join(cc)
                message["Cc"] = cc_mail

            recipients_list = [recipient] + cc + bcc

            with open(content, 'r') as file:
                markdown_content = file.read()
                html_content = markdown.markdown(markdown_content)

            content_part = MIMEText(html_content, "html")
            message.attach(content_part)

            try:
                self.smtp.sendmail(self.account, recipients_list, message.as_string())
                print(f"정상적으로 메일이 발송되었습니다: {recipients_list}")
            except Exception as e:
                print(f"메일 발송 중 오류가 발생했습니다: {recipients_list} - {str(e)}")


smtp_server = "smtp.gmail.com"
smtp_port = SMTP_PORT
account = ACCOUNT
password = PASSWORD
sender = EmailSender(smtp_server, smtp_port, account, password)

participants = pd.read_csv(SEND_TO_PATH)
participants = participants['0']

ccs = pd.read_csv(CCS_PATH)
ccs = ccs['0']

bccs = pd.read_csv(BCCS_PATH)
bccs = bccs['0']

recipients = list(participants) ## 보낼 사람들의 이메일 리스트 입력
subject = MAIL_TITLE

cc = list(ccs) ## 참조할 사람들의 이메일 리스트 입력
bcc = list(bccs) ## 숨은 참조할 사람들의 이메일 리스트 입력
content = MAIL_BODY_PATH

sender.connect()
sender.send_email(recipients, subject, cc, bcc, content)
sender.disconnect()
