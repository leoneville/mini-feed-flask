"""criando tabela post

Revision ID: 12636259b211
Revises: b06be1f08110
Create Date: 2024-01-10 06:55:45.795383

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '12636259b211'
down_revision = 'b06be1f08110'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('post',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('text', sa.UnicodeText(), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('post')
    # ### end Alembic commands ###
