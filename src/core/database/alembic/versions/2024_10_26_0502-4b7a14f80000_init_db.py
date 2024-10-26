"""init db

Revision ID: 4b7a14f80000
Revises: 
Create Date: 2024-10-26 05:02:34.344387

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '4b7a14f80000'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('request_history',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('uuid_user', mysql.VARCHAR(length=36), nullable=False),
    sa.Column('name', mysql.VARCHAR(length=255), nullable=False),
    sa.Column('url_card', mysql.TEXT(), nullable=False),
    sa.Column('url_img', mysql.TEXT(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('uuid_user')
    )
    op.create_table('user',
    sa.Column('uuid', mysql.VARCHAR(length=36), nullable=False),
    sa.Column('email', mysql.VARCHAR(length=255), nullable=False),
    sa.Column('pwd_hash', mysql.TINYBLOB(), nullable=False),
    sa.Column('reg_at', sa.DateTime(), nullable=False),
    sa.Column('active', sa.Boolean(), server_default=sa.text('TRUE'), nullable=False),
    sa.PrimaryKeyConstraint('uuid'),
    sa.UniqueConstraint('email')
    )
    op.create_index('email_index', 'user', ['email'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('email_index', table_name='user')
    op.drop_table('user')
    op.drop_table('request_history')
    # ### end Alembic commands ###
