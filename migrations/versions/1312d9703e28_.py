"""empty message

Revision ID: 1312d9703e28
Revises: 75c94d9c76df
Create Date: 2020-04-10 15:15:04.077650

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '1312d9703e28'
down_revision = '75c94d9c76df'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('gladfc',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('glad_id', sa.String(length=20), nullable=True),
    sa.Column('glad_name', sa.String(length=60), nullable=True),
    sa.Column('glad_brh', sa.String(length=100), nullable=True),
    sa.Column('tel_no', sa.String(length=20), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('employees', sa.Column('glad_id', sa.String(length=60), nullable=True))
    op.add_column('employees', sa.Column('tel_no', sa.String(length=20), nullable=True))
    op.create_index(op.f('ix_employees_glad_id'), 'employees', ['glad_id'], unique=True)
    op.create_index(op.f('ix_employees_tel_no'), 'employees', ['tel_no'], unique=False)
    op.drop_index('ix_employees_first_name', table_name='employees')
    op.drop_index('ix_employees_last_name', table_name='employees')
    op.drop_column('employees', 'first_name')
    op.drop_column('employees', 'last_name')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('employees', sa.Column('last_name', mysql.VARCHAR(length=60), nullable=True))
    op.add_column('employees', sa.Column('first_name', mysql.VARCHAR(length=60), nullable=True))
    op.create_index('ix_employees_last_name', 'employees', ['last_name'], unique=False)
    op.create_index('ix_employees_first_name', 'employees', ['first_name'], unique=False)
    op.drop_index(op.f('ix_employees_tel_no'), table_name='employees')
    op.drop_index(op.f('ix_employees_glad_id'), table_name='employees')
    op.drop_column('employees', 'tel_no')
    op.drop_column('employees', 'glad_id')
    op.drop_table('gladfc')
    # ### end Alembic commands ###