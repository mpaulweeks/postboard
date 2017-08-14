from peewee import *

db = SqliteDatabase('postboard.db')

class Comment(Model):
    key = CharField()
    name = CharField()
    comment = TextField()
    created_at = DateField()

    class Meta:
        database = db
