# Arquivo: src/backend/app.py

# Arquivo: src/backend/app.py

from fastapi import FastAPI, HTTPException, Request, Depends
from sqlalchemy.orm import Session
from backend.models import User
from backend.database import get_db, SessionLocal
from utils import enviar_email
from datetime import datetime

app = FastAPI()

# Dependência para criar sessões do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/finalizar-operacao/")
async def finalizar_operacao(request: Request, db: Session = Depends(get_db)):
    """
    Finaliza uma operação e envia notificação por email.

    Corpo esperado:
    {
        "user_id": 1,
        "tipo_operacao": "COMPRA",
        "preco_execucao": 100.0,
        "motivo": "Stop Loss"
    }
    """
    body = await request.json()

    user_id = body.get("user_id")
    tipo_operacao = body.get("tipo_operacao")
    preco_execucao = body.get("preco_execucao")
    motivo = body.get("motivo")

    if not all([user_id, tipo_operacao, preco_execucao, motivo]):
        raise HTTPException(status_code=400, detail="Faltam parâmetros obrigatórios")

    # Processar e salvar a operação
    ...


    # Buscar o e-mail do usuário pelo ID
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    email_usuario = user.email
    data_hora = datetime.now()

    # Enviar o e-mail
    enviar_email(tipo_operacao, preco_execucao, motivo, data_hora, email_usuario)

    return {"message": "Operação finalizada e notificação enviada com sucesso!"}
