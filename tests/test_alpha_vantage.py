# Arquivo: test_alpha_vantage.py

import pytest
from conexao_corretora.alpha_vantage_api import buscar_dados_multiplos_intervalos
from estrategia.estrategia_trading import estrategia_basica, estrategia_multiplos_intervalos
import pandas as pd
from conexao_corretora.alpha_vantage_api import verificar_conexao

def test_buscar_dados_em_tempo_real():
    simbolo = "AAPL"
    intervalos = ["1min", "5min"]
    dados = buscar_dados_multiplos_intervalos(simbolo, intervalos)
    for intervalo in intervalos:
        assert intervalo in dados, f"Erro: Intervalo '{intervalo}' não está nos dados retornados!"
        assert not dados[intervalo].empty, f"Erro: Dados do intervalo '{intervalo}' estão vazios!"

def test_estrategia_multiplos_intervalos():
    simbolo = "AAPL"
    intervalos = ["1min", "5min"]
    dados_por_intervalo = buscar_dados_multiplos_intervalos(simbolo, intervalos)
    resultados = estrategia_multiplos_intervalos(dados_por_intervalo, rsi_periodo=14, volume_medio=150000)
    for intervalo, sinal in resultados.items():
        assert sinal in ["COMPRA", "VENDA", "NEUTRO"]
