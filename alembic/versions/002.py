"""
    Extra invoice fields table
"""

# revision identifiers, used by Alembic.
revision = '002'
down_revision = '001' 

from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table('custom_field',
        sa.Column('id', sa.Integer(11), nullable=False),
        sa.Column('user_id', sa.Integer(11), nullable=False),
        sa.Column('name', sa.Unicode(255), nullable=False),
        sa.Column('value', sa.Unicode(255), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE' ),
    )
def downgrade():
    op.drop_table('custom_field')
    
