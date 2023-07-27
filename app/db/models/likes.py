import sqlalchemy

from .users import users_table
from .posts import posts_table

metadata = sqlalchemy.MetaData()

likes_table = sqlalchemy.Table(
    "likes",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("user_id", sqlalchemy.ForeignKey(users_table.c.id)),
    sqlalchemy.Column("post_id", sqlalchemy.ForeignKey(posts_table.c.id)),
)

dislikes_table = sqlalchemy.Table(
    "dislikes",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("user_id", sqlalchemy.ForeignKey(users_table.c.id)),
    sqlalchemy.Column("post_id", sqlalchemy.ForeignKey(posts_table.c.id)),
)
