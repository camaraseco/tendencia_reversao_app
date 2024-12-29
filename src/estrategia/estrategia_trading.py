# Arquivo: estrategia_trading.py

import pandas as pd

# Estratégia Básica
def estrategia_basica(dados, emas, rsi, volume_medio):
    if (
        emas['EMA_9'].iloc[-1] > emas['EMA_21'].iloc[-1] and  # EMA 9 acima da EMA 21
        rsi.iloc[-1] < 30 and  # RSI abaixo de 30
        dados['volume'].iloc[-1] > volume_medio  # Volume acima da média
    ):
        return "COMPRA"
    elif (
        emas['EMA_9'].iloc[-1] < emas['EMA_21'].iloc[-1] and  # EMA 9 abaixo da EMA 21
        rsi.iloc[-1] > 70 and  # RSI acima de 70
        dados['volume'].iloc[-1] > volume_medio  # Volume acima da média
    ):
        return "VENDA"
    return "NEUTRO"

# Estratégia Múltiplos Intervalos
def estrategia_multiplos_intervalos(dados, rsi_periodo=14, volume_medio=100):
    # Debug: Verificar os valores antes da lógica
    print("Dados recebidos para estratégia múltiplos intervalos:")
    print(dados[['close', 'volume']].tail())
    print(f"RSI Período: {rsi_periodo}, Volume Médio: {volume_medio}")

    resultados = {}
    for intervalo, dados in dados.items():
        # Verifica se as colunas necessárias estão presentes
        if 'close' in dados and 'volume' in dados:
            emas = {
                f'EMA_{periodo}': dados['close'].rolling(window=periodo).mean()
                for periodo in [9, 21]
            }
            rsi = (dados['close'].diff().apply(lambda x: max(x, 0)).rolling(window=rsi_periodo).mean()
                   / dados['close'].diff().abs().rolling(window=rsi_periodo).mean()) * 100
            sinal = estrategia_basica(dados, emas, rsi, volume_medio)
            resultados[intervalo] = sinal
        else:
            resultados[intervalo] = "NEUTRO"
    return resultados
