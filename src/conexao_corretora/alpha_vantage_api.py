# Arquivo: alpha_vantage_api.py

import requests
import pandas as pd
from dotenv import load_dotenv
import os

# Carregar variáveis do .env
load_dotenv()
API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
BASE_URL = "https://www.alphavantage.co/query"

def buscar_dados_multiplos_intervalos(simbolo, intervalos):
    """
    Busca dados de múltiplos intervalos na API Alpha Vantage.
    """
    resultados = {}

    for intervalo in intervalos:
        parametros = {
            "function": "TIME_SERIES_INTRADAY",
            "symbol": simbolo,
            "interval": intervalo,
            "apikey": API_KEY,
            "datatype": "json",
            "outputsize": "compact"
        }

        try:
            resposta = requests.get(BASE_URL, params=parametros)
            resposta.raise_for_status()
            dados = resposta.json()

            # Verifica se a resposta contém dados válidos
            chave_serie_temporal = f"Time Series ({intervalo})"
            if chave_serie_temporal in dados:
                serie_temporal = dados[chave_serie_temporal]
                df = pd.DataFrame.from_dict(serie_temporal, orient="index")
                df.columns = ["open", "high", "low", "close", "volume"]
                
                # Converte para os tipos numéricos corretos
                df = df.astype({"open": float, "high": float, "low": float, "close": float, "volume": float})
                df.index = pd.to_datetime(df.index)
                resultados[intervalo] = df
            else:
                print(f"Erro: Intervalo '{intervalo}' não retornou dados válidos. Resposta: {dados}")
        except Exception as e:
            print(f"Erro ao buscar dados para o intervalo '{intervalo}': {e}")

    return resultados

def verificar_conexao():
    """
    Verifica se a conexão com a API Alpha Vantage está ativa.
    """
    url = "https://www.alphavantage.co/query"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            print("Conexão com a API estabelecida com sucesso!")
        else:
            print("Falha na conexão com a API.")
    except requests.exceptions.RequestException as e:
        print(f"Erro ao conectar: {e}")
