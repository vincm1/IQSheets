"""sub prompt type for formulas and skripts

Revision ID: 58a8fbd20675
Revises: 
Create Date: 2024-01-03 11:28:36.541472

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '58a8fbd20675'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('prompts', schema=None) as batch_op:
        batch_op.add_column(sa.Column('sub_prompt_type', sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('prompts', schema=None) as batch_op:
        batch_op.drop_column('sub_prompt_type')

    # ### end Alembic commands ###