"""add source event provenance to derived memories

Revision ID: 0004_derived_memory_source_event
Revises: 0003_derived_memories
Create Date: 2026-03-31
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision = "0004_derived_memory_source_event"
down_revision = "0003_derived_memories"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "derived_memories",
        sa.Column("source_event_id", postgresql.UUID(as_uuid=True), nullable=True),
    )
    op.create_foreign_key(
        "fk_derived_memories_source_event_id_events",
        "derived_memories",
        "events",
        ["source_event_id"],
        ["id"],
    )
    op.create_index(
        "ix_derived_memories_source_event_id",
        "derived_memories",
        ["source_event_id"],
    )


def downgrade() -> None:
    op.drop_index("ix_derived_memories_source_event_id", table_name="derived_memories")
    op.drop_constraint("fk_derived_memories_source_event_id_events", "derived_memories", type_="foreignkey")
    op.drop_column("derived_memories", "source_event_id")
