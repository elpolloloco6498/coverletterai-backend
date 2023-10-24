"""Created resume table

Revision ID: 648dac9519fa
Revises: d18993ac4af4
Create Date: 2023-10-04 10:18:11.032905

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '648dac9519fa'
down_revision: Union[str, None] = 'd18993ac4af4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('resume',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('text', sa.String(length=10000), nullable=False),
        sa.Column('user_id', sa.String(length=255), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('resume')
