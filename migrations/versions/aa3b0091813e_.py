"""empty message

Revision ID: aa3b0091813e
Revises: 1312d9703e28
Create Date: 2020-04-10 20:52:20.797709

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'aa3b0091813e'
down_revision = '1312d9703e28'
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
    op.add_column('cars', sa.Column('age_limit', sa.String(length=10), nullable=True))
    op.add_column('cars', sa.Column('car_acc', sa.String(length=100), nullable=True))
    op.add_column('cars', sa.Column('car_code', sa.String(length=10), nullable=True))
    op.add_column('cars', sa.Column('car_year', sa.String(length=5), nullable=True))
    op.add_column('cars', sa.Column('company', sa.String(length=30), nullable=True))
    op.add_column('cars', sa.Column('cov_car', sa.String(length=10), nullable=True))
    op.add_column('cars', sa.Column('cov_mandatory', sa.Boolean(), nullable=True))
    op.add_column('cars', sa.Column('cov_noncover', sa.String(length=10), nullable=True))
    op.add_column('cars', sa.Column('cov_object', sa.String(length=10), nullable=True))
    op.add_column('cars', sa.Column('cov_person', sa.Boolean(), nullable=True))
    op.add_column('cars', sa.Column('cov_self', sa.String(length=10), nullable=True))
    op.add_column('cars', sa.Column('created', sa.DateTime(), nullable=True))
    op.add_column('cars', sa.Column('customer_eq', sa.Boolean(), nullable=True))
    op.add_column('cars', sa.Column('customer_job', sa.String(length=50), nullable=True))
    op.add_column('cars', sa.Column('driver_id', sa.String(length=20), nullable=True))
    op.add_column('cars', sa.Column('driver_limit', sa.String(length=10), nullable=True))
    op.add_column('cars', sa.Column('driver_name', sa.String(length=50), nullable=True))
    op.add_column('cars', sa.Column('exp_date', sa.Date(), nullable=True))
    op.add_column('cars', sa.Column('owner_address', sa.String(length=120), nullable=True))
    op.add_column('cars', sa.Column('owner_id', sa.String(length=20), nullable=True))
    op.add_column('cars', sa.Column('owner_job', sa.String(length=50), nullable=True))
    op.add_column('cars', sa.Column('owner_name', sa.String(length=50), nullable=True))
    op.add_column('cars', sa.Column('owner_telno', sa.String(length=15), nullable=True))
    op.add_column('cars', sa.Column('spc_blackbox', sa.Boolean(), nullable=True))
    op.add_column('cars', sa.Column('spc_emergency', sa.String(length=10), nullable=True))
    op.add_column('cars', sa.Column('spc_mileage', sa.Boolean(), nullable=True))
    op.add_column('employees', sa.Column('glad_id', sa.String(length=60), nullable=True))
    op.add_column('employees', sa.Column('tel_no', sa.String(length=20), nullable=True))
    op.create_index(op.f('ix_employees_glad_id'), 'employees', ['glad_id'], unique=True)
    op.create_index(op.f('ix_employees_tel_no'), 'employees', ['tel_no'], unique=False)
    op.drop_index('ix_employees_first_name', table_name='employees')
    op.drop_index('ix_employees_last_name', table_name='employees')
    op.drop_column('employees', 'first_name')
    op.drop_column('employees', 'last_name')
    op.create_foreign_key(None, 'posts', 'employees', ['author_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'posts', type_='foreignkey')
    op.add_column('employees', sa.Column('last_name', mysql.VARCHAR(length=60), nullable=True))
    op.add_column('employees', sa.Column('first_name', mysql.VARCHAR(length=60), nullable=True))
    op.create_index('ix_employees_last_name', 'employees', ['last_name'], unique=False)
    op.create_index('ix_employees_first_name', 'employees', ['first_name'], unique=False)
    op.drop_index(op.f('ix_employees_tel_no'), table_name='employees')
    op.drop_index(op.f('ix_employees_glad_id'), table_name='employees')
    op.drop_column('employees', 'tel_no')
    op.drop_column('employees', 'glad_id')
    op.drop_column('cars', 'spc_mileage')
    op.drop_column('cars', 'spc_emergency')
    op.drop_column('cars', 'spc_blackbox')
    op.drop_column('cars', 'owner_telno')
    op.drop_column('cars', 'owner_name')
    op.drop_column('cars', 'owner_job')
    op.drop_column('cars', 'owner_id')
    op.drop_column('cars', 'owner_address')
    op.drop_column('cars', 'exp_date')
    op.drop_column('cars', 'driver_name')
    op.drop_column('cars', 'driver_limit')
    op.drop_column('cars', 'driver_id')
    op.drop_column('cars', 'customer_job')
    op.drop_column('cars', 'customer_eq')
    op.drop_column('cars', 'created')
    op.drop_column('cars', 'cov_self')
    op.drop_column('cars', 'cov_person')
    op.drop_column('cars', 'cov_object')
    op.drop_column('cars', 'cov_noncover')
    op.drop_column('cars', 'cov_mandatory')
    op.drop_column('cars', 'cov_car')
    op.drop_column('cars', 'company')
    op.drop_column('cars', 'car_year')
    op.drop_column('cars', 'car_code')
    op.drop_column('cars', 'car_acc')
    op.drop_column('cars', 'age_limit')
    op.drop_table('gladfc')
    # ### end Alembic commands ###