"""add_timestamp_column

Revision ID: 4b3bbe69293b
Revises: 80bfa1370669
Create Date: 2019-06-29 19:39:21.130837

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4b3bbe69293b'
down_revision = '80bfa1370669'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('_created_at', sa.DateTime(), nullable=False))
    op.add_column('user', sa.Column('_updated_at', sa.DateTime(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', '_updated_at')
    op.drop_column('user', '_created_at')
    # ### end Alembic commands ###