# Arquivo: src/backend/create_tables.py

from backend.database import Base, engine
from backend.models import User, Operacao, TradeHistory  # Importar modelos corretamente

def criar_tabelas():
    print("Criando tabelas...")
    Base.metadata.create_all(engine)
    print("Tabelas criadas com sucesso.")

if __name__ == "__main__":
    criar_tabelas()
