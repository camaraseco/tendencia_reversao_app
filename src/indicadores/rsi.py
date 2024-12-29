import pandas_ta as ta

def calcular_rsi(dados, periodo=14):
    """
    Calcula o RSI (Índice de Força Relativa).

    Parâmetros:
        dados (pd.DataFrame): DataFrame contendo os preços de fechamento (coluna 'close').
        periodo (int): Período para calcular o RSI (padrão: 14).

    Retorna:
        pd.Series: Série com os valores do RSI.
    """
    return ta.rsi(dados['close'], length=periodo)
