from .model import (
    sqlite_db,
    Comment,
    Note,
    Payload,
)

if __name__ == "__main__":
    sqlite_db.connect()
    sqlite_db.create_tables([Comment, Note, Payload])
