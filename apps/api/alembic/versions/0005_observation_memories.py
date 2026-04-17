"""add observation memories table

Revision ID: 0005_observation_memories
Revises: 0004_derived_memory_source_event
Create Date: 2026-03-31
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision = "0005_observation_memories"
down_revision = "0004_derived_memory_source_event"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "observation_memories",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("observation_type", sa.String(length=64), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("filename", sa.String(length=1024), nullable=False),
        sa.Column("chunk_count", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("timestamp", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("source_event_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("events.id"), nullable=False),
    )
    op.create_index("ix_observation_memories_timestamp", "observation_memories", ["timestamp"])
    op.create_index("ix_observation_memories_source_event_id", "observation_memories", ["source_event_id"])


def downgrade() -> None:
    op.drop_index("ix_observation_memories_source_event_id", table_name="observation_memories")
    op.drop_index("ix_observation_memories_timestamp", table_name="observation_memories")
    op.drop_table("observation_memories")
