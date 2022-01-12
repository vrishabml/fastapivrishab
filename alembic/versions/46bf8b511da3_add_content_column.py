"""add content column

Revision ID: 46bf8b511da3
Revises: 99738793d551
Create Date: 2022-01-12 10:58:30.420814

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '46bf8b511da3'
down_revision = '99738793d551'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content',sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts','content')
    pass
