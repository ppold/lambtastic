"""First revision.

Revision ID: 154d210ee5e7
Revises: None
Create Date: 2013-09-21 20:53:31.336363

"""

# revision identifiers, used by Alembic.
revision = '154d210ee5e7'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('landmark',
    sa.Column('key', sa.Integer(), nullable=False),
    sa.Column('name', sa.Unicode(), nullable=False),
    sa.Column('order', sa.Integer(), nullable=True),
    sa.Column('latitude', sa.String(), nullable=True),
    sa.Column('longitude', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('key')
    )
    op.create_table('kind',
    sa.Column('key', sa.Integer(), nullable=False),
    sa.Column('name', sa.Unicode(), nullable=False),
    sa.Column('order', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('key')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('kind')
    op.drop_table('landmark')
    ### end Alembic commands ###