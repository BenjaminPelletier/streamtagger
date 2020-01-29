"""Pre-SQLAlchemy configuration

Revision ID: fe56db612174
Revises: 
Create Date: 2019-12-05 15:36:21.982046

"""
from alembic import op
import sqlalchemy as sa
from app.lib.db_uuid import UUID

# revision identifiers, used by Alembic.
revision = 'fe56db612174'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', UUID(), server_default=sa.text('(gen_random_uuid())'), nullable=False),
    sa.Column('username', sa.String(), nullable=True),
    sa.Column('password_hash', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('sessions',
    sa.Column('id', UUID(), server_default=sa.text('(gen_random_uuid())'), nullable=False),
    sa.Column('user_id', UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('created_ip', sa.String(), nullable=False),
    sa.Column('last_used', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('songs',
    sa.Column('id', UUID(), server_default=sa.text('(gen_random_uuid())'), nullable=False),
    sa.Column('path', sa.String(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('artist', sa.String(), nullable=True),
    sa.Column('added_at', sa.DateTime(), nullable=False),
    sa.Column('added_by', UUID(), nullable=True),
    sa.ForeignKeyConstraint(['added_by'], ['users.id'], ondelete='RESTRICT'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('path')
    )
    op.create_table('tag_definitions',
    sa.Column('id', UUID(), server_default=sa.text('(gen_random_uuid())'), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('type', sa.String(), nullable=False),
    sa.Column('created_by', UUID(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['created_by'], ['users.id'], ondelete='RESTRICT'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('tags',
    sa.Column('tag_id', UUID(), nullable=False),
    sa.Column('song_id', UUID(), nullable=False),
    sa.Column('user_id', UUID(), nullable=False),
    sa.Column('value', sa.Integer(), nullable=True),
    sa.Column('last_changed', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['song_id'], ['songs.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['tag_id'], ['tag_definitions.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('tag_id', 'song_id', 'user_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tags')
    op.drop_table('tag_definitions')
    op.drop_table('songs')
    op.drop_table('sessions')
    op.drop_table('users')
    # ### end Alembic commands ###