"""Initial migration.

Revision ID: 1d88d7ad1346
Revises: 
Create Date: 2025-03-09 02:03:21.313059

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '1d88d7ad1346'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('gra_action_hub', schema=None) as batch_op:
        batch_op.drop_index('idx_ah_created_at')
        batch_op.drop_index('idx_ah_mentioned_user_id')
        batch_op.drop_index('idx_ah_report_id')
        batch_op.drop_index('idx_ah_section_id')
        batch_op.drop_index('idx_ah_type')
        batch_op.drop_index('idx_ah_user_id')

    op.drop_table('gra_action_hub')
    op.drop_table('users')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('email', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('password', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='users_pkey'),
    sa.UniqueConstraint('email', name='users_email_key')
    )
    op.create_table('gra_action_hub',
    sa.Column('ah_id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('ah_type', sa.VARCHAR(length=50), autoincrement=False, nullable=False),
    sa.Column('ah_report_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('ah_user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('ah_content', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('ah_created_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=False),
    sa.Column('ah_updated_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('ah_status', sa.SMALLINT(), server_default=sa.text('1'), autoincrement=False, nullable=False),
    sa.Column('ah_parent_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('ah_mentioned_user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('ah_is_read', sa.BOOLEAN(), server_default=sa.text('false'), autoincrement=False, nullable=True),
    sa.Column('ah_section_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('ah_subsection_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('ah_last_read_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('ah_id', name='gra_action_hub_pkey')
    )
    with op.batch_alter_table('gra_action_hub', schema=None) as batch_op:
        batch_op.create_index('idx_ah_user_id', ['ah_user_id'], unique=False)
        batch_op.create_index('idx_ah_type', ['ah_type'], unique=False)
        batch_op.create_index('idx_ah_section_id', ['ah_section_id'], unique=False)
        batch_op.create_index('idx_ah_report_id', ['ah_report_id'], unique=False)
        batch_op.create_index('idx_ah_mentioned_user_id', ['ah_mentioned_user_id'], unique=False)
        batch_op.create_index('idx_ah_created_at', ['ah_created_at'], unique=False)

    # ### end Alembic commands ###
