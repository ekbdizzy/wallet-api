"""Add wallets

Revision ID: 18ab23d29d9d
Revises: 
Create Date: 2024-02-03 23:29:47.523027

"""
from typing import Sequence, Union
from datetime import datetime

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '18ab23d29d9d'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table('wallets',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('label', sa.String(length=128), nullable=False),
                    sa.Column('balance', sa.DECIMAL(precision=18, scale=2), nullable=False, default='0.00'),
                    sa.Column('created_at', sa.DateTime(timezone=True), default=datetime.now()),
                    sa.Column('updated_at', sa.DateTime(timezone=True), default=datetime.now()),
                    sa.PrimaryKeyConstraint('id'),
                    )
    op.create_index(op.f('ix_wallets_id'), 'wallets', ['id'], unique=False)
    op.create_index('ix_wallets_label', 'wallets', ['label'], unique=False)
    op.create_index('ix_wallets_balance', 'wallets', ['balance'], unique=False)


def downgrade():
    op.drop_index('ix_wallets_id', table_name='wallets')
    op.drop_index('ix_wallets_balance', table_name='wallets')
    op.drop_index('ix_wallets_label', table_name='wallets')
    op.drop_table('wallets')