"""empty message

Revision ID: 50bc755eed70
Revises: 92ce49e4c131
Create Date: 2020-05-12 10:10:38.673311

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '50bc755eed70'
down_revision = '92ce49e4c131'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_contracts_index', table_name='contracts')
    # ### op.drop_table('contracts')
    op.add_column('posts', sa.Column('filename', sa.String(length=100), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('posts', 'filename')
    op.create_table('contracts',
    sa.Column('index', mysql.BIGINT(display_width=20), autoincrement=False, nullable=True),
    sa.Column('지점', mysql.TEXT(), nullable=True),
    sa.Column('직할지점', mysql.TEXT(), nullable=True),
    sa.Column('팀', mysql.TEXT(), nullable=True),
    sa.Column('수금사원번호', mysql.TEXT(), nullable=True),
    sa.Column('수금사원명', mysql.TEXT(), nullable=True),
    sa.Column('증권번호', mysql.TEXT(), nullable=True),
    sa.Column('계약일자', mysql.TEXT(), nullable=True),
    sa.Column('보험사', mysql.TEXT(), nullable=True),
    sa.Column('계약종류', mysql.TEXT(), nullable=True),
    sa.Column('상품종류', mysql.TEXT(), nullable=True),
    sa.Column('초회보험료', mysql.BIGINT(display_width=20), autoincrement=False, nullable=True),
    sa.Column('계약상태', mysql.TEXT(), nullable=True),
    sa.Column('납입회차', mysql.DOUBLE(asdecimal=True), nullable=True),
    sa.Column('납입주기(방법)', mysql.TEXT(), nullable=True),
    sa.Column('최종상태변경일', mysql.TEXT(), nullable=True),
    sa.Column('원수사성적', mysql.BIGINT(display_width=20), autoincrement=False, nullable=True),
    sa.Column('(신)글로벌성적', mysql.BIGINT(display_width=20), autoincrement=False, nullable=True),
    sa.Column('계약자', mysql.TEXT(), nullable=True),
    sa.Column('피보험자', mysql.TEXT(), nullable=True),
    sa.Column('최종납입년월', mysql.TEXT(), nullable=True),
    sa.Column('최종수금일', mysql.TEXT(), nullable=True),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_index('ix_contracts_index', 'contracts', ['index'], unique=False)
    # ### end Alembic commands ###
