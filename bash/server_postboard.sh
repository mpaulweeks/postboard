touch server.pid
source venv/bin/activate
POSTBOARD_DB=postboard.db POSTBOARD_PORT=5200 python -m py.server
