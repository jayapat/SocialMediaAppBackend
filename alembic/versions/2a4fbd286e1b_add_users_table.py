"""add users table

Revision ID: 2a4fbd286e1b
Revises: 891e730beba6
Create Date: 2023-07-04 18:59:49.689782

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2a4fbd286e1b'
down_revision = '891e730beba6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable= False),
                    sa.Column('email', sa.String(), nullable= False),
                    sa.Column('password', sa.String(), nullable= False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), 
                              server_default=sa.text("now()"), nullable= False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    
                    )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
