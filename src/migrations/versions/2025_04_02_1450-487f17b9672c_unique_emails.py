"""unique emails

Revision ID: 487f17b9672c
Revises: 9304ddac416a
Create Date: 2025-04-02 14:50:23.745617

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "487f17b9672c"
down_revision: Union[str, None] = "9304ddac416a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(None, "users", ["email"])



def downgrade() -> None:
    op.drop_constraint(None, "users", type_="unique")

