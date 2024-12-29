from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.app import executar_estrategias
import os

router = APIRouter()

class TradingRequest(BaseModel):
    symbol: str
    interval: str = "1min"

@router.post("/execute")
async def execute_trading_strategy(request: TradingRequest):
    """
    Executa as estratégias de negociação para o símbolo fornecido.
    """
    try:
        api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
        if not api_key:
            raise HTTPException(status_code=500, detail="Chave da API Alpha Vantage não configurada.")
        
        resultados = executar_estrategias(request.symbol, api_key, request.interval)
        return {"resultados": resultados}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
