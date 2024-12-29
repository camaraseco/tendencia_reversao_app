# Arquivo: src/app.py

from indicadores.medias_moveis import calcular_emas
from indicadores.rsi import calcular_rsi
from estrategia.estrategia_cruzamento import estrategia_cruzamento_medias
from estrategia.estrategia_trading import estrategia_basica, estrategia_multiplos_intervalos
import requests
import pandas as pd
import os
from dotenv import load_dotenv
from src.utils import init_db

# Carregar variáveis de ambiente
load_dotenv()

def carregar_dados_alpha_vantage(symbol, api_key, intervalo='1min'):
    """
    Carrega os dados do mercado usando a API Alpha Vantage.
    """
    url = f"https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_INTRADAY",
        "symbol": symbol,
        "interval": intervalo,
        "apikey": api_key,
        "datatype": "json"
    }
    response = requests.get(url, params=params)

    if response.status_code != 200:
        raise Exception(f"Erro ao acessar Alpha Vantage: {response.status_code} - {response.text}")

    data = response.json()
    key = f"Time Series ({intervalo})"
    if key not in data:
        raise Exception(f"Erro: Chave '{key}' não encontrada na resposta da API.")

    df = pd.DataFrame.from_dict(data[key], orient="index")
    df = df.rename(columns={
        "1. open": "open",
        "2. high": "high",
        "3. low": "low",
        "4. close": "close",
        "5. volume": "volume"
    })
    df.index = pd.to_datetime(df.index)
    df = df.sort_index()

    if df.empty:
        raise Exception("Erro: Nenhum dado retornado pela API ou dados inválidos.")

    return df.astype(float)

def executar_estrategias(symbol, api_key, intervalo='1min'):
    """
    Executa todas as estratégias com base nos dados do Alpha Vantage.
    """
    # Carregar dados
    dados = carregar_dados_alpha_vantage(symbol, api_key, intervalo)

    # Calcular indicadores
    emas = calcular_emas(dados, [9, 21])
    dados['EMA_rapida'] = emas['EMA_9']
    dados['EMA_lenta'] = emas['EMA_21']
    rsi = calcular_rsi(dados, 14)

    resultados = {}

    # Estratégia de cruzamento de médias móveis
    sinal_cruzamento = estrategia_cruzamento_medias(
        dados=None,
        ema_rapida=dados['EMA_rapida'],
        ema_lenta=dados['EMA_lenta'],
        margem=0.5
    )
    resultados['estrategia_cruzamento'] = sinal_cruzamento

    # Estratégia de múltiplos intervalos
    volume_medio = dados['volume'].mean()
    sinal_multiplos = estrategia_multiplos_intervalos(dados, 14, volume_medio)
    resultados['estrategia_multiplos'] = sinal_multiplos

    # Estratégia básica
    sinal_basico = estrategia_basica(dados, emas, rsi, volume_medio)
    resultados['estrategia_basica'] = sinal_basico

    return resultados

if __name__ == "__main__":
    init_db()
