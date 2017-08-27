from .model import (
    sqlite_db,
    Comment,
    Payload,
)

if __name__ == "__main__":
    sqlite_db.connect()
    sqlite_db.create_tables([Comment, Payload])
