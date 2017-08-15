from peewee import (
    SqliteDatabase,
    Model,
    CharField,
    TextField,
    DateField,
)

sqlite_db = SqliteDatabase('postboard.db')


class BaseModel(Model):
    class Meta:
        database = sqlite_db


class Comment(BaseModel):
    key = CharField()
    name = CharField()
    text = TextField()
    created_at = DateField()
