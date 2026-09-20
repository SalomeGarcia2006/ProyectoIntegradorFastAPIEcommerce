from fastapi import FastAPI


from app.routes.routes import (
    router,
    category_router,
    pedido_router,
    DetallePedido_router,
    auth_router
)

from fastapi import FastAPI

from app.routes.routes import (
    router,
    category_router,
    pedido_router,
    DetallePedido_router,
    auth_router
)


# Crea la aplicación principal de FastAPI
app = FastAPI(
    title="Sistema de Gestión de Inventario y Pedidos"
)


# Incluye las rutas relacionadas con las categorías
app.include_router(category_router)

# Incluye las rutas relacionadas con los productos
app.include_router(router)

# Incluye las rutas relacionadas con los pedidos
app.include_router(pedido_router)

# Incluye las rutas relacionadas con los detalles de los pedidos
app.include_router(DetallePedido_router)

# Incluye las rutas relacionadas con la autenticación
app.include_router(auth_router)