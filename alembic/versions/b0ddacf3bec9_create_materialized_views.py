"""create materialized views

Revision ID: b0ddacf3bec9
Revises: 453d6ea5323e
Create Date: 2025-06-06 13:06:26.501548

"""
from typing import Sequence, Union

from alembic import op

revision: str = 'b0ddacf3bec9'
down_revision: Union[str, None] = '2e1821eac24f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(open("sql/popular_books_mv.sql").read())
    op.execute(open("sql/idx_popular_books.sql").read())
    op.execute(open("sql/book_rating_stats_mv.sql").read())
    op.execute(open("sql/idx_book_rating_stats.sql").read())
    op.execute(open("sql/top_authors_mv.sql").read())
    op.execute(open("sql/idx_top_authors.sql").read())
    op.execute(open("sql/review_stats_mv.sql").read())


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP MATERIALIZED VIEW IF EXISTS popular_books")
    op.execute("DROP INDEX IF EXISTS idx_popular_books_book_id")
    op.execute("DROP MATERIALIZED VIEW IF EXISTS book_rating_stats")
    op.execute("DROP INDEX IF EXISTS idx_book_rating_stats_book_id")
    op.execute("DROP MATERIALIZED VIEW IF EXISTS top_authors")
    op.execute("DROP INDEX IF EXISTS idx_top_authors_author_id")
    op.execute("DROP MATERIALIZED VIEW IF EXISTS review_stats")
