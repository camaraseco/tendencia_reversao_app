# Arquivo: backend\app.py

from fastapi import FastAPI
from backend.routers import auth, broker, trading
from fastapi import FastAPI, HTTPException, Request
from backend.routers import auth, broker, trading
from utils import enviar_email
from datetime import datetime

app = FastAPI()

# Incluindo as rotas
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(broker.router, prefix="/broker", tags=["Broker"])
app.include_router(trading.router, prefix="/trading", tags=["Trading"])

@app.get("/")
async def root():
    return {"message": "Bem-vindo ao App de Negociação Automática"}

@app.post("/finalizar-operacao/")
async def finalizar_operacao(request: Request):
    """
    Finaliza uma operação e envia notificação por email.

    Corpo esperado:
    {
        "tipo_operacao": "COMPRA" ou "VENDA",
        "preco_execucao": 100.0,
        "motivo": "Stop Loss" ou "Take Profit",
        "email_usuario": "usuario@exemplo.com"
    }
    """
    body = await request.json()

    tipo_operacao = body.get("tipo_operacao")
    preco_execucao = body.get("preco_execucao")
    motivo = body.get("motivo")
    email_usuario = body.get("email_usuario")

    if not all([tipo_operacao, preco_execucao, motivo, email_usuario]):
        raise HTTPException(status_code=400, detail="Faltam parâmetros obrigatórios")

    data_hora = datetime.now()
    enviar_email(tipo_operacao, preco_execucao, motivo, data_hora, email_usuario)

    return {"message": "Operação finalizada e notificação enviada com sucesso!"}