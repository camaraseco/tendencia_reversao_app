# Arquivos : src\backend\models.py

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from backend.database import Base  # Importa o Base corretamente

# Modelo para a tabela de usuários
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Integer, default=1)
    broker_account = Column(String, nullable=True)  # Número da conta da corretora
    broker_password = Column(String, nullable=True)  # Senha da conta da corretora
    created_at = Column(DateTime)
    operacoes = relationship("Operacao", back_populates="usuario")  # Relacionamento com Operacao

# Modelo para a tabela de operações
class Operacao(Base):
    __tablename__ = "operacoes"

    id = Column(Integer, primary_key=True, index=True)
    tipo_operacao = Column(String, nullable=False)  # 'COMPRA' ou 'VENDA'
    preco_execucao = Column(Float, nullable=False)
    motivo = Column(String, nullable=False)  # 'Stop Loss' ou 'Take Profit'
    data_hora = Column(DateTime, nullable=False)
    quantidade = Column(Float, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))  # Referência para a tabela de usuários
    usuario = relationship("User", back_populates="operacoes")  # Relacionamento com User
    trade_history = relationship("TradeHistory", back_populates="operacao")  # Relacionamento com TradeHistory

# Modelo para o histórico de operações
class TradeHistory(Base):
    __tablename__ = "trade_history"

    id = Column(Integer, primary_key=True, index=True)
    operacao_id = Column(Integer, ForeignKey("operacoes.id"))  # Referência para a tabela Operacao
    motivo = Column(String, nullable=False)  # 'Stop Loss' ou 'Take Profit'
    data_hora = Column(DateTime, nullable=False)
    operacao = relationship("Operacao", back_populates="trade_history")  # Relacionamento com Operacao
