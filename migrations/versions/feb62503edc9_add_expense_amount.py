"""add expense amount

Revision ID: feb62503edc9
Revises: 17eec1603212
Create Date: 2020-02-02 10:10:46.404929

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'feb62503edc9'
down_revision = '17eec1603212'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('expense', sa.Column('amount', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('expense', 'amount')
    # ### end Alembic commands ###
