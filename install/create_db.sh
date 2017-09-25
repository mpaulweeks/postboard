rm postboard.db
source venv/bin/activate
POSTBOARD_DB=postboard.db python -m py.create_db
