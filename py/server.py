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


def decide_redirect(req, message):
    if req.form.get('no_redirect'):
        return message
    destination = req.form.get('next') or req.referrer
    if destination:
        return redirect(destination)
    else:
        return app.send_static_file('back.html')


@app.before_request
def before_request():
    sqlite_db.get_conn()


@app.after_request
def after_request(response):
    sqlite_db.close()
    return response


@app.route('/')
def root():
    return redirect('/health')


@app.route('/health')
def health():
    return 'ok'


@app.route('/comments')
def input_comments():
    return app.send_static_file('comments.html')


@app.route('/payload')
def input_payload():
    return app.send_static_file('payload.html')



@app.route('/<domain>/keys')
def get_comment_keys(domain):
    comments = (
        Comment
        .select(Comment.key)
        .where(Comment.domain == domain)
        .distinct()
    )
    return json.dumps([c.key for c in comments])


@app.route('/comments/<domain>/<key>')
def get_comment_by_key(domain, key):
    comments = (
        Comment
        .select()
        .where(Comment.domain == domain and Comment.key == key)
        .order_by(Comment.created_at.desc())
    )
    return json.dumps([c.to_dict() for c in comments])


@app.route('/comments/<domain>/<key>', methods=['POST'])
def create_comment_by_key(domain, key):
    comment = Comment.create(
        domain=domain,
        key=key,
        name=request.form['name'],
        text=request.form['text'],
    )
    return decide_redirect(request, json.dumps(comment.to_dict()))


@app.route('/delete/comment/<domain>/<key>/<id>')  # GET for easy teaching
def delete_comment(domain, key, id):
    comment = Comment.get(Comment.id == id)
    if comment.domain == domain and comment.key == key:
        comment.delete_instance()
    return decide_redirect(request, json.dumps(comment.to_dict()))


@app.route('/payload/<key>')
def get_payload_by_key(key):
    try:
        payload = Payload.get(Payload.key == key)
    except Exception:
        return abort(404)
    return payload.blob


@app.route('/payload', methods=['POST'])
def post_payload():
    payload, _ = Payload.get_or_create(
        key=request.form['key'],
    )
    payload.blob = request.form['blob']
    payload.created_at = datetime.datetime.now()
    payload.save()
    return decide_redirect(request, json.dumps(payload.to_dict()))


if __name__ == '__main__':
    with open('server.pid', 'wt') as f:
        f.write(str(os.getpid()))
    app.run(host='0.0.0.0', port=os.environ['POSTBOARD_PORT'])
