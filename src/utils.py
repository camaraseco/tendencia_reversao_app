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
    """
    Envia uma notificação por e-mail ao usuário.
    """
    try:
        # Configurações do servidor SMTP
        email_user = os.getenv("EMAIL_USER")
        email_password = os.getenv("EMAIL_PASSWORD")

        if not email_user or not email_password:
            raise Exception("Credenciais de e-mail não configuradas nas variáveis de ambiente.")

        # Compor o e-mail
        subject = "Notificação de Operação Finalizada"
        body = f"""
        Detalhes da operação:
        Tipo de operação: {tipo_operacao}
        Preço de execução: {preco_execucao}
        Motivo: {motivo}
        Data e hora: {data_hora}

        Obrigado por usar nosso sistema!
        """
        msg = MIMEMultipart()
        msg['From'] = email_user
        msg['To'] = email_usuario
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # Enviar o e-mail
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(email_user, email_password)
            server.sendmail(email_user, email_usuario, msg.as_string())

        logger.info(f"E-mail enviado com sucesso para {email_usuario}")

    except Exception as e:
        logger.error(f"Erro ao enviar e-mail: {e}")
        raise