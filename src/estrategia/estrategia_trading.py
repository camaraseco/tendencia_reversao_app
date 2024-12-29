# Arquivo: estrategia_trading.py

import pandas as pd
from utils import enviar_email
from datetime import datetime

def calcular_emas(dados, periodos):
    resultado = {}
    for periodo in periodos:
        if len(dados) < periodo:
            resultado[f'EMA_{periodo}'] = None
        else:
            resultado[f'EMA_{periodo}'] = dados['close'].ewm(span=periodo).mean()
    return resultado

def calcular_rsi(dados, periodo):
    if len(dados) < periodo:
        return None
    delta = dados['close'].diff()
    ganho = delta.where(delta > 0, 0)
    perda = -delta.where(delta < 0, 0)
    media_ganho = ganho.rolling(window=periodo).mean()
    media_perda = perda.rolling(window=periodo).mean()
    rs = media_ganho / media_perda
    rsi = 100 - (100 / (1 + rs))
    return rsi


# Estratégia Básica
def estrategia_basica(dados, emas, rsi, volume_medio):
    if (
        emas['EMA_9'] is not None and
        emas['EMA_21'] is not None and
        rsi is not None and
        not rsi.isna().all() and  # Certifique-se de que o RSI não está vazio
        emas['EMA_9'].iloc[-1] > emas['EMA_21'].iloc[-1] and  # EMA 9 acima da EMA 21
        rsi.iloc[-1] < 30 and  # RSI abaixo de 30
        dados['volume'].iloc[-1] > volume_medio  # Volume acima da média
    ):
        return "COMPRA"
    elif (
        emas['EMA_9'] is not None and
        emas['EMA_21'] is not None and
        rsi is not None and
        not rsi.isna().all() and
        emas['EMA_9'].iloc[-1] < emas['EMA_21'].iloc[-1] and  # EMA 9 abaixo da EMA 21
        rsi.iloc[-1] > 70 and  # RSI acima de 70
        dados['volume'].iloc[-1] > volume_medio  # Volume acima da média
    ):
        return "VENDA"
    return "NEUTRO"

# Estratégia Múltiplos Intervalos
def estrategia_multiplos_intervalos(dados_por_intervalo, rsi_periodo=14, volume_medio=1500):
    resultados = {}
    for intervalo, dados in dados_por_intervalo.items():
        # Verificar se os dados estão válidos
        if dados is None or dados.empty:
            resultados[intervalo] = None
            continue

        # Calcular indicadores
        emas = calcular_emas(dados, [9, 21])
        rsi = calcular_rsi(dados, rsi_periodo)

        # Aplicar a lógica da estratégia
        sinal = estrategia_basica(dados, emas, rsi, volume_medio)
        resultados[intervalo] = sinal

    return resultados

def processar_negociacao(tipo_operacao, preco_execucao, stop_loss, take_profit, preco_atual, email_usuario):
    """
    Processa a negociação e envia notificação por email se atingir Stop Loss ou Take Profit.

    Args:
        tipo_operacao (str): 'Compra' ou 'Venda'.
        preco_execucao (float): Preço inicial da operação.
        stop_loss (float): Preço de Stop Loss.
        take_profit (float): Preço de Take Profit.
        preco_atual (float): Preço atual do ativo.
        email_usuario (str): Email do usuário para notificação.
    """
    if preco_atual <= stop_loss:
        motivo = "Stop Loss"
        enviar_email(tipo_operacao, preco_execucao, motivo, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), email_usuario)
        return f"Operação finalizada em {stop_loss} por Stop Loss."
    elif preco_atual >= take_profit:
        motivo = "Take Profit"
        enviar_email(tipo_operacao, preco_execucao, motivo, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), email_usuario)
        return f"Operação finalizada em {take_profit} por Take Profit."
    return "Operação em andamento."
