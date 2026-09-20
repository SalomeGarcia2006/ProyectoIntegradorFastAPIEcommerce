from datetime import datetime, timedelta, timezone

from fastapi import HTTPException
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.models.model import User
from app.schemas.schema import UserRegister, UserLogin


# Configuración utilizada para proteger las contraseñas
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

# Configuración utilizada para generar los tokens JWT
SECRET_KEY = "clave-secreta-ecommerce"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# Convierte una contraseña en un valor cifrado antes de guardarla
def hash_password(password: str):
    return pwd_context.hash(password)


# Comprueba si la contraseña recibida coincide con la contraseña cifrada
def verify_password(password: str, hashed_password: str):
    return pwd_context.verify(password, hashed_password)


# Genera el token JWT que identificará al usuario autenticado
def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({"exp": expire})

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


# Registra un nuevo usuario en el sistema
def register_user(db: Session, data: UserRegister):

    # Comprueba que el correo no esté registrado
    usuario_existente = db.query(User).filter(
        User.email == data.email
    ).first()

    if usuario_existente:
        raise HTTPException(
            status_code=400,
            detail="El correo ya está registrado"
        )

    # Comprueba que el teléfono no esté registrado
    telefono_existente = db.query(User).filter(
        User.phone == data.phone
    ).first()

    if telefono_existente:
        raise HTTPException(
            status_code=400,
            detail="El teléfono ya está registrado"
        )

    # Los registros públicos siempre se crean como cliente
    usuario = User(
        name=data.name,
        email=data.email,
        phone=data.phone,
        role="cliente",
        password=hash_password(data.password)
    )

    db.add(usuario)
    db.commit()
    db.refresh(usuario)

    return usuario


# Comprueba las credenciales y genera el token de acceso
def login_user(db: Session, data: UserLogin):

    usuario = db.query(User).filter(
        User.email == data.email
    ).first()

    if not usuario or not verify_password(
        data.password,
        usuario.password
    ):
        raise HTTPException(
            status_code=401,
            detail="Correo o contraseña incorrectos"
        )

    access_token = create_access_token({
        "sub": str(usuario.id),
        "role": usuario.role
    })

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }