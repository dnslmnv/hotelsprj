"""user table column rename

Revision ID: 9304ddac416a
Revises: 2088f04673e7
Create Date: 2025-04-02 14:23:05.290625

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "9304ddac416a"
down_revision: Union[str, None] = "2088f04673e7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "users", sa.Column("hashed_password", sa.String(length=200), nullable=False)
    )
    op.drop_column("users", "password")



def downgrade() -> None:
    op.add_column(
        "users",
        sa.Column(
            "password", sa.VARCHAR(length=200), autoincrement=False, nullable=False
        ),
    )
    op.drop_column("users", "hashed_password")

