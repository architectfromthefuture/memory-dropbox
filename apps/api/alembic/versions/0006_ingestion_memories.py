"""add ingestion memories table

Revision ID: 0006_ingestion_memories
Revises: 0005_observation_memories
Create Date: 2026-04-09
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision = "0006_ingestion_memories"
down_revision = "0005_observation_memories"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "ingestion_memories",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("filename", sa.String(length=1024), nullable=False),
        sa.Column("total_chunks", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("ingestion_count", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("last_ingested_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.UniqueConstraint("filename", name="uq_ingestion_memories_filename"),
    )
    op.create_index("ix_ingestion_memories_filename", "ingestion_memories", ["filename"])
    op.create_index("ix_ingestion_memories_last_ingested_at", "ingestion_memories", ["last_ingested_at"])


def downgrade() -> None:
    op.drop_index("ix_ingestion_memories_last_ingested_at", table_name="ingestion_memories")
    op.drop_index("ix_ingestion_memories_filename", table_name="ingestion_memories")
    op.drop_table("ingestion_memories")
