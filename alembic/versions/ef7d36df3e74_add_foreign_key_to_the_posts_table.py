"""add foreign key to the posts table

Revision ID: ef7d36df3e74
Revises: 2a4fbd286e1b
Create Date: 2023-07-04 19:09:00.037466

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ef7d36df3e74'
down_revision = '2a4fbd286e1b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('posts_users_id', sa.Integer(), nullable=False))
    op.create_foreign_key("posts_users_fk", source_table="posts", referent_table="users", local_cols=["posts_users_id"], remote_cols= ['id'], ondelete= "CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint("posts_users_fk", table_name="posts")
    op.drop_column("posts", 'posts_users_id')
    pass
