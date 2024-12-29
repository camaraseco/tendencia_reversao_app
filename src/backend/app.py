# Arquivo: backend\app.py

from fastapi import FastAPI
from backend.routers import auth, broker, trading

app = FastAPI()

# Incluindo as rotas
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(broker.router, prefix="/broker", tags=["Broker"])
app.include_router(trading.router, prefix="/trading", tags=["Trading"])

@app.get("/")
async def root():
    return {"message": "Bem-vindo ao App de Negociação Automática"}
