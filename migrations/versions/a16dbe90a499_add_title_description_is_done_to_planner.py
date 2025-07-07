"""Add title, description, is_done to planner

Revision ID: a16dbe90a499
Revises: 22aa3f363e28
Create Date: 2025-07-04 18:22:41.642884
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'a16dbe90a499'
down_revision = '22aa3f363e28'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('planner', schema=None) as batch_op:
        # Add new columns as nullable for now
        batch_op.add_column(sa.Column('title', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('description', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('is_done', sa.Boolean(), nullable=True))
        
        # Drop old columns
        batch_op.drop_column('task')
        batch_op.drop_column('time')

    # Backfill with default values to avoid NULL errors
    op.execute("UPDATE planner SET title = 'Untitled Task' WHERE title IS NULL")
    op.execute("UPDATE planner SET description = '' WHERE description IS NULL")

    # Alter to set NOT NULL constraints after backfill
    with op.batch_alter_table('planner', schema=None) as batch_op:
        batch_op.alter_column('title', existing_type=sa.String(length=100), nullable=False)
        batch_op.alter_column('description', existing_type=sa.Text(), nullable=False)


def downgrade():
    with op.batch_alter_table('planner', schema=None) as batch_op:
        batch_op.add_column(sa.Column('time', postgresql.TIME(), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('task', sa.VARCHAR(length=200), autoincrement=False, nullable=False))
        batch_op.drop_column('is_done')
        batch_op.drop_column('description')
        batch_op.drop_column('title')
