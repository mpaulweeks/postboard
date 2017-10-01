import datetime
import json
import os

from flask import (
    Flask,
    abort,
    redirect,
    request,
)

from .model import (
    sqlite_db,
    Comment,
    Payload,
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
def get_comment_keys():
    comments = (
        Comment
        .select(Comment.key)
        .distinct()
    )
    return json.dumps([c.key for c in comments])


@app.route("/comments/<key>")
def get_comment_by_key(key):
    comments = (
        Comment
        .select()
        .where(Comment.key == key)
        .order_by(Comment.created_at.desc())
    )
    return json.dumps([c.to_dict() for c in comments])


@app.route("/comments", methods=['POST'])
def create_comment_by_key():
    comment = Comment.create(
        key=request.form['key'],
        name=request.form['name'],
        text=request.form['text'],
    )
    if request.form.get('no_redirect'):
        return json.dumps(comment.to_dict())
    destination = (
        request.form.get('next') or
        request.referrer or
        ''
    )
    return redirect(destination)


@app.route("/payload/<key>")
def get_payload_by_key(key):
    try:
        payload = Payload.get(Payload.key == key)
    except Exception:
        return abort(404)
    return payload.blob


@app.route("/payload", methods=['POST'])
def post_payload():
    data = request.json
    payload, _ = Payload.get_or_create(
        key=data['key'],
    )
    payload.blob = data['blob']
    payload.created_at = datetime.datetime.now()
    payload.save()
    if data.get('no_redirect'):
        return json.dumps(payload.to_dict())
    return redirect(request.form.get('next') or request.referrer)


if __name__ == "__main__":
    with open('server.pid', 'wt') as f:
        f.write(str(os.getpid()))
    app.run(host='0.0.0.0', port=os.environ['POSTBOARD_PORT'])
