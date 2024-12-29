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
    Envia uma notificação por email ao usuário sobre uma operação finalizada.

    Args:
        tipo_operacao (str): 'Compra' ou 'Venda'.
        preco_execucao (float): Preço de execução da operação.
        motivo (str): 'Stop Loss' ou 'Take Profit'.
        data_hora (str): Data e hora da finalização.
        email_destinatario (str): Email do usuário.
    """
    email_user = os.getenv("EMAIL_USER")
    email_password = os.getenv("EMAIL_PASSWORD")
    email_host = os.getenv("EMAIL_HOST")
    email_port = int(os.getenv("EMAIL_PORT"))

    assunto = f"Notificação: Operação {tipo_operacao} Finalizada ({motivo})"
    corpo = f"""
    Prezado usuário,

    Sua operação foi finalizada com os seguintes detalhes:

    - Tipo de operação: {tipo_operacao}
    - Preço de execução: {preco_execucao}
    - Motivo: {motivo}
    - Data e hora: {data_hora}

    Atenciosamente,
    Equipe de Negociação Automática.
    """

    mensagem = MIMEMultipart()
    mensagem['From'] = email_user
    mensagem['To'] = email_destinatario
    mensagem['Subject'] = assunto
    mensagem.attach(MIMEText(corpo, 'plain'))

    try:
        with smtplib.SMTP(email_host, email_port) as servidor:
            servidor.starttls()
            servidor.login(email_user, email_password)
            servidor.sendmail(email_user, email_destinatario, mensagem.as_string())
        print(f"Email enviado com sucesso para {email_destinatario}.")
    except Exception as e:
        print(f"Erro ao enviar email: {e}")