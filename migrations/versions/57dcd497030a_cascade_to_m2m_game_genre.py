"""cascade to m2m game_genre

Revision ID: 57dcd497030a
Revises: 385b676965a7
Create Date: 2023-06-25 18:52:42.220480

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '57dcd497030a'
down_revision = '385b676965a7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('game_genre_genre_id_fkey', 'game_genre', type_='foreignkey')
    op.drop_constraint('game_genre_game_id_fkey', 'game_genre', type_='foreignkey')
    op.create_foreign_key(None, 'game_genre', 'genres', ['genre_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'game_genre', 'games', ['game_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('genres_user_id_fkey', 'genres', type_='foreignkey')
    op.create_foreign_key(None, 'genres', 'users', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'genres', type_='foreignkey')
    op.create_foreign_key('genres_user_id_fkey', 'genres', 'users', ['user_id'], ['id'], ondelete='SET NULL')
    op.drop_constraint(None, 'game_genre', type_='foreignkey')
    op.drop_constraint(None, 'game_genre', type_='foreignkey')
    op.create_foreign_key('game_genre_game_id_fkey', 'game_genre', 'games', ['game_id'], ['id'])
    op.create_foreign_key('game_genre_genre_id_fkey', 'game_genre', 'genres', ['genre_id'], ['id'])
    # ### end Alembic commands ###
