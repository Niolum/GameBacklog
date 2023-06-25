"""add ondelete to m2m backlog_game and complete_game

Revision ID: f1326bf1ab6e
Revises: 57dcd497030a
Create Date: 2023-06-25 20:36:30.905469

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f1326bf1ab6e'
down_revision = '57dcd497030a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('backlog_game_backlog_id_fkey', 'backlog_game', type_='foreignkey')
    op.drop_constraint('backlog_game_game_id_fkey', 'backlog_game', type_='foreignkey')
    op.create_foreign_key(None, 'backlog_game', 'games', ['game_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'backlog_game', 'backlogs', ['backlog_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('completegame_game_game_id_fkey', 'completegame_game', type_='foreignkey')
    op.drop_constraint('completegame_game_complete_game_id_fkey', 'completegame_game', type_='foreignkey')
    op.create_foreign_key(None, 'completegame_game', 'games', ['game_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'completegame_game', 'completegames', ['complete_game_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'completegame_game', type_='foreignkey')
    op.drop_constraint(None, 'completegame_game', type_='foreignkey')
    op.create_foreign_key('completegame_game_complete_game_id_fkey', 'completegame_game', 'completegames', ['complete_game_id'], ['id'])
    op.create_foreign_key('completegame_game_game_id_fkey', 'completegame_game', 'games', ['game_id'], ['id'])
    op.drop_constraint(None, 'backlog_game', type_='foreignkey')
    op.drop_constraint(None, 'backlog_game', type_='foreignkey')
    op.create_foreign_key('backlog_game_game_id_fkey', 'backlog_game', 'games', ['game_id'], ['id'])
    op.create_foreign_key('backlog_game_backlog_id_fkey', 'backlog_game', 'backlogs', ['backlog_id'], ['id'])
    # ### end Alembic commands ###