from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum
from datetime import datetime


# Este archivo sirve para controlar los datos que entran y salen de la API


class ProductCreate(BaseModel):
    # Define los datos necesarios para registrar un nuevo producto
    name: str = Field(..., max_length=50) #field obligatorio con longitud máxima de 50 caracteres
    stock: int = Field(..., gt=0) #field obligatorio con valor mayor a 0
    price: float = Field(..., gt=0) #field obligatorio con valor mayor a 0
    id_categoria: int

    # Agrega un ejemplo de producto para facilitar las pruebas en Swagger
    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Laptop Lenovo",
                "stock": 10,
                "price": 2500000,
                "id_categoria": 1
            }
        }
    }

class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=50)
    stock: Optional[int] = Field(None, gt=0)
    price: Optional[float] = Field(None, gt=0)
    id_categoria: Optional[int] = None


class ProductUpdatePartial(BaseModel):
    # Permite actualizar el stock del producto cuando se proporciona este dato
    stock: Optional[int] = Field(None, gt=0)

    # Permite actualizar el precio del producto cuando se proporciona este dato
    price: Optional[float] = Field(None, gt=0)

    # Agrega un ejemplo para facilitar las pruebas de actualización en Swagger
    model_config = {
        "json_schema_extra": {
            "example": {
                "stock": 15,
                "price": 7000
            }
        }
    }
class ProductResponse(BaseModel):
    id: int
    name: str
    stock: int
    price: float
    id_categoria: int

    model_config = {"from_attributes": True}


class CategoryCreate(BaseModel):
    name: str = Field(..., max_length=50)


class CategoryResponse(BaseModel):
    id: int
    name: str

    model_config = {"from_attributes": True}


class CategoryUpdate(BaseModel):
    # Define el nombre que tendrá la categoría al actualizarla
    name: str = Field(..., max_length=50)

class estado_envioEnum(str, Enum):
    pendiente = "pendiente"
    enviado = "enviado"
    entregado = "entregado"


class DetallePedidoCreate(BaseModel):
    id_producto: int
    cantidad: int = Field(..., gt=0)


class PedidoCreate(BaseModel):
    # Define el estado inicial del pedido
    estado_envio: estado_envioEnum

    # Exige que el pedido tenga como mínimo un producto
    detalles: list[DetallePedidoCreate] = Field(..., min_length=1)

    # Agrega un ejemplo de pedido para facilitar las pruebas en Swagger
    model_config = {
        "json_schema_extra": {
            "example": {
                "estado_envio": "pendiente",
                "detalles": [
                    {
                        "id_producto": 2,
                        "cantidad": 2
                    }
                ]
            }
        }
    }


class PedidoUpdatePartial(BaseModel):
    # Define el nuevo estado de envío que tendrá el pedido
    estado_envio: estado_envioEnum

    # Agrega un ejemplo para facilitar las pruebas de actualización en Swagger
    model_config = {
        "json_schema_extra": {
            "example": {
                "estado_envio": "enviado"
            }
        }
    }

class PedidoResponse(BaseModel):
    id: int
    id_usuario: int
    estado_envio: estado_envioEnum

    model_config = {"from_attributes": True}


class DetallePedidoResponse(BaseModel):
    id: int
    id_pedido: int
    id_producto: int
    cantidad: int

    model_config = {"from_attributes": True}


class HistorialPedidoResponse(BaseModel):
    pedido: PedidoResponse
    detalles: list[DetallePedidoResponse]



class UserRegister(BaseModel):
    name: str = Field(..., max_length=50)
    email: str
    phone: str = Field(..., max_length=20)
    password: str = Field(..., min_length=8)

class UserLogin(BaseModel):
    email: str
    password: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: str
    role: str
    created_at: datetime
    is_active: bool

    model_config = {"from_attributes": True}

class Token(BaseModel):
    access_token: str
    token_type: str