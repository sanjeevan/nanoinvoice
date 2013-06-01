"""
    Taking payments from clients
"""

# revision identifiers, used by Alembic.
revision = '004'
down_revision = '003'

from alembic import op
import sqlalchemy as sa

def upgrade():

    op.create_table('invoice_link', 
        sa.Column('id', sa.Integer(11), nullable=False),
        sa.Column('user_id', sa.Integer(11), nullable=False),
        sa.Column('invoice_id', sa.Integer(11), nullable=False),
        sa.Column('link', sa.Unicode(25), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE' ),
        sa.ForeignKeyConstraint(['invoice_id'], ['invoice.id'], ondelete='CASCADE' ),
    )

    op.create_table('stripe_account', 
        sa.Column('id', sa.Integer(11), nullable=False),
        sa.Column('user_id', sa.Integer(11), nullable=False),
        sa.Column('secret_key', sa.Unicode(255), nullable=True),
        sa.Column('public_key', sa.Unicode(255), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE' ),
    )

    op.create_table('gocardless_account',
        sa.Column('id', sa.Integer(11), nullable=False),
        sa.Column('user_id', sa.Integer(11), nullable=False),
        sa.Column('app_identifier', sa.Unicode(255), nullable=True),
        sa.Column('app_secret', sa.Unicode(255), nullable=True),
        sa.Column('merchant_access_token', sa.Unicode(255), nullable=True),
        sa.Column('merchant_id', sa.Unicode(255), nullable=True),
        sa.Column('created_at', sa.DateTime, nullable=False),
        sa.Column('updated_at', sa.DateTime, nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE' ),
    )

    op.create_table('gocardless_payment', 
        sa.Column('id', sa.Integer(11), nullable=False),
        sa.Column('user_id', sa.Integer(11), nullable=False),
        sa.Column('payment_id', sa.Integer(11), nullable=False),
        sa.Column('created_at', sa.DateTime, nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE' ),
        sa.ForeignKeyConstraint(['payment_id'], ['payment.id'], ondelete='CASCADE' ),
    )

    op.create_table('stripe_payment',
        sa.Column('id', sa.Integer(11), nullable=False),
        sa.Column('user_id', sa.Integer(11), nullable=False),
        sa.Column('payment_id', sa.Integer(11), nullable=False),
        sa.Column('created_at', sa.DateTime, nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE' ),
        sa.ForeignKeyConstraint(['payment_id'], ['payment.id'], ondelete='CASCADE' ),
    )

def downgrade():
    op.drop_table('stripe_payment')
    op.drop_table('gocardless_payment')
    op.drop_table('gocardless_account')
    op.drop_table('stripe_account')
    op.drop_table('invoice_link')
    
