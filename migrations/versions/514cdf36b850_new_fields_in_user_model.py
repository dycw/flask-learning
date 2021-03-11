"""new fields in user model

Revision ID: 514cdf36b850
Revises: c26dc7d94e65
Create Date: 2021-03-11 21:40:47.122430

"""
import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = "514cdf36b850"
down_revision = "c26dc7d94e65"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "user", sa.Column("about_me", sa.String(length=140), nullable=True)
    )
    op.add_column("user", sa.Column("last_seen", sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("user", "last_seen")
    op.drop_column("user", "about_me")
    # ### end Alembic commands ###
