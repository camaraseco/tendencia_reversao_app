# Arquivo: src/backend/database.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL de conexão ao banco de dados
DATABASE_URL = "postgresql://postgres:Pocamara.99@localhost:5432/setup_db"

# Engine do SQLAlchemy
engine = create_engine(DATABASE_URL)

# Base para os modelos
Base = declarative_base()

# Sessão para interagir com o banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependência para obter uma sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

