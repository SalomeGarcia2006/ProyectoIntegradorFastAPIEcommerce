# Proyecto Integrador FastAPI - E-commerce

API REST para la administración de productos, categorías, inventario y pedidos de un comercio electrónico.

La aplicación está construida con **FastAPI**, **SQLAlchemy**, **Pydantic**, **SQLite** y autenticación mediante **JWT**.

## Funcionalidades principales

- Registro e inicio de sesión de usuarios.
- Autenticación mediante tokens JWT.
- Roles de usuario: `cliente` y `administrador`.
- CRUD de productos.
- CRUD de categorías.
- Consulta pública del catálogo.
- Creación de pedidos para clientes autenticados.
- Consulta del historial de compras del usuario autenticado.
- Actualización del estado de envío para administradores.
- Validación de precios, stock y cantidades con Pydantic.
- Descuento automático del stock al crear una compra.
- Documentación interactiva con Swagger y ReDoc.
- Base de datos SQLite.

## Requisitos previos

Instala en el equipo:

- Python 3.10 o superior.
- Git.
- Una terminal de Windows: PowerShell o CMD.

Comprueba que Python y Git estén instalados:

```powershell
python --version
git --version
```

## Clonar el proyecto

Desde la carpeta donde quieras guardar el proyecto:

```powershell
git clone URL_DEL_REPOSITORIO
cd ecommerce
```

Reemplaza `URL_DEL_REPOSITORIO` por la URL real del repositorio.

## Crear el entorno virtual

Desde la raíz del proyecto ejecuta:

```powershell
python -m venv venv
```

Esto crea el entorno virtual en la carpeta `venv`.

## Activar el entorno virtual

### PowerShell

```powershell
.\venv\Scripts\Activate.ps1
```

Si PowerShell bloquea la ejecución de scripts, ejecuta una sola vez en esa terminal:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

Después vuelve a activar el entorno:

```powershell
.\venv\Scripts\Activate.ps1
```

### CMD

```cmd
venv\Scripts\activate.bat
```

Cuando el entorno esté activo, la terminal mostrará `(venv)` al inicio de la línea.

## Instalar dependencias

Con el entorno virtual activo:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Las dependencias principales son:

- `fastapi`: construcción de la API.
- `uvicorn`: servidor de desarrollo.
- `sqlalchemy`: conexión y manejo de la base de datos.
- `alembic`: migraciones de la base de datos.
- `pydantic`: validación de datos.
- `python-jose`: generación y validación de JWT.
- `passlib[bcrypt]`: cifrado de contraseñas.
- `python-multipart`: recepción del formulario de login.
- `python-dotenv`: soporte para variables de entorno.

## Base de datos

La aplicación utiliza SQLite mediante el archivo:

```text
ecommerce.db
```

La conexión está definida en `app/database.py`.

En un equipo nuevo, crea las tablas mediante la migración inicial:

```powershell
alembic upgrade head
```

Este comando crea el archivo `ecommerce.db` y las tablas definidas en la migración.

## Crear el usuario administrador

Después de instalar las dependencias y con el entorno virtual activo, ejecuta desde la raíz del proyecto:

```powershell
python crear_admin.py
```

El script crea un administrador si todavía no existe.

### Credenciales del administrador de prueba

```text
Correo: admin@test.com
Contraseña: 12345678
Rol: administrador
```

Estas credenciales son únicamente para desarrollo y demostración. En un entorno real se debe cambiar la contraseña y no guardar credenciales sensibles directamente en el código.

Si el administrador ya existe, el script mostrará un mensaje indicando que no es necesario crearlo nuevamente.

## Ejecutar el proyecto

Con el entorno virtual activo, ejecuta:

```powershell
uvicorn app.main:app --reload
```

La API estará disponible en:

```text
http://127.0.0.1:8000
```

Para detener el servidor presiona `CTRL + C`.

## Documentación Swagger

Abre en el navegador:

```text
http://127.0.0.1:8000/docs
```

También está disponible ReDoc:

