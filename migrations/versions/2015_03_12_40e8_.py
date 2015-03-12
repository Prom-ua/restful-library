"""empty message

Revision ID: 40e89f69741
Revises: None
Create Date: 2015-03-12 13:46:37.893976

"""

revision = '40e89f69741'
down_revision = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


def upgrade():
    op.create_table(
        'user',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(length=120), nullable=False),
        sa.Column('password', sa.String(length=80), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_table(
        'book',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'author',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=50), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'authors_books',
        sa.Column('author_id', sa.Integer(), nullable=True),
        sa.Column('book_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['author_id'], ['author.id'], ),
        sa.ForeignKeyConstraint(['book_id'], ['book.id'], )
    )
    op.create_table(
        'api_token',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('uuid', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('date_created', sa.DateTime(), nullable=True),
        sa.Column('date_expiry', sa.DateTime(), nullable=False),
        sa.Column('created_by_id', sa.Integer(), nullable=True),
        sa.Column('description', sa.String(length=300), nullable=True),
        sa.ForeignKeyConstraint(['created_by_id'], ['user.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('api_token')
    op.drop_table('authors_books')
    op.drop_table('author')
    op.drop_table('book')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
