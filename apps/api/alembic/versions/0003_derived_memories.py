"""add derived memories table

Revision ID: 0003_derived_memories
Revises: 0002_events_table
Create Date: 2026-03-31
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision = "0003_derived_memories"
down_revision = "0002_events_table"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "derived_memories",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("event_type", sa.String(length=64), nullable=False),
        sa.Column("filename", sa.String(length=1024), nullable=False),
        sa.Column("chunk_count", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("timestamp", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
    )
    op.create_index("ix_derived_memories_timestamp", "derived_memories", ["timestamp"])


def downgrade() -> None:
    op.drop_index("ix_derived_memories_timestamp", table_name="derived_memories")
    op.drop_table("derived_memories")
