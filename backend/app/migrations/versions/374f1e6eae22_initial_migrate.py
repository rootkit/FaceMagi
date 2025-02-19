"""initial migrate

Revision ID: 374f1e6eae22
Revises: 
Create Date: 2020-03-07 00:29:05.377468

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '374f1e6eae22'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('config',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('key', sa.String(length=64), nullable=False),
    sa.Column('value', sa.String(length=128), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('key')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('openId', sa.String(length=50), nullable=False),
    sa.Column('brandModel', sa.String(length=50), nullable=False),
    sa.Column('screen', sa.String(length=20), nullable=True),
    sa.Column('language', sa.String(length=40), nullable=True),
    sa.Column('version', sa.String(length=40), nullable=True),
    sa.Column('platformSystem', sa.String(length=40), nullable=True),
    sa.Column('appleUser', sa.String(length=50), nullable=True),
    sa.Column('cashbox', sa.Numeric(precision=8, scale=2), nullable=True),
    sa.Column('cTimestamp', sa.DateTime(), nullable=True),
    sa.Column('level', sa.Integer(), nullable=True),
    sa.Column('levelExpTimestamp', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('openId')
    )
    op.create_index(op.f('ix_users_cTimestamp'), 'users', ['cTimestamp'], unique=False)
    op.create_table('orders',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('userId', sa.Integer(), nullable=True),
    sa.Column('status', sa.Integer(), nullable=True),
    sa.Column('prepayId', sa.String(length=64), nullable=False),
    sa.Column('cTimestamp', sa.DateTime(), nullable=True),
    sa.Column('uTimestamp', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['userId'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('prepayId')
    )
    op.create_index(op.f('ix_orders_cTimestamp'), 'orders', ['cTimestamp'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_orders_cTimestamp'), table_name='orders')
    op.drop_table('orders')
    op.drop_index(op.f('ix_users_cTimestamp'), table_name='users')
    op.drop_table('users')
    op.drop_table('config')
    # ### end Alembic commands ###
