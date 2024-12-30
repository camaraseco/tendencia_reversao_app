# Arquivo: src\utils.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os


DATABASE_URL = "postgresql://postgres:Pocamara.99@localhost:5432/setup_db"  # Substitua pelo URL do seu banco de dados

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    # Importar os modelos aqui para que sejam registrados corretamente
    import src.backend.models
    src.backend.models.Base.metadata.create_all(bind=engine)

def enviar_email(tipo_operacao, preco_execucao, motivo, data_hora, email_destinatario):
    """
    Envia um email de notificação ao usuário quando uma operação é finalizada.

    Parâmetros:
        tipo_operacao (str): Tipo de operação realizada ('COMPRA' ou 'VENDA').
        preco_execucao (float): Preço em que a operação foi executada.
        motivo (str): Motivo da finalização da operação ('Stop Loss' ou 'Take Profit').
        data_hora (datetime): Data e hora da operação.
        email_destinatario (str): Email do usuário para enviar a notificação.
    """
    smtp_host = "smtp.gmail.com"
    smtp_port = 587
    smtp_user = os.getenv("EMAIL_USER")
    smtp_password = os.getenv("EMAIL_PASSWORD")

    mensagem = MIMEMultipart()
    mensagem["From"] = smtp_user
    mensagem["To"] = email_destinatario
    mensagem["Subject"] = f"Notificação: Operação {tipo_operacao} Finalizada ({motivo})"

    corpo_email = f"""
    Prezado usuário,

    Sua operação foi finalizada com os seguintes detalhes:

    Tipo de operação: {tipo_operacao}
    Preço de execução: {preco_execucao}
    Motivo: {motivo}
    Data e hora: {data_hora}

    Atenciosamente,
    Equipe de Negociação Automática
    """
    mensagem.attach(MIMEText(corpo_email, "plain"))

    try:
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.sendmail(smtp_user, email_destinatario, mensagem.as_string())
            print(f"Email enviado com sucesso para {email_destinatario}.")
    except Exception as e:
        print(f"Erro ao enviar email: {e}")