"""empty message

Revision ID: d76238233275
Revises: c308800b44ad
Create Date: 2023-04-18 19:21:11.505936

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'd76238233275'
down_revision = 'c308800b44ad'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('favorites')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('favorites',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('provider', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('favorite_type', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('method', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('command', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('prompt', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('favorite_date', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='favorites_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='favorites_pkey')
    )
    # ### end Alembic commands ###