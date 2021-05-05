"""empty message

Revision ID: f106e3841905
Revises: 619c6e7b8027
Create Date: 2020-04-02 09:43:25.602034

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f106e3841905'
down_revision = '619c6e7b8027'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cars',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('customer_name', sa.String(length=100), nullable=True),
    sa.Column('customer_id', sa.String(length=20), nullable=True),
    sa.Column('customer_address', sa.String(length=200), nullable=True),
    sa.Column('customer_telno', sa.String(length=15), nullable=True),
    sa.Column('car_no', sa.String(length=20), nullable=True),
    sa.Column('car_name', sa.String(length=50), nullable=True),
    sa.Column('fc_id', sa.String(length=20), nullable=True),
    sa.Column('description', sa.String(length=200), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('cars')
    # ### end Alembic commands ###