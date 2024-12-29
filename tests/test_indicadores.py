import sys
import os

# Adiciona a pasta 'src' ao caminho do Python, caso o pytest.ini não seja suficiente
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from indicadores.medias_moveis import calcular_emas
from indicadores.rsi import calcular_rsi
from estrategia.estrategia_trading import estrategia


# Testes
import pandas as pd

def test_estrategia():
    # Dados simulados
    dados = pd.DataFrame({
        'close': [100, 102, 101, 104, 105, 107, 106],
        'volume': [1000, 1200, 1500, 1800, 2000, 1700, 1600]
    })

    # Configuração
    periodos_ema = [9, 21]
    rsi_periodo = 14
    volume_medio = 1500

    # Calcular indicadores
    emas = calcular_emas(dados, periodos_ema)
    rsi = calcular_rsi(dados, rsi_periodo)

    # Testar estratégia
    sinal = estrategia(dados, emas, rsi, volume_medio)

    assert sinal in ["COMPRA", "VENDA", None], f"Sinal inesperado: {sinal}"

def test_calcular_emas():
    # Dados simulados
    dados = pd.DataFrame({
        'close': [100, 102, 101, 104, 105, 107, 106, 108, 110, 112]
    })
    periodos = [9, 21]

    # Calcula as EMAs
    emas = calcular_emas(dados, periodos)

    # Verifica se as EMAs foram calculadas corretamente
    assert emas['EMA_9'] is not None, "EMA_9 não foi calculada!"
    assert emas['EMA_21'] is None, "EMA_21 deveria ser None devido a dados insuficientes!"

def test_estrategia_volume_baixo():
    dados = pd.DataFrame({
        'close': [100, 101, 102, 103, 104, 105],
        'volume': [900, 950, 1000, 1100, 1200, 1300],  # Todos abaixo de 1500
    })
    periodos_ema = [9, 21]
    rsi_periodo = 14
    volume_medio = 1500

    emas = calcular_emas(dados, periodos_ema)
    rsi = calcular_rsi(dados, rsi_periodo)
    sinal = estrategia(dados, emas, rsi, volume_medio)

    assert sinal is None  # Nenhum sinal deve ser gerado, pois o volume está abaixo da média

def test_estrategia_rsi_alto():
    """
    Testa a lógica de venda da função 'estrategia' em um cenário com RSI alto.
    """
    # Configuração do volume médio
    volume_medio = 2000

    # Dados simulados com close, volume e indicadores técnicos
    dados = pd.DataFrame({
        'close': [100, 101, 102, 103, 104, 105],  # Preços crescentes
        'volume': [2500, 2700, 2800, 2900, 3000, 3100]  # Volume alto
    })

    # Simulação de valores de EMA
    emas = {
        'EMA_9': pd.Series([100, 101, 102, 103, 104, 105]),  # Valores menores
        'EMA_21': pd.Series([107, 108, 109, 110, 111, 112])  # Valores maiores
    }

    # Simulação de valores de RSI (acima de 70)
    rsi = pd.Series([65, 70, 72, 75, 80, 85])

    # Executa a estratégia
    sinal = estrategia(dados, emas, rsi, volume_medio)

    # Verifica se o sinal retornado é "VENDA"
    assert sinal == "VENDA", f"Esperado: VENDA, Obtido: {sinal}"
