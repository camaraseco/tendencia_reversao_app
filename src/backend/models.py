from sqlalchemy import Column, Integer, String, Float, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

# URL de conexão ao banco de dados
DATABASE_URL = "postgresql://postgres:Pocamara.99@localhost:5432/setup_db"  # Você pode trocar para outro banco, como PostgreSQL ou MySQL

# Configuração do motor do banco de dados
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Modelo para a tabela de usuários
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    broker_account = Column(String, nullable=True)  # Número da conta da corretora
    broker_password = Column(String, nullable=True)  # Senha da conta da corretora

# Modelo para o histórico de operações
class TradeHistory(Base):
    __tablename__ = "trade_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)  # Referência ao ID do usuário
    symbol = Column(String, nullable=False)  # Símbolo do ativo, ex: "AAPL"
    action = Column(String, nullable=False)  # Tipo de operação: "Compra" ou "Venda"
    volume = Column(Float, nullable=False)  # Quantidade negociada
    price = Column(Float, nullable=False)  # Preço por unidade no momento da operação
    timestamp = Column(DateTime, nullable=False)  # Data e hora da operação
