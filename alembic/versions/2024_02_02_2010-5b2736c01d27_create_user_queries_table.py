"""create user_queries table

Revision ID: 5b2736c01d27
Revises:
Create Date: 2024-02-02 20:10:46.596699

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '5b2736c01d27'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    """Create the gemini_queries table to store questions and responses."""
    op.create_table(# pylint: disable=no-member
        'gemini_queries',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('original_filename', sa.String(150)),
        sa.Column('cloud_filename', sa.String(150)),
        sa.Column('prompt', sa.String),
        sa.Column('response', sa.String),
        sa.Column('created_at', sa.DateTime, server_default=sa.text('now()'))
    )

def downgrade() -> None:
    """Drop the gemini_queries table."""
    op.drop_table('gemini_queries') # pylint: disable=no-member
