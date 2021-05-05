"""empty message

Revision ID: 619c6e7b8027
Revises: 
Create Date: 2020-03-31 09:05:36.041165

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '619c6e7b8027'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('departments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=60), nullable=True),
    sa.Column('description', sa.String(length=200), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=60), nullable=True),
    sa.Column('description', sa.String(length=200), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('employees',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=60), nullable=True),
    sa.Column('username', sa.String(length=60), nullable=True),
    sa.Column('first_name', sa.String(length=60), nullable=True),
    sa.Column('last_name', sa.String(length=60), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('department_id', sa.Integer(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['department_id'], ['departments.id'], ),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_employees_email'), 'employees', ['email'], unique=True)
    op.create_index(op.f('ix_employees_first_name'), 'employees', ['first_name'], unique=False)
    op.create_index(op.f('ix_employees_last_name'), 'employees', ['last_name'], unique=False)
    op.create_index(op.f('ix_employees_username'), 'employees', ['username'], unique=True)
    op.drop_table('long_contr')
    op.drop_index('개시일_index', table_name='worksheet')
    op.drop_index('납입회차_index', table_name='worksheet')
    op.drop_index('만기일_index', table_name='worksheet')
    op.drop_index('수수료H_index', table_name='worksheet')
    op.drop_index('수수료M_index', table_name='worksheet')
    op.drop_index('수수료S_index', table_name='worksheet')
    op.drop_index('수수료T_index', table_name='worksheet')
    op.drop_index('수정보험료_index', table_name='worksheet')
    op.drop_index('수정율_index', table_name='worksheet')
    op.drop_index('실손수정보_index', table_name='worksheet')
    op.drop_index('실손월납보_index', table_name='worksheet')
    op.drop_index('영수일_index', table_name='worksheet')
    op.drop_index('월납보험료_index', table_name='worksheet')
    op.drop_index('정산월구분_index', table_name='worksheet')
    op.drop_index('조정보험료_index', table_name='worksheet')
    op.drop_index('총회차_index', table_name='worksheet')
    op.drop_table('worksheet')
    op.drop_table('시트명2')
    op.drop_table('contract')
    op.drop_table('users')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('deptname', mysql.VARCHAR(length=50), nullable=False),
    sa.Column('username', mysql.VARCHAR(length=50), nullable=False),
    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('salary', mysql.FLOAT(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('contract',
    sa.Column('idcontract', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('c_name', mysql.VARCHAR(length=45), nullable=True),
    sa.Column('c_date', mysql.DATETIME(), nullable=True),
    sa.Column('c_brh', mysql.VARCHAR(length=45), nullable=True),
    sa.PrimaryKeyConstraint('idcontract'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('시트명2',
    sa.Column('시트명2_id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('MPK033', mysql.VARCHAR(length=255), nullable=True),
    sa.PrimaryKeyConstraint('시트명2_id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('worksheet',
    sa.Column('worksheet_id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('지점', mysql.VARCHAR(length=5), nullable=True),
    sa.Column('지점ID', mysql.VARCHAR(length=12), nullable=True),
    sa.Column('팀', mysql.VARCHAR(length=12), nullable=True),
    sa.Column('팀ID', mysql.VARCHAR(length=12), nullable=True),
    sa.Column('담당', mysql.VARCHAR(length=5), nullable=True),
    sa.Column('담당ID', mysql.VARCHAR(length=12), nullable=True),
    sa.Column('담당명', mysql.VARCHAR(length=5), nullable=True),
    sa.Column('업무담당', mysql.VARCHAR(length=5), nullable=True),
    sa.Column('전담당', mysql.VARCHAR(length=255), nullable=True),
    sa.Column('위촉상태', mysql.VARCHAR(length=5), nullable=True),
    sa.Column('계약일', mysql.VARCHAR(length=12), nullable=True),
    sa.Column('보험회사', mysql.VARCHAR(length=5), nullable=True),
    sa.Column('대리점', mysql.VARCHAR(length=5), nullable=True),
    sa.Column('보험상품', mysql.VARCHAR(length=45), nullable=True),
    sa.Column('상품코드', mysql.VARCHAR(length=12), nullable=True),
    sa.Column('보종', mysql.VARCHAR(length=5), nullable=True),
    sa.Column('정산월구분', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('월납보험료', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('수정보험료', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('조정보험료', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('실손월납보', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('실손수정보', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('수수료T', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('수수료H', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('수수료M', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('수수료S', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('수정율', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('구분', mysql.VARCHAR(length=5), nullable=True),
    sa.Column('납입회차', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('총회차', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('피보험자', mysql.VARCHAR(length=5), nullable=True),
    sa.Column('생년월일_/_성별', mysql.VARCHAR(length=12), nullable=True),
    sa.Column('계약자', mysql.VARCHAR(length=5), nullable=True),
    sa.Column('생년월일_/_성별2', mysql.VARCHAR(length=12), nullable=True),
    sa.Column('영수일', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('증권번호', mysql.VARCHAR(length=25), nullable=True),
    sa.Column('개시일', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('만기일', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('경로', mysql.VARCHAR(length=255), nullable=True),
    sa.Column('기타1', mysql.VARCHAR(length=255), nullable=True),
    sa.Column('납입방법', mysql.VARCHAR(length=5), nullable=True),
    sa.Column('상담자', mysql.VARCHAR(length=5), nullable=True),
    sa.PrimaryKeyConstraint('worksheet_id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_index('총회차_index', 'worksheet', ['총회차'], unique=False)
    op.create_index('조정보험료_index', 'worksheet', ['조정보험료'], unique=False)
    op.create_index('정산월구분_index', 'worksheet', ['정산월구분'], unique=False)
    op.create_index('월납보험료_index', 'worksheet', ['월납보험료'], unique=False)
    op.create_index('영수일_index', 'worksheet', ['영수일'], unique=False)
    op.create_index('실손월납보_index', 'worksheet', ['실손월납보'], unique=False)
    op.create_index('실손수정보_index', 'worksheet', ['실손수정보'], unique=False)
    op.create_index('수정율_index', 'worksheet', ['수정율'], unique=False)
    op.create_index('수정보험료_index', 'worksheet', ['수정보험료'], unique=False)
    op.create_index('수수료T_index', 'worksheet', ['수수료T'], unique=False)
    op.create_index('수수료S_index', 'worksheet', ['수수료S'], unique=False)
    op.create_index('수수료M_index', 'worksheet', ['수수료M'], unique=False)
    op.create_index('수수료H_index', 'worksheet', ['수수료H'], unique=False)
    op.create_index('만기일_index', 'worksheet', ['만기일'], unique=False)
    op.create_index('납입회차_index', 'worksheet', ['납입회차'], unique=False)
    op.create_index('개시일_index', 'worksheet', ['개시일'], unique=False)
    op.create_table('long_contr',
    sa.Column('long_contr_id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('계약일', mysql.VARCHAR(length=255), nullable=False),
    sa.PrimaryKeyConstraint('long_contr_id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.drop_index(op.f('ix_employees_username'), table_name='employees')
    op.drop_index(op.f('ix_employees_last_name'), table_name='employees')
    op.drop_index(op.f('ix_employees_first_name'), table_name='employees')
    op.drop_index(op.f('ix_employees_email'), table_name='employees')
    op.drop_table('employees')
    op.drop_table('roles')
    op.drop_table('departments')
    # ### end Alembic commands ###
