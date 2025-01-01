# Arquivo: tests/test_notificacoes.py

# Arquivo: tests/test_notificacoes.py

import pytest
from unittest.mock import patch, call
from utils import enviar_email

@patch("utils.smtplib.SMTP")
def test_enviar_email(mock_smtp):
    # Configuração do mock para o servidor SMTP
    mock_server = mock_smtp.return_value.__enter__.return_value

    # Valores simulados para o teste
    email_user = "seu_email@gmail.com"
    email_password = "sua_senha"
    tipo_operacao = "COMPRA"
    preco_execucao = 100.0
    motivo = "Stop Loss"
    data_hora = "2024-12-31 10:00:00"
    email_usuario = "usuario@exemplo.com"

    # Mock de variáveis de ambiente
    with patch.dict("os.environ", {"EMAIL_USER": email_user, "EMAIL_PASSWORD": email_password}):
        # Chamar a função de envio de e-mail
        enviar_email(
            tipo_operacao=tipo_operacao,
            preco_execucao=preco_execucao,
            motivo=motivo,
            data_hora=data_hora,
            email_usuario=email_usuario
        )

        # Verificar se o servidor SMTP foi configurado corretamente
        mock_server.starttls.assert_called_once()
        mock_server.login.assert_called_once_with(email_user, email_password)

        # Verificar se o e-mail foi enviado com os argumentos esperados
        mock_server.sendmail.assert_called_once()
        msg = mock_server.sendmail.call_args[0]
        assert msg[0] == email_user  # Remetente
        assert msg[1] == email_usuario  # Destinatário

