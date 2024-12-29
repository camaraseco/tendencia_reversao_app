# Arquivo: test_alpha_vantage.py

import pytest
from unittest.mock import patch

from estrategia.estrategia_trading import estrategia_basica, estrategia_multiplos_intervalos
import pandas as pd

# Dados simulados que imitam a resposta da API
mock_response = {
    "1min": pd.DataFrame({
        "open": [150.00, 149.50],
        "high": [155.00, 150.00],
        "low": [149.00, 148.50],
        "close": [154.00, 149.00],
        "volume": [2000, 1500]
    }),
    "5min": pd.DataFrame({
        "open": [148.00, 147.50],
        "high": [149.00, 148.50],
        "low": [147.00, 146.50],
        "close": [148.00, 147.00],
        "volume": [500, 400]
    })
}

# Testando a função buscar_dados_multiplos_intervalos com Mock
@patch('conexao_corretora.alpha_vantage_api.buscar_dados_multiplos_intervalos')
def test_buscar_dados_em_tempo_real(mock_buscar_dados):
    # Configura o mock para retornar os dados simulados
    mock_buscar_dados.return_value = mock_response

    from conexao_corretora.alpha_vantage_api import buscar_dados_multiplos_intervalos

    simbolo = "AAPL"
    intervalos = ["1min", "5min"]
    dados = buscar_dados_multiplos_intervalos(simbolo, intervalos)

    for intervalo in intervalos:
        assert intervalo in dados, f"Erro: Intervalo '{intervalo}' não está nos dados retornados!"
        assert not dados[intervalo].empty, f"Erro: Dados do intervalo '{intervalo}' estão vazios!"

# Testando a estratégia múltiplos intervalos com Mock
@patch('conexao_corretora.alpha_vantage_api.buscar_dados_multiplos_intervalos')
def test_estrategia_multiplos_intervalos(mock_buscar_dados):
    # Configura o mock para retornar os dados simulados
    mock_buscar_dados.return_value = mock_response

    from conexao_corretora.alpha_vantage_api import buscar_dados_multiplos_intervalos

    simbolo = "AAPL"
    intervalos = ["1min", "5min"]
    dados_por_intervalo = buscar_dados_multiplos_intervalos(simbolo, intervalos)

    resultados = estrategia_multiplos_intervalos(dados_por_intervalo, rsi_periodo=14, volume_medio=150000)

    for intervalo, sinal in resultados.items():
        assert sinal in ["COMPRA", "VENDA", "NEUTRO"], f"Sinal inesperado: {sinal} no intervalo {intervalo}"



