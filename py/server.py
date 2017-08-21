import datetime
import json
import os

from flask import (
    Flask,
    redirect,
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


@app.route("/keys")
def get_keys():
    comments = (
        Comment
        .select(Comment.key)
        .distinct()
    )
    return json.dumps([c.key for c in comments])


@app.route("/comments/<key>")
def get_by_key(key):
    comments = (
        Comment
        .select()
        .where(Comment.key == key)
        .order_by(Comment.created_at.desc())
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
    if request.form.get('no_redirect'):
        return json.dumps(comment.to_dict())
    return redirect(request.form.get('next') or request.referrer)


if __name__ == "__main__":
    with open('server.pid', 'wt') as f:
        f.write(str(os.getpid()))
    app.run(host='0.0.0.0', port=os.environ['POSTBOARD_PORT'])
