"""changed pw column

Revision ID: 564b1fe557cb
Revises: 
Create Date: 2023-02-21 16:14:21.388713

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '564b1fe557cb'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('password_hash', sa.String(), nullable=False))
        batch_op.drop_column('passwort_hash')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('passwort_hash', sa.VARCHAR(), autoincrement=False, nullable=False))
        batch_op.drop_column('password_hash')

    # ### end Alembic commands ###
