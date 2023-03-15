"""method in Favorite

Revision ID: bc0cc3706aa8
Revises: f9896190aa5d
Create Date: 2023-03-15 17:35:17.108476

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bc0cc3706aa8'
down_revision = 'f9896190aa5d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('favorites', schema=None) as batch_op:
        batch_op.add_column(sa.Column('provider', sa.String(), nullable=False))
        batch_op.add_column(sa.Column('method', sa.String(), nullable=False))
        batch_op.drop_column('favorite_method')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('favorites', schema=None) as batch_op:
        batch_op.add_column(sa.Column('favorite_method', sa.VARCHAR(), autoincrement=False, nullable=False))
        batch_op.drop_column('method')
        batch_op.drop_column('provider')

    # ### end Alembic commands ###
