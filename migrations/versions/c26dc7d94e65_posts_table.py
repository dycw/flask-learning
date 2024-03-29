"""posts table

Revision ID: c26dc7d94e65
Revises: ea34a60a283d
Create Date: 2021-03-09 21:59:42.493039

"""
import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = "c26dc7d94e65"
down_revision = "ea34a60a283d"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "post",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("body", sa.String(length=140), nullable=True),
        sa.Column("timestamp", sa.DateTime(), nullable=True),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["user.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_post_timestamp"), "post", ["timestamp"], unique=False
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_post_timestamp"), table_name="post")
    op.drop_table("post")
    # ### end Alembic commands ###
