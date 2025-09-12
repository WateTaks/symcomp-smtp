import os
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

load_dotenv()
sender_email = os.getenv('EMAIL_USER')
password = os.getenv('EMAIL_PASSWORD')

# Lista de emails para serem enviados (agora pode ter múltiplos emails por empresa)
lista_destinatarios = [
    ("Example", "example@example.br, outroexample@example.com"),
    ("Example1", "example1@example1.com, outroexample1@example1.com")
]

with open('index.html', 'r') as file:
    html_template = file.read()

def send_email(subject, html, to_emails):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587

    message = MIMEMultipart('alternative')
    message['Subject'] = subject
    message['From'] = sender_email
    message['To'] = ', '.join(to_emails)  # agora pode receber lista de emails

    part = MIMEText(html, 'html')
    message.attach(part)

    # Anexando imagens
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
    # separa os emails por vírgula e remove espaços extras
    emails = [e.strip() for e in emails_str.split(',')]
    html_personalizado = html_template.replace('{{NOME_EMPRESA}}', empresa)
    try:
        send_email(subject, html_personalizado, emails)
        print(f"Email enviado com sucesso para {emails} (Empresa: {empresa})")
    except Exception as e:
        print(f"Falha ao enviar email para {emails}: {e}")

print("Processo concluído.")
