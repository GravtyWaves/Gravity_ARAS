"""add_fulltext_search_to_articles

Revision ID: c2352ab4b554
Revises: 278207100710
Create Date: 2025-11-13 09:25:22.917832

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c2352ab4b554'
down_revision: Union[str, Sequence[str], None] = '278207100710'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add full-text search support to news_articles table."""
    # Add tsvector column for full-text search
    op.execute("""
        ALTER TABLE news_articles 
        ADD COLUMN search_vector tsvector
        GENERATED ALWAYS AS (
            setweight(to_tsvector('english', coalesce(title, '')), 'A') ||
            setweight(to_tsvector('english', coalesce(content, '')), 'B') ||
            setweight(to_tsvector('english', coalesce(summary, '')), 'C')
        ) STORED;
    """)
    
    # Create GIN index for fast full-text search
    op.create_index(
        'ix_news_articles_search_vector',
        'news_articles',
        ['search_vector'],
        postgresql_using='gin'
    )
    
    # Add URL constraint to ensure uniqueness
    op.create_index(
        'ix_news_articles_url_unique',
        'news_articles',
        ['url'],
        unique=True
    )


def downgrade() -> None:
    """Remove full-text search support."""
    op.drop_index('ix_news_articles_search_vector', table_name='news_articles')
    op.drop_index('ix_news_articles_url_unique', table_name='news_articles')
    op.execute("ALTER TABLE news_articles DROP COLUMN search_vector;")
