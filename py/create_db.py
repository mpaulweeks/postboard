from model import (
  db,
  Comment,
)

if __name__ == "__main__":
  db.connect()
  db.create_tables([Comment])
