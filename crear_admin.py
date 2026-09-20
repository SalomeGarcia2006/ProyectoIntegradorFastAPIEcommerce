from app.database import SessionLocal
from app.models.model import User
from app.services.auth_service import hash_password


db = SessionLocal()

admin_existente = db.query(User).filter(
    User.email == "admin@test.com"
).first()

if admin_existente:
    print("El usuario administrador ya existe.")
else:
    administrador = User(
        name="Administrador",
        email="admin@test.com",
        phone="3000000000",
        role="administrador",
        password=hash_password("12345678")
    )

    db.add(administrador)
    db.commit()
    db.refresh(administrador)

    print("Usuario administrador creado correctamente.")
    print(f"ID: {administrador.id}")
    print(f"Correo: {administrador.email}")
    print(f"Rol: {administrador.role}")

db.close()