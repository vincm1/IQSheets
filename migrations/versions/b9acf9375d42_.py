"""empty message

Revision ID: b9acf9375d42
Revises: c657c8d28692
Create Date: 2023-04-18 19:52:46.992525

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b9acf9375d42'
down_revision = 'c657c8d28692'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('prompts', schema=None) as batch_op:
        batch_op.add_column(sa.Column('feedback', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('prompts', schema=None) as batch_op:
        batch_op.drop_column('feedback')

    # ### end Alembic commands ###