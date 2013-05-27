"""
    Payments table
"""

# revision identifiers, used by Alembic.
revision = '003'
down_revision = '002' 

from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table('payment',
        sa.Column('id', sa.Integer(11), nullable=False),
        sa.Column('invoice_id', sa.Integer(11), nullable=False),
        sa.Column('date', sa.DateTime, nullable=False),
        sa.Column('currency_code', sa.Unicode(3), nullable=False),
        sa.Column('amount', sa.Numeric(8, 2), nullable=False, server_default='0'),
        sa.Column('method', sa.Unicode(50), nullable=True),
        sa.Column('created_at', sa.DateTime, nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['invoice_id'], ['invoice.id'], ondelete='CASCADE' ),
    )

    op.add_column('invoice', sa.Column('payment_status', sa.Unicode(10), server_default='unpaid'))

def downgrade():
    op.drop_table('payment')
    
