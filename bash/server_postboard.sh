touch server.pid
source venv/bin/activate
HEALTH_PORT=5200 python -m py.server
