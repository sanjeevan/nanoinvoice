"""Subscriptions"""

# revision identifiers, used by Alembic.
revision = '006'
down_revision = '005'

import sqlalchemy as sa

from alembic import op
from sqlalchemy import func

def upgrade():
    op.create_table('plan',
        sa.Column('id',                 sa.Integer(11),     nullable=False),
        sa.Column('name',               sa.Unicode(20),     nullable=False),
        sa.Column('gateway_uid',        sa.Unicode(20),     nullable=False),
        sa.Column('description',        sa.Unicode(255),    nullable=False),
        sa.Column('amount',             sa.Numeric(8, 2),   server_default='0.0'),
        sa.Column('billing_interval',   sa.Enum('daily', 'weekly', 'monthly', 'yearly'), server_default=u'monthly'),

        sa.Column('created_at', sa.DateTime, nullable=False),

        sa.PrimaryKeyConstraint('id')
    )

    op.create_table('subscription',
        sa.Column('id',         sa.Integer(11), nullable=False),
        sa.Column('user_id',    sa.Integer(11), nullable=False),
        sa.Column('plan_id',    sa.Integer(11), nullable=False),
        sa.Column('active',     sa.Boolean,     nullable=False, server_default='0'),
        sa.Column('start_date', sa.DateTime,    nullable=True),
        sa.Column('end_date',   sa.DateTime,    nullable=True),
        sa.Column('created_at', sa.DateTime,    nullable=False),
        sa.Column('stripe_data',sa.UnicodeText(4294967295), nullable=False, default=u'{}'),
        sa.Column('updated_at', sa.DateTime,    nullable=False, server_onupdate=func.now()),

        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE' ),
        sa.ForeignKeyConstraint(['plan_id'], ['plan.id'], ondelete='CASCADE' ),
    )

    op.create_table('transaction',
        sa.Column('id',             sa.Integer(11), nullable=False),
        sa.Column('user_id',        sa.Integer(11), nullable=False),
        sa.Column('subscription_id',sa.Integer(11), nullable=False),
        sa.Column('success',        sa.Boolean,     nullable=False, server_default=u'0'),
        sa.Column('amount',         sa.Numeric(8, 2), default='0.0'),
        sa.Column('charge_id',      sa.Unicode(100), nullable=True),
        sa.Column('charge',         sa.UnicodeText(4294967295), nullable=True, default=u'{}'),

        sa.Column('created_at', sa.DateTime, nullable=False),
        sa.Column('updated_at', sa.DateTime, nullable=False, server_onupdate=func.now()),

        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE' ),
        sa.ForeignKeyConstraint(['subscription_id'], ['subscription.id'], ondelete='CASCADE' ),
    )

def downgrade():
    op.drop_table('transaction')
    op.drop_table('subscription')
    op.drop_table('plan')


