"""add last few columns to the posts tables

Revision ID: 8ecc3398658c
Revises: ef7d36df3e74
Create Date: 2023-07-04 19:17:34.615755

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8ecc3398658c'
down_revision = 'ef7d36df3e74'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable= False, server_default="TRUE"),)
    op.add_column('posts',sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable= False, server_default= sa.text("NOW()")),)
    pass


def downgrade() -> None:
    op.drop_column('posts','published')
    op.drop_column('posts','created_at')
    pass
