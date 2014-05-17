"""Webhook logging"""

# revision identifiers, used by Alembic.
revision = '007'
down_revision = '006'

import sqlalchemy as sa

from alembic import op
from sqlalchemy import func

def upgrade():
    op.create_table('webhook_log',
        sa.Column('id', sa.Integer, nullable=False),
        sa.Column('service', sa.Unicode(50), nullable=False),
        sa.Column('data', sa.UnicodeText(4294967295), nullable=False),
        sa.Column('ip', sa.Unicode(50), nullable=False),
        sa.Column('headers', sa.UnicodeText, nullable=False),
        sa.Column('created_at', sa.DateTime, nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    op.add_column('subscription', sa.Column('stripe_customer_id', sa.Unicode(255), nullable=True))

def downgrade():
    op.drop_table('webhook_log')
    op.drop_column('subscription', 'stripe_customer_id')


