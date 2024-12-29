# Arquivo: tests/test_cruzamento.py

import pytest
import pandas as pd
from estrategia.estrategia_cruzamento import estrategia_cruzamento_medias

def test_estrategia_cruzamento_compra():
    # EMA Rápida cruza para cima da EMA Lenta
    ema_rapida = pd.Series([98, 99, 100, 101, 102])  # EMA Rápida sobe
    ema_lenta = pd.Series([100, 100, 100, 101, 101])  # EMA Lenta permanece acima
    sinal = estrategia_cruzamento_medias(None, ema_rapida, ema_lenta, margem=1)
    assert sinal == "COMPRA", f"Sinal incorreto retornado: {sinal}"


def test_estrategia_cruzamento_venda():
    # EMA Rápida cruza para baixo da EMA Lenta
    ema_rapida = pd.Series([102, 101, 100, 99, 98])  # EMA Rápida desce
    ema_lenta = pd.Series([100, 100, 100, 99, 99])  # EMA Lenta permanece acima
    sinal = estrategia_cruzamento_medias(None, ema_rapida, ema_lenta, margem=1)
    assert sinal == "VENDA", f"Sinal incorreto retornado: {sinal}"


def test_estrategia_cruzamento_neutro():
    # Nenhum cruzamento ocorre
    ema_rapida = pd.Series([100, 101, 102, 103, 104])  # EMA Rápida sobe constantemente
    ema_lenta = pd.Series([100, 101, 102, 103, 104])  # EMA Lenta segue mesma direção
    sinal = estrategia_cruzamento_medias(None, ema_rapida, ema_lenta, margem=1)
    assert sinal == "NEUTRO", f"Sinal incorreto retornado: {sinal}"



