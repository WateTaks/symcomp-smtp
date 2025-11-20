import os
from dotenv import load_dotenv
import smtplib
from email.message import EmailMessage
import csv

load_dotenv()
FILENAME = os.getenv('FILENAME')
FOLDER = os.getenv('FOLDER')
SENDER_EMAIL = str(os.getenv('EMAIL_USER'))
PASSWORD = str(os.getenv('EMAIL_PASSWORD'))

if FILENAME is None:
    raise ValueError("Missing csv file")
if FOLDER is None:
    raise ValueError("Missing FOLDER")

# Tratamento dos dados
def load_csv(filename: str) -> dict[str, str]:
    data = {}
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data[row['nome']] = row['email']
             
    return data

# Envia um email com o arquivo em específico
def send_email(filename: str, email: str, name: str) -> None:
    file_path = os.path.join(FOLDER, filename)
    
    print("Arguments passed:", file_path, email, name)

    smtp_server = 'smtp.gmail.com'
    smtp_port = 465
    
    # Define o conteúdo do email
    msg = EmailMessage()
    msg['Subject'] = 'Certificado de Participação - XV Semana da Computação'
    msg['From'] = SENDER_EMAIL
    msg['To'] = email

    msg.set_content(f"""\
Olá {name}!
Muito obrigado por participar da XV Semana da Computação!
O certificado de participação, com as horas totais em palestras participadas, se encontra em anexo.

Nós da Symcomp agradecemos pela atenção :)"""
    )
    
    # Faz o attach do PDF
    with open(file_path, 'rb') as file:
        file_data = file.read()
        msg.add_attachment(file_data,
                           maintype='application',
                           subtype='pdf',
                           filename=filename)
    
    # Conecta ao servidor SMTP e envia o email
    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(SENDER_EMAIL, PASSWORD)
            server.send_message(msg)
        print(f"Email to {email} sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}") 

    print()

# Envio dos emails em massa
data: dict[str, str] = load_csv(FILENAME)
names: list[str] = os.listdir(FOLDER)

for name in names:
    actual_name: str = name[:-4]
    email: str = data[actual_name]
    send_email(name, email, actual_name)

print("Process finished!")
