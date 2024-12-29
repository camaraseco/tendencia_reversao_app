import pandas_ta as ta

def calcular_emas(dados, periodos):
    """
    Calcula as EMAs para os períodos fornecidos.

    Parâmetros:
        dados (pd.DataFrame): DataFrame contendo os preços de fechamento (coluna 'close').
        periodos (list): Lista de períodos para calcular as EMAs.

    Retorna:
        dict: Um dicionário com as EMAs calculadas ou mensagens de erro caso os dados sejam insuficientes.
    """
    emas = {}
    for periodo in periodos:
        # Verifica se há dados suficientes para calcular o período
        if len(dados['close']) >= periodo:
            emas[f'EMA_{periodo}'] = ta.ema(dados['close'], length=periodo)
        else:
            emas[f'EMA_{periodo}'] = None  # Indica que não foi possível calcular
    
    return emas
