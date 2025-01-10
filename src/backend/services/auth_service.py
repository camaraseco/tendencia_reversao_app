# Arquivo: src\backend\services\auth_service.py

import jwt
import bcrypt
from datetime import datetime, timedelta
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from backend.models import User
from backend.database import get_database_session

# Configurações de segurança
SECRET_KEY = "sua_chave_secreta_super_segura"  # Substitua por uma variável de ambiente em produção
ALGORITHM = "HS256"
TOKEN_EXPIRATION_MINUTES = 60


def hash_password(password: str) -> str:
    """
    Gera o hash de uma senha utilizando bcrypt.
    """
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica se uma senha está correta comparando com o hash armazenado.
    """
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))


def create_access_token(data: dict) -> str:
    """
    Cria um token de acesso JWT com os dados fornecidos.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRATION_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def register_user(email: str, password: str, db: Session):
    """
    Registra um novo usuário no banco de dados.
    """
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuário já cadastrado."
        )

    hashed_password = hash_password(password)
    new_user = User(email=email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "Usuário registrado com sucesso."}


def authenticate_user(email: str, password: str, db: Session):
    """
    Autentica o usuário com base no email e senha fornecidos.
    """
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos."
        )

    access_token = create_access_token({"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


def login(form_data: OAuth2PasswordRequestForm, db: Session = Depends(get_database_session)):
    """
    Realiza o login do usuário com base no formulário de autenticação.
    """
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Credenciais inválidas")

    token = create_access_token({"sub": user.email, "user_id": user.id})
    return {"access_token": token, "token_type": "bearer"}
