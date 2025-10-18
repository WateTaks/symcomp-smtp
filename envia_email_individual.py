import os
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

load_dotenv()
sender_email = os.getenv('EMAIL_USER').strip()
password = os.getenv('EMAIL_PASSWORD').strip()

lista_destinatarios = [
    ("JOJO", "jonathascastilho@usp.br")
]

with open('index.html', 'r', encoding='utf-8') as file:
    html_template = file.read()

def send_email(subject, html, to_emails):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 465

    message = MIMEMultipart('related')
    message['Subject'] = subject
    message['From'] = sender_email
    message['To'] = ', '.join(to_emails)

    part = MIMEText(html, 'html')
    message.attach(part)

    for img_path, cid in [('./src/header_2025.png', 'HeaderImage'),
                          ('./src/cotas_2025.png', 'CotasImage')]:
        with open(img_path, 'rb') as fp:
            img = MIMEImage(fp.read())
        img.add_header('Content-ID', f'<{cid}>')
        message.attach(img)

    with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, to_emails, message.as_string())

if not lista_destinatarios:
    print("Nenhum destinatário informado.")
    exit()

print("Abaixo os emails com os nomes dos contatos que receberão o email: \n")
for empresa, emails_str in lista_destinatarios:
    print(f"{empresa}: {emails_str}")

confirmation = input("Digite 'Y' para confirmar o envio ou 'N' para cancelar: ")

if confirmation.upper() != 'Y':
    print("Envio de email cancelado.")
    exit()

print("Enviando emails...")

subject = 'XIV Semana da Computação IME - USP'

for empresa, emails_str in lista_destinatarios:
    emails = [e.strip() for e in emails_str.split(',')]
    html_personalizado = html_template.replace('{{NOME_EMPRESA}}', empresa)
    try:
        send_email(subject, html_personalizado, emails)
        print(f"Email enviado com sucesso para {emails} (Empresa: {empresa})")
    except Exception as e:
        print(f"Falha ao enviar email para {emails}: {e}")

print("Processo concluído.")