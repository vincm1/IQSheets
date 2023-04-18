"""empty message

Revision ID: a4dac4dcd78c
Revises: d76238233275
Create Date: 2023-04-18 19:35:03.347187

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a4dac4dcd78c'
down_revision = 'd76238233275'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('prompts', schema=None) as batch_op:
        batch_op.add_column(sa.Column('request', sa.String(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('prompts', schema=None) as batch_op:
        batch_op.drop_column('request')

    # ### end Alembic commands ###