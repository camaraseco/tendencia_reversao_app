# Arquivo: tests/test_notificacoes.py

import pytest
from utils import enviar_email

def test_enviar_email(monkeypatch):
    def mock_sendmail(*args, **kwargs):
        return {}

    monkeypatch.setattr("smtplib.SMTP.sendmail", mock_sendmail)

    try:
        enviar_email(
            tipo_operacao="Compra",
            preco_execucao=150.0,
            motivo="Take Profit",
            data_hora="2024-12-29 15:30:00",
            email_destinatario="usuario_teste@gmail.com"
        )
        assert True
    except Exception:
        assert False, "Erro ao enviar email."
