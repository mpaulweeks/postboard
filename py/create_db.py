from .model import (
    sqlite_db,
    Comment,
)

if __name__ == "__main__":
    sqlite_db.connect()
    sqlite_db.create_tables([Comment])
