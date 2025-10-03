"""make user email unique

Revision ID: 6295f8d5c8c2
Revises: 0caffc2960f2
Create Date: 2024-11-17 11:30:31.570392

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "6295f8d5c8c2"
down_revision: Union[str, None] = "0caffc2960f2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(None, "users", ["email"])


def downgrade() -> None:
    op.drop_constraint(None, "users", type_="unique")
