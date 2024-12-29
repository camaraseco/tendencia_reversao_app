from sqlalchemy.orm import Session
from backend.models import Base, engine

def init_db():
    """
    Inicializa o banco de dados e cria as tabelas necessárias.
    """
    print("Inicializando o banco de dados...")
    Base.metadata.create_all(bind=engine)

def get_database_session() -> Session:
    """
    Gera uma sessão de banco de dados para realizar operações.
    """
    from backend.models import SessionLocal
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
