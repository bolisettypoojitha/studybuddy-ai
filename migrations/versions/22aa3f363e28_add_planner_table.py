"""Add planner table

Revision ID: 22aa3f363e28
Revises: 7e7cc8aae42d
Create Date: 2025-07-04 17:46:25.762100

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '22aa3f363e28'
down_revision = '7e7cc8aae42d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('planner',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('task', sa.String(length=200), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('time', sa.Time(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('planner')
    # ### end Alembic commands ###
