# Arquivo: src/backend/populate_db.py

from datetime import datetime
from backend.database import SessionLocal
from backend.models import User, Operacao, TradeHistory

def popular_banco_de_dados():
    """
    Popula o banco de dados com usuários e operações de teste.
    """
    print("Iniciando população do banco de dados...")
    # Sessão do banco
    db = SessionLocal()

    try:
        # Inserir usuário de teste
        usuario_teste = User(
            email="usuario_teste@example.com",
            hashed_password="hashed_password_teste",
            is_active=1,
            created_at=datetime.now()
        )
        db.add(usuario_teste)
        db.commit()
        db.refresh(usuario_teste)  # Atualiza o objeto para incluir o ID gerado
        print(f"Usuário criado: {usuario_teste.email}")

        # Inserir operação vinculada ao usuário
        operacao_teste = Operacao(
            tipo_operacao="COMPRA",
            preco_execucao=150.00,
            motivo="Take Profit",
            data_hora=datetime.now(),
            quantidade=10,
            user_id=usuario_teste.id  # Vincula ao usuário
        )
        db.add(operacao_teste)
        db.commit()
        db.refresh(operacao_teste)  # Atualiza o objeto para incluir o ID gerado
        print(f"Operação criada: {operacao_teste.tipo_operacao}, Preço: {operacao_teste.preco_execucao}")

        # Inserir histórico vinculado à operação
        historico_teste = TradeHistory(
            operacao_id=operacao_teste.id,
            motivo="Take Profit",
            data_hora=datetime.now()
        )
        db.add(historico_teste)
        db.commit()
        print("Histórico de operações criado com sucesso!")

        print("Banco de dados populado com sucesso!")
    except Exception as e:
        print(f"Erro ao popular banco de dados: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    popular_banco_de_dados()
