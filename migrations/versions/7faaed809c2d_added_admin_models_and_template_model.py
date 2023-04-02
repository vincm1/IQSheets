"""added admin models and template model

Revision ID: 7faaed809c2d
Revises: 4a6d02548bfe
Create Date: 2023-03-31 14:10:31.509877

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7faaed809c2d'
down_revision = '4a6d02548bfe'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_admin', sa.Boolean(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('is_admin')

    # ### end Alembic commands ###