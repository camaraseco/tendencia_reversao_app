from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from backend.models import User
from backend.models import SessionLocal
import requests

router = APIRouter()

# Dependência para obter sessão do banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Schemas
class BrokerConnectionRequest(BaseModel):
    broker_account: str
    broker_password: str

class OrderRequest(BaseModel):
    symbol: str
    action: str  # "COMPRA" ou "VENDA"
    volume: float


@router.post("/connect")
async def connect_to_broker(request: BrokerConnectionRequest, user_id: int, db: Session = Depends(get_db)):
    """
    Conecta a conta do usuário à corretora.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    # Simular conexão à corretora
    # Aqui você implementaria a integração com a API da corretora
    if request.broker_account and request.broker_password:
        user.broker_account = request.broker_account
        user.broker_password = request.broker_password
        db.commit()
        return {"message": "Conectado à corretora com sucesso"}
    else:
        raise HTTPException(status_code=400, detail="Credenciais inválidas")


@router.post("/execute_order")
async def execute_order(request: OrderRequest, user_id: int, db: Session = Depends(get_db)):
    """
    Executa uma ordem de compra ou venda na conta conectada da corretora.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    if not user.broker_account or not user.broker_password:
        raise HTTPException(status_code=400, detail="Usuário não está conectado a uma corretora")

    # Simular envio de ordem para a API da corretora
    # Aqui você implementaria a lógica de integração real com a API da corretora
    order_result = {
        "symbol": request.symbol,
        "action": request.action,
        "volume": request.volume,
        "status": "success",  # Esta linha deve vir da resposta da corretora
    }
    return {"message": "Ordem executada com sucesso", "order_result": order_result}
