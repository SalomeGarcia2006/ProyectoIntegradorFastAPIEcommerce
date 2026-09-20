"""Migracion inicial ecommerce

Revision ID: 7e1432c80903
Revises:
Create Date: 2026-09-19 01:11:10.938459

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# Identificadores utilizados por Alembic para controlar la migración
revision: str = '7e1432c80903'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Crea las tablas iniciales de la aplicación."""

    # Crea la tabla de usuarios
    op.create_table(
        'usuarios',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=50), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('phone', sa.String(length=20), nullable=False),
        sa.Column('role', sa.String(length=20), nullable=False),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('phone')
    )

    # Crea la tabla de categorías
    op.create_table(
        'categorias',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=50), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # Crea la tabla de productos y la relaciona con categorías
    op.create_table(
        'productos',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=50), nullable=False),
        sa.Column('stock', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('price', sa.Float(), nullable=False),
        sa.Column('id_categoria', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ['id_categoria'],
            ['categorias.id']
        ),
        sa.PrimaryKeyConstraint('id')
    )

    # Crea la tabla de pedidos y la relaciona con usuarios
    op.create_table(
        'pedidos',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('id_usuario', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('estado_envio', sa.String(length=20), nullable=False),
        sa.ForeignKeyConstraint(
            ['id_usuario'],
            ['usuarios.id']
        ),
        sa.PrimaryKeyConstraint('id')
    )

    # Crea la tabla de detalles y establece sus relaciones
    # con pedidos y productos
    op.create_table(
        'detalle_pedidos',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('id_pedido', sa.Integer(), nullable=True),
        sa.Column('id_producto', sa.Integer(), nullable=True),
        sa.Column('cantidad', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ['id_pedido'],
            ['pedidos.id']
        ),
        sa.ForeignKeyConstraint(
            ['id_producto'],
            ['productos.id']
        ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    """Elimina las tablas creadas por la migración inicial."""

    # Se eliminan primero las tablas que dependen de otras tablas
    op.drop_table('detalle_pedidos')
    op.drop_table('pedidos')
    op.drop_table('productos')
    op.drop_table('categorias')
    op.drop_table('usuarios')