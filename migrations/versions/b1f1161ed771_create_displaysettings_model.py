"""Create DisplaySettings model

Revision ID: b1f1161ed771
Revises: df1541844fa1
Create Date: 2024-03-18 17:24:42.594918

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b1f1161ed771'
down_revision = 'df1541844fa1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('display_settings',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('photo_order', sa.String(length=24), nullable=False),
    sa.Column('display_time', sa.Integer(), nullable=False),
    sa.Column('fade', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('display_settings')
    # ### end Alembic commands ###