```text
http://127.0.0.1:8000/redoc
```

En Swagger puedes probar los endpoints y autenticarte usando el botón **Authorize**.

## Flujo recomendado de uso

### 1. Crear el administrador

Ejecuta:

```powershell
python crear_admin.py
```

### 2. Iniciar sesión como administrador

En Swagger utiliza `POST /auth/login` con formato formulario:

```text
username: admin@test.com
password: 12345678
```

Copia el `access_token` recibido y pulsa **Authorize**. Escribe:

```text
Bearer TU_ACCESS_TOKEN
```

### 3. Crear una categoría

Utiliza `POST /categories/` como administrador:

```json
{
  "name": "Tecnología"
}
```

Guarda el identificador de la categoría creada.

### 4. Crear un producto

Utiliza `POST /products/` como administrador:

```json
{
  "name": "Laptop Lenovo",
  "stock": 10,
  "price": 2500000,
  "id_categoria": 1
}
```

El campo `id_categoria` debe corresponder a una categoría existente.

### 5. Registrar un cliente

Utiliza `POST /auth/register` sin autenticación:

```json
{
  "name": "Cliente de prueba",
  "email": "cliente@test.com",
  "phone": "3000000001",
  "password": "12345678"
}
```

Los registros públicos se crean automáticamente con el rol `cliente`.

### 6. Iniciar sesión como cliente

En `POST /auth/login` utiliza:

```text
username: cliente@test.com
password: 12345678
```

Autoriza Swagger con el token recibido.

### 7. Consultar el catálogo

Estas rutas son públicas:

- `GET /products/`
- `GET /products/category`
- `GET /categories/`

### 8. Crear un pedido

Como cliente autenticado utiliza `POST /pedidos/`:

```json
{
  "estado_envio": "pendiente",
  "detalles": [
    {
      "id_producto": 1,
      "cantidad": 2
    }
  ]
}
```

El pedido debe contener al menos un producto. El sistema verifica la existencia del producto, valida el stock y descuenta automáticamente la cantidad comprada.

### 9. Consultar el historial

Como cliente autenticado utiliza:

```text
GET /pedidos/historial
```

El usuario solo puede consultar sus propios pedidos.

### 10. Actualizar el estado del envío

Como administrador utiliza `PUT /pedidos/{pedido_id}`:

```json
{
  "estado_envio": "enviado"
}
```

Los estados permitidos son:

- `pendiente`
- `enviado`
- `entregado`

## Endpoints disponibles

### Autenticación

| Método | Ruta | Acceso | Descripción |
|---|---|---|---|
| `POST` | `/auth/register` | Público | Registra un cliente nuevo. |
| `POST` | `/auth/login` | Público | Inicia sesión y devuelve un JWT. |

### Productos

| Método | Ruta | Acceso | Descripción |
|---|---|---|---|
| `POST` | `/products/` | Administrador | Crea un producto. |
| `GET` | `/products/` | Público | Lista los productos. |
| `PUT` | `/products/{product_id}` | Administrador | Actualiza precio o stock. |
| `DELETE` | `/products/{product_id}` | Administrador | Elimina un producto. |
| `GET` | `/products/category` | Público | Lista productos con su categoría. |

### Categorías

| Método | Ruta | Acceso | Descripción |
|---|---|---|---|
| `POST` | `/categories/` | Administrador | Crea una categoría. |
| `GET` | `/categories/` | Público | Lista las categorías. |
| `PUT` | `/categories/{category_id}` | Administrador | Actualiza una categoría. |
| `DELETE` | `/categories/{category_id}` | Administrador | Elimina una categoría. |

### Pedidos

| Método | Ruta | Acceso | Descripción |
|---|---|---|---|
| `POST` | `/pedidos/` | Cliente autenticado | Crea un pedido y descuenta stock. |
| `GET` | `/pedidos/historial` | Usuario autenticado | Consulta el historial propio. |
| `PUT` | `/pedidos/{pedido_id}` | Administrador | Actualiza el estado del envío. |
| `GET` | `/pedidos/products` | Administrador | Consulta pedidos con usuarios y productos. |

