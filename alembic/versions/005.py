"""Settings"""

# revision identifiers, used by Alembic.
revision = '005'
down_revision = '004'

from alembic import op

import sqlalchemy as sa
import sqlalchemy.types

def upgrade():
    op.create_table('setting', 
        sa.Column('id',         sa.Integer(11), nullable=False),
        sa.Column('user_id',    sa.Integer(11), nullable=False),
        sa.Column('key',        sa.Unicode(100), nullable=False),
        sa.Column('value',      sqlalchemy.types.BLOB, nullable=False),
        sa.Column('created_at', sa.DateTime, nullable=False),
        sa.Column('updated_at', sa.DateTime, nullable=False),

        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE' ),
    )

def downgrade():
    op.drop_table('setting')
    
