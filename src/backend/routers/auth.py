# Arquivo: backend\routers\auth.py

# Arquivo: backend/routers/auth.py
import bcrypt
from fastapi import APIRouter, HTTPException, Depends
from backend.models import SessionLocal, User
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session


router = APIRouter()

# Schemas
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Dependência para obter a sessão do banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/signup", summary="Registrar novo usuário", tags=["Autenticação"])
async def signup(user: UserCreate, db: Session = Depends(get_db)):
    # Verificar se o usuário já existe
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="E-mail já está em uso.")
    
    # Hash da senha
    hashed_password = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt())
    
    # Criar novo usuário
    db_user = User(email=user.email, password=hashed_password.decode("utf-8"))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"message": "Usuário criado com sucesso!", "email": db_user.email}

@router.post("/login", summary="Login de usuário", tags=["Autenticação"])
async def login(user: UserLogin, db: Session = Depends(get_db)):
    # Consultar usuário no banco de dados
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not bcrypt.checkpw(user.password.encode("utf-8"), db_user.password.encode("utf-8")):
        raise HTTPException(status_code=400, detail="Credenciais inválidas")
    
    # Retornar sucesso no login
    return {"message": "Login bem-sucedido", "email": db_user.email}