### Detalles de pedidos

| Método | Ruta | Acceso | Descripción |
|---|---|---|---|
| `POST` | `/detalle_pedidos/` | Usuario autenticado | Agrega un detalle a un pedido propio. |

Esta ruta recibe los parámetros `id_pedido`, `id_producto` y `cantidad`.

## Validaciones principales

La API valida mediante Pydantic:

- `price` debe ser mayor que cero.
- `stock` debe ser mayor que cero.
- `cantidad` debe ser mayor que cero.
- Cada pedido debe tener mínimo un detalle.
- El nombre del producto y la categoría no puede superar 50 caracteres.
- La contraseña debe tener mínimo 8 caracteres.
- El estado del pedido debe ser `pendiente`, `enviado` o `entregado`.
- El producto debe pertenecer a una categoría existente.
- No se permite comprar más unidades que el stock disponible.

## Roles y permisos

### Usuario visitante

Puede:

- Consultar productos.
- Consultar categorías.
- Registrarse.
- Iniciar sesión.

### Cliente autenticado

Puede:

- Crear pedidos.
- Agregar detalles a sus pedidos.
- Consultar su propio historial.
- Consultar el catálogo.

No puede:

- Crear, actualizar o eliminar productos.
- Crear, actualizar o eliminar categorías.
- Cambiar estados de envío.
- Consultar el listado general de pedidos administrativos.

### Administrador

Puede:

- Crear, consultar, actualizar y eliminar productos.
- Gestionar categorías.
- Actualizar estados de pedidos.
- Consultar pedidos con usuarios y productos.
- Consultar el catálogo.

## Estructura principal del proyecto

```text
.
├── alembic.ini
├── alembic/
│   ├── env.py
│   └── versions/
├── app/
│   ├── database.py
│   ├── main.py
│   ├── dependencies/
│   │   ├── database_dependency.py
│   │   └── user_dependencies.py
│   ├── models/
│   │   └── model.py
│   ├── routes/
│   │   └── routes.py
│   ├── schemas/
│   │   └── schema.py
│   └── services/
│       ├── auth_service.py
│       └── service.py
├── crear_admin.py
├── requirements.txt
└── README.md
```

## Comandos rápidos

Instalar y ejecutar en PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
alembic upgrade head
python crear_admin.py
uvicorn app.main:app --reload
```

Instalar y ejecutar en CMD:

```cmd
python -m venv venv
venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt
alembic upgrade head
python crear_admin.py
uvicorn app.main:app --reload
```

## Solución de problemas

### `python` no se reconoce

Instala Python y activa la opción **Add Python to PATH** durante la instalación. Después reinicia la terminal.

### PowerShell no permite activar el entorno

Ejecuta:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

Luego activa nuevamente:

```powershell
.\venv\Scripts\Activate.ps1
```

### No se puede iniciar sesión

Verifica que:

1. El administrador haya sido creado con `python crear_admin.py`.
2. El correo y contraseña sean correctos.
3. El login se envíe como formulario usando los campos `username` y `password`.
4. La aplicación esté ejecutándose.

### Error de módulo no encontrado

Comprueba que el entorno virtual esté activo y reinstala las dependencias:

```powershell
pip install -r requirements.txt
```

### El puerto 8000 está ocupado

Puedes ejecutar la aplicación en otro puerto:

```powershell
uvicorn app.main:app --reload --port 8001
```

En ese caso, Swagger estará en `http://127.0.0.1:8001/docs`.

## Seguridad

Las credenciales incluidas en este README son únicamente para desarrollo. Antes de publicar el proyecto:

- Cambia la contraseña del administrador.
- Usa una clave JWT segura mediante variables de entorno.
- No subas contraseñas ni secretos al repositorio.
- Agrega `ecommerce.db` y `.env` al `.gitignore` si contienen datos reales.
- Usa HTTPS en producción.
