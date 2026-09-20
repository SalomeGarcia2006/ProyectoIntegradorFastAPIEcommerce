from datetime import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime, Float
from app.database import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String(20), unique=True, nullable=False)
    role = Column(String(20), nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

    # Relaciona un usuario con todos sus pedidos
    pedidos = relationship("Pedido", back_populates="usuario")


class Product(Base):
    __tablename__ = "productos"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    stock = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    price = Column(Float, nullable=False)
    id_categoria = Column(Integer, ForeignKey("categorias.id"))

    # Relaciona el producto con su categoría
    categoria = relationship("Category", back_populates="productos")

    # Relaciona el producto con los detalles de pedidos donde aparece
    detalles = relationship("DetallePedido", back_populates="producto")


class Category(Base):
    __tablename__ = "categorias"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

    # Relaciona una categoría con todos sus productos
    productos = relationship("Product", back_populates="categoria")


class Pedido(Base):
    __tablename__ = "pedidos"
    id = Column(Integer, primary_key=True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    estado_envio = Column(String(20), nullable=False)

    # Relaciona cada pedido con el usuario que lo realizó
    usuario = relationship("User", back_populates="pedidos")

    # Relaciona un pedido con todos los detalles que contiene
    detalles = relationship("DetallePedido", back_populates="pedido")


class DetallePedido(Base):
    __tablename__ = "detalle_pedidos"
    id = Column(Integer, primary_key=True)
    id_pedido = Column(Integer, ForeignKey("pedidos.id"))
    id_producto = Column(Integer, ForeignKey("productos.id"))
    cantidad = Column(Integer, nullable=False)

    # Relaciona cada detalle con el pedido al que pertenece
    pedido = relationship("Pedido", back_populates="detalles")

    # Relaciona cada detalle con el producto comprado
    producto = relationship("Product", back_populates="detalles")