"""Table

Revision ID: d398c46d1a90
Revises: 
Create Date: 2023-10-03 12:15:52.223116

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd398c46d1a90'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('app',
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('gender', sa.String(length=16), nullable=True),
    sa.Column('name', sa.String(length=15), nullable=True),
    sa.Column('years', sa.Integer(), nullable=True),
    sa.Column('city', sa.String(length=32), nullable=True),
    sa.Column('usrname', sa.String(length=32), nullable=True),
    sa.Column('photo_id', sa.String(length=128), nullable=True),
    sa.Column('pub_video', sa.Boolean(), nullable=True),
    sa.Column('video_id', sa.String(length=128), nullable=True),
    sa.Column('score', sa.BigInteger(), nullable=True),
    sa.Column('moderated', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('user_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('app')
    # ### end Alembic commands ###
