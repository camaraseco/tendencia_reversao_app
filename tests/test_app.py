import os
from app import carregar_dados_alpha_vantage

def test_carregar_dados_alpha_vantage():
    api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
    dados = carregar_dados_alpha_vantage("AAPL", api_key, "1min")
    assert not dados.empty, "Os dados carregados devem conter valores."
