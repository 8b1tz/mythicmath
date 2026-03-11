#!/usr/bin/env python
"""create users table

Revision ID: 64776d5e38bf
Revises: 
Create Date: 2026-03-11 14:37:05.589109
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '64776d5e38bf'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False, unique=True),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("photo_url", sa.String(length=2048), nullable=True),
        sa.Column("xp", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("level", sa.Integer(), nullable=False, server_default=sa.text("1")),
        sa.Column("total_score", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("ranked_wins", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
    )


def downgrade() -> None:
    op.drop_table("users")
