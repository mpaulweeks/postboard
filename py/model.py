import os

from peewee import (
    SqliteDatabase,
    Model,
    CharField,
    TextField,
    DateTimeField,
)

sqlite_db = SqliteDatabase(os.environ['POSTBOARD_DB'])


class BaseModel(Model):
    class Meta:
        database = sqlite_db


class Comment(BaseModel):
    key = CharField()
    name = CharField()
    text = TextField()
    created_at = DateTimeField()

    def to_dict(self):
        return {
            'key': self.key,
            'name': self.name,
            'text': self.text,
            'created_at': self.created_at.isoformat(),
        }
