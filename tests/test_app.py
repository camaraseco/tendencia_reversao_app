# Arquivo: tests/test_app.py

import os
import pytest
from unittest.mock import patch
import pandas as pd

# Dados simulados para o teste
mock_response = pd.DataFrame({
    "open": [150.00, 149.50],
    "high": [155.00, 150.00],
    "low": [149.00, 148.50],
    "close": [154.00, 149.00],
    "volume": [2000, 1500]
})

# Testando carregar_dados_alpha_vantage com Mock
@patch('app.carregar_dados_alpha_vantage')
def test_carregar_dados_alpha_vantage(mock_carregar_dados):
    # Configura o mock para retornar os dados simulados
    mock_carregar_dados.return_value = mock_response

    from main import carregar_dados_alpha_vantage

    api_key = "MOCKED_API_KEY"
    dados = carregar_dados_alpha_vantage("AAPL", api_key, "1min")

    assert not dados.empty, "Os dados carregados devem conter valores."
    assert "close" in dados.columns, "Os dados devem conter a coluna 'close'."
    assert dados["close"].iloc[-1] == 149.00, "O último valor de fechamento deve ser 149.00."
