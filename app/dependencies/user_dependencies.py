from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.model import User
from app.services.auth_service import SECRET_KEY, ALGORITHM


# Indica a FastAPI dónde debe solicitar el token JWT
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# Obtiene y valida el usuario identificado por el token JWT
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("sub")

        if user_id is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    usuario = db.query(User).filter(
        User.id == int(user_id)
    ).first()

    if usuario is None:
        raise credentials_exception

    return usuario



# Verifica que el usuario autenticado tenga permisos de administrador
def require_admin(
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "administrador":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos de administrador"
        )

    return current_user