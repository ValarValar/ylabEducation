"""readd user model

Revision ID: 6c80e6891cd6
Revises: 326f6db5d93d
Create Date: 2022-07-19 21:33:10.223401

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = '6c80e6891cd6'
down_revision = '326f6db5d93d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    pass
    # ### commands auto generated by Alembic - please adjust! ###

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
