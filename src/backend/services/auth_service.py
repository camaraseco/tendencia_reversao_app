import jwt
import bcrypt
from datetime import datetime, timedelta
from backend.models import User
from src.utils import get_database_session
from fastapi import HTTPException, status

# Chave secreta para gerar tokens JWT
SECRET_KEY = "sua_chave_secreta_super_segura"
ALGORITHM = "HS256"
TOKEN_EXPIRATION_MINUTES = 60

def hash_password(password: str) -> str:
    """
    Gera o hash de uma senha.
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica se uma senha está correta comparando com o hash armazenado.
    """
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def create_access_token(data: dict) -> str:
    """
    Cria um token de acesso JWT com os dados fornecidos.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRATION_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def register_user(email: str, password: str):
    """
    Registra um novo usuário no sistema.
    """
    db = get_database_session()

    # Verificar se o usuário já existe
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuário já cadastrado."
        )

    # Criar novo usuário
    hashed_password = hash_password(password)
    new_user = User(email=email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "Usuário registrado com sucesso."}

def authenticate_user(email: str, password: str):
    """
    Autentica o usuário com base no e-mail e senha fornecidos.
    """
    db = get_database_session()

    # Buscar usuário no banco de dados
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos."
        )

    # Gerar token JWT
    access_token = create_access_token({"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
