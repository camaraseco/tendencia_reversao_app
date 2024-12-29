from dotenv import load_dotenv
import os

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# Configuração da API Alpha Vantage
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")


# Configurações do projeto

BROKER_API_KEY = "sua_chave_api"
BROKER_SECRET_KEY = "sua_chave_secreta"
BROKER_NAME = "binance"

EMA_PERIODS = [9, 21]
RSI_PERIOD = 14
STOP_LOSS_PERCENT = 0.005
TAKE_PROFIT_PERCENT = 0.01

