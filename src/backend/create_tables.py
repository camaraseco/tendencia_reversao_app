from database import Base, engine
from models import User, Operacao

print("Criando tabelas...")
Base.metadata.create_all(bind=engine)
print("Tabelas criadas com sucesso.")
