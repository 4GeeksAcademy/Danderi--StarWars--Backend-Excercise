"""empty message

Revision ID: abe84d17f77d
Revises: 87462374cebc
Create Date: 2024-04-28 01:23:54.045317

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'abe84d17f77d'
down_revision = '87462374cebc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('planets',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=120), nullable=False),
    sa.Column('gravity', sa.Integer(), nullable=True),
    sa.Column('population', sa.Integer(), nullable=True),
    sa.Column('climate', sa.String(length=80), nullable=True),
    sa.Column('diameter', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('planets')
    # ### end Alembic commands ###