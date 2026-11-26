"""keycloak_id added, password_hash dropped

Revision ID: 0003
Revises: 0002
Create Date: 2026-11-26 21:30:00.000000

"""
from collections.abc import Sequence
from typing import Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "0003"
down_revision: Union[str, Sequence[str], None] = "0002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("users", sa.Column("keycloak_id", sa.String(64), nullable=True))
    op.execute(
        "UPDATE users SET keycloak_id = 'legacy-' || id WHERE keycloak_id IS NULL"
    )
    op.alter_column("users", "keycloak_id", nullable=False)
    op.create_index("ix_users_keycloak_id", "users", ["keycloak_id"], unique=True)
    op.drop_column("users", "password_hash")


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column(
        "users",
        sa.Column("password_hash", sa.String(length=255), nullable=True),
    )
    op.drop_index("ix_users_keycloak_id", table_name="users")
    op.drop_column("users", "keycloak_id")
