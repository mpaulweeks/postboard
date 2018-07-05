import datetime
import json
import os

from peewee import (
    SqliteDatabase,
    Model,
    PrimaryKeyField,
    CharField,
    TextField,
    DateTimeField,
)

sqlite_db = SqliteDatabase(os.environ['POSTBOARD_DB'])


class BaseModel(Model):
    class Meta:
        database = sqlite_db


class Comment(BaseModel):
    id = PrimaryKeyField()
    domain = CharField()
    key = CharField()
    name = CharField()
    text = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)

    def to_dict(self):
        return {
            'id': self.id,
            'domain': self.domain,
            'key': self.key,
            'name': self.name,
            'text': self.text,
            'created_at': self.created_at.isoformat(),
        }


class Note(BaseModel):
    id = PrimaryKeyField()
    domain = CharField()
    key = CharField()
    data = CharField()
    created_at = DateTimeField(default=datetime.datetime.now)

    def to_dict(self):
        return {
            'id': self.id,
            'domain': self.domain,
            'key': self.key,
            'data': json.loads(self.data),
            'created_at': self.created_at.isoformat(),
        }


class Payload(BaseModel):
    key = CharField()
    blob = TextField(null=True)
    created_at = DateTimeField(default=datetime.datetime.now)

    def to_dict(self):
        return {
            'key': self.key,
            'blob': self.blob,
            'created_at': self.created_at.isoformat(),
        }
