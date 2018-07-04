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
    data = {
        "comment_keys": Comment.select(Comment.key).distinct().count(),
        "comments": Comment.select().count(),
        "payloads": Payload.select().count(),
    }
    return json.dumps(data)


@app.route('/comments')
def input_comments():
    return app.send_static_file('comments.html')


@app.route('/payload')
def input_payload():
    return app.send_static_file('payload.html')


@app.route('/echo/test')
def input_echo():
    return app.send_static_file('echo_test.html')


@app.route('/static/echo.js')
def static_echo_js():
    return app.send_static_file('echo.js')


@app.route('/static/echo.css')
def static_echo_css():
    return app.send_static_file('echo.css')


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
        return ''
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


echo_html = """
<html>
<head>
    <title>Postboard Echo</title>

    <script id="echo" type="application/json">%s</script>

    <link rel="stylesheet" href="static/echo.css?v=%s">
    <script defer src="static/echo.js?v=%s"></script>
</head>
<body>
</body>
</html>
"""


def get_cache_bust():
    time_diff = datetime.datetime.now() - datetime.datetime(1, 1, 1)
    return int(time_diff.total_seconds())


@app.route('/echo', methods=['POST'])
def post_echo():
    data = {
        key: value[0] if len(value) == 1 else value
        for key, value in request.form.iterlists()
    }
    cache_bust = get_cache_bust()
    return echo_html % (
        json.dumps(data),
        cache_bust,
        cache_bust,
    )


if __name__ == '__main__':
    with open('server.pid', 'wt') as f:
        f.write(str(os.getpid()))
    app.run(host='0.0.0.0', port=os.environ['POSTBOARD_PORT'])
