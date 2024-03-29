"""Adicionando coluna password_hash na tabela user

Revision ID: e7bab2253169
Revises: 071ee07b9ee6
Create Date: 2024-01-05 13:24:51.050442

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e7bab2253169'
down_revision = '071ee07b9ee6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('password_hash', sa.String(length=128), nullable=False))
        batch_op.create_index(batch_op.f('ix_user_password_hash'), ['password_hash'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_password_hash'))
        batch_op.drop_column('password_hash')

    # ### end Alembic commands ###
