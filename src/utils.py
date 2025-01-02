# Arquivo: src\utils.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import logging

# Configurar logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



DATABASE_URL = "postgresql://postgres:Pocamara.99@localhost:5432/setup_db"  # Substitua pelo URL do seu banco de dados

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    # Importar os modelos aqui para que sejam registrados corretamente
    import src.backend.models
    src.backend.models.Base.metadata.create_all(bind=engine)

def enviar_email(tipo_operacao, preco_execucao, motivo, data_hora, email_usuario):
    try:
        # Configurações do email
        email_user = os.getenv("EMAIL_USER")
        email_password = os.getenv("EMAIL_PASSWORD")

        if not email_user or not email_password:
            raise ValueError("EMAIL_USER ou EMAIL_PASSWORD não configurados no arquivo .env.")

        # Configurando o servidor SMTP
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email_user, email_password)

        # Criando o email
        msg = MIMEMultipart()
        msg["From"] = email_user
        msg["To"] = email_usuario
        msg["Subject"] = "Notificação de Operação"
        body = (
            f"Operação finalizada com sucesso!\n\n"
            f"Tipo: {tipo_operacao}\n"
            f"Preço: {preco_execucao}\n"
            f"Motivo: {motivo}\n"
            f"Data e Hora: {data_hora}\n"
        )
        msg.attach(MIMEText(body, "plain"))

        # Enviar o email
        server.sendmail(email_user, email_usuario, msg.as_string())
        server.quit()

        print(f"Email enviado para {email_usuario}")
    except Exception as e:
        print(f"Erro ao enviar email: {e}")
        raise