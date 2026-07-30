"""cart usa session_id em vez de user_id

Revision ID: c82d673571bf
Revises: 7e7a6b1a8608
Create Date: 2026-07-30

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c82d673571bf'
down_revision = '7e7a6b1a8608'
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table('carts') as batch_op:
        batch_op.add_column(
            sa.Column('session_id', sa.String(), nullable=True)
        )
        batch_op.drop_column('user_id')

    with op.batch_alter_table('carts') as batch_op:
        batch_op.alter_column('session_id', nullable=False)
        batch_op.create_unique_constraint(
            'uq_carts_session_id', ['session_id']
        )


def downgrade() -> None:
    with op.batch_alter_table('carts') as batch_op:
        batch_op.drop_constraint('uq_carts_session_id', type_='unique')
        batch_op.drop_column('session_id')
        batch_op.add_column(
            sa.Column('user_id', sa.Integer(), nullable=False)
        )
