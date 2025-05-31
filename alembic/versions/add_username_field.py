"""add username field

Revision ID: add_username_field
Revises: 
Create Date: 2024-03-21 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# revision identifiers, used by Alembic.
revision = 'add_username_field'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    logger.info("Starting upgrade: adding username field")
    # use native SQL to add column
    op.execute('ALTER TABLE users ADD COLUMN username VARCHAR')
    logger.info("Added username column")
    
    # create unique index
    op.execute('CREATE UNIQUE INDEX ix_users_username ON users (username)')
    logger.info("Created username index")


def downgrade() -> None:
    logger.info("Starting downgrade: removing username field")
    # drop index
    op.execute('DROP INDEX IF EXISTS ix_users_username')
    logger.info("Dropped username index")
    
    # drop column
    op.execute('ALTER TABLE users DROP COLUMN IF EXISTS username')
    logger.info("Dropped username column") 