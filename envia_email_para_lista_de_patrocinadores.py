import os
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

import email_extractor  # importa o módulo que gera df_filtered

load_dotenv()
sender_email = os.getenv('EMAIL_USER')
password = os.getenv('EMAIL_PASSWORD')

with open('index.html', 'r') as file:
    html_template = file.read()

def send_email(subject, html, to_email):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587

    message = MIMEMultipart('alternative')
    message['Subject'] = subject
    message['From'] = sender_email
    message['To'] = to_email

    part = MIMEText(html, 'html')
    message.attach(part)

    with open('./src/header_2025.png', 'rb') as fp:
        imageHeader = MIMEImage(fp.read())
    imageHeader.add_header('Content-ID', '<HeaderImage>')
    message.attach(imageHeader)

    with open('./src/cotas_2025.png', 'rb') as fp:
        imageCotas = MIMEImage(fp.read())
    imageCotas.add_header('Content-ID', '<CotasImage>')
    message.attach(imageCotas)

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, to_email, message.as_string())

with open('index.html', 'r') as file:
    html = file.read()

subject = 'XIV Semana da Computação IME - USP'

df = email_extractor.df_filtered

df_to_send = df[df['STATUS'] == 'waiting_send']

if df_to_send.empty:
    print("Não há emails para enviar com status 'waiting_send'.")
    exit()

print("Abaixo os emails com os nomes dos contatos que receberão o email: \n")

for idx, row in df_to_send.iterrows():
    nome = row['NOME DA EMPRESA']
    emails = row['CONTATO']
    print(f"{nome}: {', '.join(emails)}")

confirmation = input("Digite 'Y' para confirmar o envio ou 'N' para cancelar: ")

if confirmation.upper() != 'Y':
    print("Envio de email cancelado.")
    exit()

print("Enviando emails...")

for idx, row in df_to_send.iterrows():
    empresa = row['NOME DA EMPRESA']
    emails = row['CONTATO']
    for email in emails:
        html_personalizado = html_template.replace('{{NOME_EMPRESA}}', empresa)
        try:
            send_email(subject, html_personalizado, email)
            print(f"Email enviado com sucesso para {email} (Empresa: {empresa})")
        except Exception as e:
            print(f"Falha ao enviar email para {email}: {e}")

print("Processo concluído.")
