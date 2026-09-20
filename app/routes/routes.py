from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.user_dependencies import get_current_user, require_admin
from app.schemas.schema import (
    ProductCreate,
    ProductUpdatePartial,
    ProductResponse,
    CategoryResponse,
    CategoryCreate,
    CategoryUpdate,
    PedidoCreate,
    PedidoResponse,
    PedidoUpdatePartial,
    DetallePedidoResponse,
    HistorialPedidoResponse,
    UserRegister,
    UserLogin,
    Token,
    UserResponse
)

from app.services.service import (
    post_product,
    get_product,
    put_product_partial,
    delete_product,
    post_category,
    get_category,
    put_category,
    delete_category,
    post_pedido,
    post_detalle_pedido,
    historial_pedidos,
    put_pedido_estado,
    get_product_category,
    get_pedido_product,
)

from app.services.auth_service import register_user, login_user


# Este router agrupa las rutas relacionadas con la autenticación
auth_router = APIRouter(prefix="/auth", tags=["Autenticación"])

# Este router agrupa todas las rutas relacionadas con los productos
router = APIRouter(prefix="/products", tags=["Products"])

# Este router agrupa todas las rutas relacionadas con las categorías
category_router = APIRouter(prefix="/categories", tags=["Categories"])

# Este router agrupa todas las rutas relacionadas con los pedidos
pedido_router = APIRouter(prefix="/pedidos", tags=["Pedidos"])

# Este router agrupa las rutas relacionadas con los detalles de los pedidos
DetallePedido_router = APIRouter(prefix="/detalle_pedidos", tags=["DetallePedidos"])


# Permite crear una nueva categoría para organizar los productos del catálogo
@category_router.post("/", response_model=CategoryResponse)
def crear_categoria(
    data: CategoryCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_admin)
):
    return post_category(db, data)


# Permite consultar todas las categorías registradas en el sistema
@category_router.get("/", response_model=list[CategoryResponse])
def leer_categorias(
    db: Session = Depends(get_db)
):
    return get_category(db)


# Permite actualizar el nombre de una categoría existente
@category_router.put("/{category_id}", response_model=CategoryResponse)
def actualizar_categoria_parcial(
    category_id: int,
    data: CategoryUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(require_admin)
):
    return put_category(db, category_id, data)


# Permite eliminar una categoría utilizando su identificador
@category_router.delete("/{category_id}", response_model=CategoryResponse)
def eliminar_categoria(
    category_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_admin)
):
    return delete_category(db, category_id)


# Permite crear un nuevo producto utilizando los datos recibidos en ProductCreate
@router.post("/", response_model=ProductResponse)
def crear_producto(
    data: ProductCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_admin)
):
    return post_product(db, data)


# Permite consultar y obtener todos los productos registrados
@router.get("/", response_model=list[ProductResponse])
def leer_productos(
    db: Session = Depends(get_db)
):
    return get_product(db)


# Permite actualizar el precio y el stock de un producto existente
@router.put("/{product_id}", response_model=ProductResponse)
def actualizar_producto_parcial(
    product_id: int,
    data: ProductUpdatePartial,
    db: Session = Depends(get_db),
    current_user = Depends(require_admin)
):
    return put_product_partial(db, product_id, data)


# Permite eliminar un producto utilizando su identificador
@router.delete("/{product_id}", response_model=ProductResponse)
def eliminar_producto(
    product_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_admin)
):
    return delete_product(db, product_id)


# Permite crear un nuevo pedido junto con sus productos
# PedidoCreate exige como mínimo un detalle de producto
@pedido_router.post("/", response_model=PedidoResponse)
def crear_pedido(
    data: PedidoCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return post_pedido(db, data, current_user.id)


# Permite crear un detalle de pedido de forma independiente
# indicando el pedido, producto y cantidad
@DetallePedido_router.post("/", response_model=DetallePedidoResponse)
def crear_detalle_pedido(
    id_pedido: int,
    id_producto: int,
    cantidad: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Crea el detalle utilizando el usuario autenticado para validar la propiedad del pedido
    return post_detalle_pedido(
        db,
        id_pedido,
        id_producto,
        cantidad,
        current_user.id
    )


# Permite consultar el historial de compras de un usuario
# utilizando el identificador del usuario
@pedido_router.get(
    "/historial",
    response_model=list[HistorialPedidoResponse]
)
def leer_historial(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return historial_pedidos(db, current_user.id)

# Permite actualizar únicamente el estado de envío de un pedido
@pedido_router.put(
    "/{pedido_id}",
    response_model=PedidoResponse
)
def actualizar_estado_pedido(
    pedido_id: int,
    data: PedidoUpdatePartial,
    db: Session = Depends(get_db),
    current_user = Depends(require_admin)
):
    return put_pedido_estado(db, pedido_id, data)


@router.get("/category")
def product_category(db: Session = Depends(get_db)):
    # Obtiene los productos relacionados con sus categorías
    return get_product_category(db)


@pedido_router.get("/products")
def pedido_product(
    db: Session = Depends(get_db),
    current_user = Depends(require_admin)
):
    # Consulta la información de los pedidos solamente para usuarios administradores
    return get_pedido_product(db)


# Permite registrar un nuevo usuario
@auth_router.post("/register", response_model=UserResponse)
def registrar_usuario(
    data: UserRegister,
    db: Session = Depends(get_db)
):
    return register_user(db, data)


# Permite iniciar sesión y obtener un token JWT
@auth_router.post("/login", response_model=Token)
def iniciar_sesion(
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    data = UserLogin(
        email=username,
        password=password
    )
    return login_user(db, data)