from sqlalchemy.orm import Session
from app.models.model import Product, Category, Pedido, DetallePedido, User
from app.schemas.schema import (
    ProductCreate,
    ProductUpdatePartial,
    CategoryCreate,
    CategoryUpdate,
    PedidoCreate,
    PedidoUpdatePartial
)
from fastapi import HTTPException

#Este archivo es donde hacemos los crud 



# Crear productos
# Crea un producto después de verificar que la categoría exista
def post_product(db: Session, data: ProductCreate):
    # Busca la categoría indicada en los datos del producto si la categoria no esta devuelve categoría no encontrada
    categoria = db.query(Category).filter(
        Category.id == data.id_categoria
    ).first()

    # Verifica que la categoría exista antes de crear el producto
    if not categoria:
        raise HTTPException(
            status_code=404, # aca devuelve un error 404 si la categoria no existe
            detail="Categoría no encontrada"
        )

    # Crea el producto utilizando los datos validados
    product = Product(
        name=data.name,
        stock=data.stock,
        price=data.price,
        id_categoria=data.id_categoria
    )

    # Guarda el producto en la base de datos
    db.add(product)
    db.commit()
    db.refresh(product)

    return product


#Lectura de productos
def get_product(db: Session):
    return db.query(Product).all()


#actualizadcion de precio o stovk de productos
def put_product_partial(db: Session, product_id: int, data: ProductUpdatePartial):
    # Busca el producto que se desea actualizar
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Producto no encontrado"
        )

    # Actualiza el stock solamente si fue enviado
    if data.stock is not None:
        product.stock = data.stock

    # Actualiza el precio solamente si fue enviado
    if data.price is not None:
        product.price = data.price

    db.commit()
    db.refresh(product)

    return product

# Eliminacion de productos
def delete_product(db: Session, product_id: int):
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Producto no encontrado"
        )

    db.delete(product)
    db.commit()

    return product

#Crear categorias
def post_category(db: Session, data: CategoryCreate):
    category = Category(
        name=data.name
    )
    
    db.add(category)
    db.commit()
    db.refresh(category)
    return category 

# Consulta de categorias
def get_category(db: Session):
    return db.query(Category).all()


# Actualizacion de categorias
def put_category(db: Session, category_id: int, data: CategoryUpdate):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException( # Validación de existencia de la categoría
            status_code=404,
            detail="Categoría no encontrada"
        )

    # Actualización de la categoría
    category.name = data.name

    db.commit()
    db.refresh(category)
    return category

# Eliminación de categorias
def delete_category(db: Session, category_id: int):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(
            status_code=404,
            detail="Categoría no encontrada"
        )
    db.delete(category)
    db.commit()
    return category



def post_pedido(db: Session, data: PedidoCreate, user_id: int):
    # Crea el pedido asociado al usuario autenticado
    pedido = Pedido(
        id_usuario=user_id,
        estado_envio=data.estado_envio
    )
    db.add(pedido)
    db.flush()

    for detalle in data.detalles:
        # Busca el producto que el cliente quiere comprar
        producto = db.query(Product).filter(
            Product.id == detalle.id_producto
        ).first()

        if not producto:
            db.rollback()
            raise HTTPException(
                status_code=404,
                detail="Producto no encontrado"
            )

        # Verifica que exista suficiente stock para realizar la compra
        if producto.stock < detalle.cantidad:
            db.rollback()
            raise HTTPException(
                status_code=400,
                detail=f"Stock insuficiente para el producto {producto.name}"
            )

        # Descuenta del stock la cantidad solicitada
        producto.stock -= detalle.cantidad

        # Crea el detalle correspondiente al producto comprado
        detalle_pedido = DetallePedido(
            id_pedido=pedido.id,
            id_producto=detalle.id_producto,
            cantidad=detalle.cantidad
        )
        db.add(detalle_pedido)

    db.commit()
    db.refresh(pedido)
    return pedido

# Crea un detalle de pedido y verifica que el producto tenga stock disponible
def post_detalle_pedido(
    db: Session,
    id_pedido: int,
    id_producto: int,
    cantidad: int,
    user_id: int
):
    # Busca el pedido que se desea modificar
    pedido = db.query(Pedido).filter(
        Pedido.id == id_pedido
    ).first()

    # Verifica que el pedido exista y pertenezca al usuario autenticado
    if not pedido or pedido.id_usuario != user_id:
        raise HTTPException(
            status_code=404,
            detail="Pedido no encontrado"
        )

    # Busca el producto que se desea agregar al pedido
    producto = db.query(Product).filter(
        Product.id == id_producto
    ).first()

    # Verifica que el producto exista
    if not producto:
        raise HTTPException(
            status_code=404,
            detail="Producto no encontrado"
        )

    # Verifica que exista suficiente stock para la cantidad solicitada
    if producto.stock < cantidad:
        raise HTTPException(
            status_code=400,
            detail=f"Stock insuficiente para el producto {producto.name}"
        )

    # Descuenta del stock la cantidad agregada al pedido
    producto.stock -= cantidad

    # Crea el detalle relacionado con el pedido y el producto
    detalle_pedido = DetallePedido(
        id_pedido=id_pedido,
        id_producto=id_producto,
        cantidad=cantidad
    )

    # Guarda los cambios realizados en la base de datos
    db.add(detalle_pedido)
    db.commit()
    db.refresh(detalle_pedido)

    return detalle_pedido


def historial_pedidos(db: Session, user_id: int):
    pedidos = db.query(Pedido).filter(Pedido.id_usuario == user_id).all()

    historial = []

    for pedido in pedidos:
        detalles = db.query(DetallePedido).filter(
            DetallePedido.id_pedido == pedido.id
        ).all()

        historial.append({
            "pedido": pedido,
            "detalles": detalles
        })

    return historial


def put_pedido_estado(db: Session, pedido_id: int, data: PedidoUpdatePartial):
    pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()

    if not pedido:
        raise HTTPException(
            status_code=404,
            detail="Pedido no encontrado"
        )

    pedido.estado_envio = data.estado_envio

    db.commit()
    db.refresh(pedido)

    return pedido

def get_product_category(db: Session):
    # Consulta los productos junto con el nombre de su categoría
    resultado = (
        db.query(
            Product.id,
            Product.name,
            Product.stock,
            Product.price,
            Category.name.label("categoria")
        )
        .join(Category, Product.id_categoria == Category.id)
        .all()
    )

    return [
        {
            "id": producto.id,
            "name": producto.name,
            "stock": producto.stock,
            "price": producto.price,
            "categoria": producto.categoria
        }
        for producto in resultado
    ]

def get_pedido_product(db: Session):
    # Une usuarios, pedidos, detalles y productos para consultar la información de cada compra
    resultado = (
        db.query(
            Pedido.id.label("pedido"),
            User.name.label("usuario"),
            Product.name.label("producto"),
            DetallePedido.cantidad,
            Pedido.estado_envio
        )
        .join(User, Pedido.id_usuario == User.id)
        .join(DetallePedido, Pedido.id == DetallePedido.id_pedido)
        .join(Product, DetallePedido.id_producto == Product.id)
        .all()
    )

    return [
        {
            "pedido": item.pedido,
            "usuario": item.usuario,
            "producto": item.producto,
            "cantidad": item.cantidad,
            "estado_envio": item.estado_envio
        }
        for item in resultado
    ]