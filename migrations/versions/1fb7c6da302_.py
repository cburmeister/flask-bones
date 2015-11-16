"""Initial migration

Revision ID: 1fb7c6da302
Revises: None
Create Date: 2015-11-16 17:19:00.332397

"""

# revision identifiers, used by Alembic.
revision = '1fb7c6da302'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('user',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(length=20), nullable=False),
        sa.Column('email', sa.String(length=128), nullable=False),
        sa.Column('pw_hash', sa.String(length=60), nullable=False),
        sa.Column('created_ts', sa.DateTime(), nullable=False),
        sa.Column('remote_addr', sa.String(length=20), nullable=True),
        sa.Column('active', sa.Boolean(), nullable=True),
        sa.Column('is_admin', sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('username')
    )


def downgrade():
    op.drop_table('user')
