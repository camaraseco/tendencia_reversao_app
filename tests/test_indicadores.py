# Arquivo: tests/test_indicadores.py

from indicadores.medias_moveis import calcular_emas
from indicadores.rsi import calcular_rsi
from estrategia.estrategia_trading import estrategia_basica, estrategia_multiplos_intervalos

# Testes
import pandas as pd

def test_estrategia_basica():
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
    sinal = estrategia_basica(dados, emas, rsi, volume_medio)

    assert sinal in ["COMPRA", "VENDA", "NEUTRO"], f"Sinal inesperado: {sinal}"

def test_estrategia_multiplos_intervalos():
    dados_por_intervalo = {
        "1min": pd.DataFrame({
            'close': [100, 101, 102, 103, 104],
            'volume': [2000, 2200, 2300, 2400, 2500]
        }),
        "5min": pd.DataFrame({
            'close': [110, 111, 112, 113, 114],
            'volume': [3000, 3200, 3300, 3400, 3500]
        })
    }

    resultados = estrategia_multiplos_intervalos(dados_por_intervalo, rsi_periodo=14, volume_medio=1500)

    for intervalo, sinal in resultados.items():
        assert sinal in ["COMPRA", "VENDA", "NEUTRO", None], f"Sinal inesperado: {sinal} para o intervalo {intervalo}"

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
    sinal = estrategia_basica(dados, emas, rsi, volume_medio)

    assert sinal == "NEUTRO", "Esperado: NEUTRO devido ao volume baixo"

def test_estrategia_rsi_alto():
    # Configuração do volume médio
    volume_medio = 2000

    # Dados simulados com close, volume e indicadores técnicos
    dados = pd.DataFrame({
        'close': [100, 101, 102, 103, 104, 105],
        'volume': [2500, 2700, 2800, 2900, 3000, 3100]  # Volume alto
    })

    # Simulação de valores de EMA
    emas = {
        'EMA_9': pd.Series([100, 101, 102, 103, 104, 105]),
        'EMA_21': pd.Series([107, 108, 109, 110, 111, 112])
    }

    # Simulação de valores de RSI (acima de 70)
    rsi = pd.Series([65, 70, 72, 75, 80, 85])

    # Executa a estratégia
    sinal = estrategia_basica(dados, emas, rsi, volume_medio)

    # Verifica se o sinal retornado é "VENDA"
    assert sinal == "VENDA", f"Esperado: VENDA, Obtido: {sinal}"
