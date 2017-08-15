import datetime
import json
import os

from flask import (
    Flask,
    request,
)

from .model import (
    sqlite_db,
    Comment,
)


app = Flask(__name__)


@app.before_request
def before_request():
    sqlite_db.get_conn()


@app.after_request
def after_request(response):
    sqlite_db.close()
    return response


@app.route('/')
def root():
    return app.send_static_file('index.html')


@app.route("/health")
def health():
    return "ok"


@app.route("/comments/<key>")
def get_by_key(key):
    comments = (
        Comment
        .select()
        .where(Comment.key == key)
    )
    return json.dumps([c.to_dict() for c in comments])


@app.route("/comments", methods=['POST'])
def create():
    comment = Comment.create(
        key=request.form['key'],
        name=request.form['name'],
        text=request.form['text'],
        created_at=datetime.datetime.now()
    )
    return json.dumps(comment.to_dict())


if __name__ == "__main__":
    with open('server.pid', 'wt') as f:
        f.write(str(os.getpid()))
    app.run(host='0.0.0.0', port=os.environ['POSTBOARD_PORT'])
