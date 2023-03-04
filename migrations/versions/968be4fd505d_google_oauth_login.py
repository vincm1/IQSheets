"""google oauth login

Revision ID: 968be4fd505d
Revises: 38b548091a2a
Create Date: 2023-03-04 16:17:08.215647

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '968be4fd505d'
down_revision = '38b548091a2a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('flask_dance_oauth')
    with op.batch_alter_table('OAuth', schema=None) as batch_op:
        batch_op.add_column(sa.Column('provider_user_id', sa.String(length=256), nullable=False))
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('id', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('provider', sa.String(length=50), nullable=False))
        batch_op.add_column(sa.Column('created_at', sa.DateTime(), nullable=False))
        batch_op.add_column(sa.Column('token', sa.JSON(), nullable=False))
        batch_op.create_unique_constraint(None, ['provider_user_id'])
        batch_op.create_foreign_key(None, 'users', ['user_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('OAuth', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_column('token')
        batch_op.drop_column('created_at')
        batch_op.drop_column('provider')
        batch_op.drop_column('id')
        batch_op.drop_column('user_id')
        batch_op.drop_column('provider_user_id')

    op.create_table('flask_dance_oauth',
    sa.Column('provider_user_id', sa.VARCHAR(length=256), autoincrement=False, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('provider', sa.VARCHAR(length=50), autoincrement=False, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('token', postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='flask_dance_oauth_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='flask_dance_oauth_pkey'),
    sa.UniqueConstraint('provider_user_id', name='flask_dance_oauth_provider_user_id_key')
    )
    # ### end Alembic commands ###
