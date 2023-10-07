"""empty message

Revision ID: 896c41c41711
Revises: f570f862088a
Create Date: 2023-10-07 16:46:33.252520

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '896c41c41711'
down_revision = 'f570f862088a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('salt', sa.String(length=40), nullable=False))
        batch_op.add_column(sa.Column('is_active', sa.Boolean(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('is_active')
        batch_op.drop_column('salt')

    # ### end Alembic commands ###
