# Arquivo: tests/test_populate_db.py

import pytest
from backend.database import SessionLocal
from backend.models import User, Operacao, TradeHistory

def test_popular_banco():
    db = SessionLocal()

    # Verifica se o usuário foi criado
    usuario = db.query(User).filter_by(email="usuario_teste@example.com").first()
    assert usuario is not None, "Usuário não foi criado corretamente."

    # Verifica se a operação foi criada
    operacao = db.query(Operacao).filter_by(user_id=usuario.id).first()
    assert operacao is not None, "Operação não foi criada corretamente."

    # Verifica se o histórico foi criado
    historico = db.query(TradeHistory).filter_by(operacao_id=operacao.id).first()
    assert historico is not None, "Histórico não foi criado corretamente."

    db.close()
