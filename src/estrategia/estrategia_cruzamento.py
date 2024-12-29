# Arquivo: estrategia_cruzamento.py

import pandas as pd

# Estratégia de Cruzamento de Médias Móveis
def estrategia_cruzamento_medias(dados, ema_rapida, ema_lenta, margem=0.01):
    """
    Estratégia baseada no cruzamento de médias móveis.

    Parâmetros:
        dados (pd.DataFrame): DataFrame com os dados de mercado (opcional).
        ema_rapida (pd.Series): Série da média móvel rápida.
        ema_lenta (pd.Series): Série da média móvel lenta.
        margem (float): Margem de tolerância para detectar cruzamentos.

    Retorna:
        str: "COMPRA", "VENDA" ou "NEUTRO".
    """
    # Garantir que há pelo menos 2 valores para realizar a comparação
    if len(ema_rapida) < 2 or len(ema_lenta) < 2:
        print("Dados insuficientes para cálculo de cruzamento.")
        return "NEUTRO"

    # Obter os valores de ontem e hoje
    ema_rapida_ontem = ema_rapida.iloc[-2]
    ema_rapida_hoje = ema_rapida.iloc[-1]
    ema_lenta_ontem = ema_lenta.iloc[-2]
    ema_lenta_hoje = ema_lenta.iloc[-1]

    # Logs para depuração
    print(f"Debug - EMA Rápida Ontem: {ema_rapida_ontem}, Hoje: {ema_rapida_hoje}")
    print(f"Debug - EMA Lenta Ontem: {ema_lenta_ontem}, Hoje: {ema_lenta_hoje}")

    # Verificar cruzamento para "COMPRA"
    if (ema_rapida_ontem <= ema_lenta_ontem and ema_rapida_hoje > ema_lenta_hoje):
        if abs(ema_lenta_ontem - ema_rapida_ontem) <= margem or abs(ema_lenta_hoje - ema_rapida_hoje) <= margem:
            print("Cruzamento detectado: COMPRA")
            return "COMPRA"

    # Verificar cruzamento para "VENDA"
    if (ema_rapida_ontem >= ema_lenta_ontem and ema_rapida_hoje < ema_lenta_hoje):
        if abs(ema_lenta_ontem - ema_rapida_ontem) <= margem or abs(ema_lenta_hoje - ema_rapida_hoje) <= margem:
            print("Cruzamento detectado: VENDA")
            return "VENDA"

    # Caso nenhum cruzamento seja detectado
    print("Nenhum cruzamento detectado: NEUTRO")
    return "NEUTRO"


# Exemplo de uso da estratégia de cruzamento de médias móveis
def exemplo_cruzamento_medias():
    dados = pd.DataFrame({
        "close": [100, 102, 104, 103, 105, 107, 106]
    })
    # Calculando EMAs rápidas e lentas
    dados['EMA_9'] = dados['close'].ewm(span=9, adjust=False).mean()
    dados['EMA_21'] = dados['close'].ewm(span=21, adjust=False).mean()

    # Aplicando a estratégia
    sinal = estrategia_cruzamento_medias(dados, dados['EMA_9'], dados['EMA_21'])
    print(f"Sinal gerado: {sinal}")

if __name__ == "__main__":
    exemplo_cruzamento_medias()
      

                                                                                                                                            




