"""Initial database setup

Revision ID: 59fdaa7da10f
Revises: None
Create Date: 2012-07-17 12:20:38.716366

"""

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None

from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table('logo',
        sa.Column('id', sa.Integer(11), nullable=False),
        sa.Column('original_image_id', sa.Integer(11), nullable=False),
        sa.Column('thumbnail_image_id', sa.Integer(11), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['original_image_id'], ['file.id'], ondelete='CASCADE' ),
        sa.ForeignKeyConstraint(['thumbnail_image_id'], ['file.id'], ondelete='CASCADE' ),
    )
def downgrade():
    op.drop_table('logo')
    
