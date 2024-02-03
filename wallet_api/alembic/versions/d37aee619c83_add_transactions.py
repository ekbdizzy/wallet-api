"""Add transactions

Revision ID: d37aee619c83
Revises: 18ab23d29d9d
Create Date: 2024-02-03 23:33:48.529919

"""
import uuid
from datetime import datetime
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd37aee619c83'
down_revision: Union[str, None] = '18ab23d29d9d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table('transactions',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.Column('txid', sa.String(36), nullable=False, unique=True),
                    sa.Column('wallet_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['wallet_id'], ['wallets.id'], name='fk_transaction_wallet_id_wallets'),
                    sa.Column('amount', sa.DECIMAL(precision=18, scale=2), nullable=True),
                    sa.Column('is_inbound', sa.Boolean(), nullable=True),
                    sa.Column('created_at', sa.DateTime(timezone=True), default=datetime.now()),
                    sa.Column('updated_at', sa.DateTime(timezone=True), default=datetime.now()),
                    )
    op.create_index(op.f('ix_transactions_id'), 'transactions', ['id'], unique=False)
    op.create_index('ix_transactions_txid', 'transactions', ['txid'], unique=False)
    op.create_index('ix_transactions_created_at', 'transactions', ['created_at'], unique=False)


def downgrade():
    op.drop_index('ix_transactions_id', table_name='transactions')
    op.drop_index('ix_transactions_created_at', table_name='transactions')
    op.drop_index('ix_transactions_txid', table_name='transactions')
    op.drop_table('transactions')