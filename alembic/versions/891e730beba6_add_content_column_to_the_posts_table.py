"""add content column to the posts table

Revision ID: 891e730beba6
Revises: 4e0837c3f339
Create Date: 2023-07-04 18:42:54.415015

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '891e730beba6'
down_revision = '4e0837c3f339'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts','content')
    pass
