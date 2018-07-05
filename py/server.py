import datetime
import json
import os

from flask import (
    Flask,
    jsonify,
    redirect,
    request,
)

from .model import (
    sqlite_db,
    gen_nonce,
    Comment,
    Note,
    Payload,
)


app = Flask(__name__)


###########################
#   HELPERS
###########################

def decide_redirect(req, message):
    if req.form.get('no_redirect'):
        return message
    destination = req.form.get('next') or req.referrer
    if destination:
        return redirect(destination)
    else:
        return app.send_static_file('back.html')


def get_complete_form_data(r):
    return {
        key: value[0] if len(value) == 1 else value
        for key, value in r.form.iterlists()
        if key not in ['no_redirect', 'next']
    }


@app.before_request
def before_request():
    sqlite_db.get_conn()


@app.after_request
def after_request(response):
    sqlite_db.close()
    return response


###########################
#   WEB VIEW
###########################


@app.route('/')
def root():
    return redirect('/health')


@app.route('/health')
def health():
    data = {
        "comment_keys": Comment.select(Comment.key).distinct().count(),
        "comments": Comment.select().count(),
        "note_keys": Note.select(Note.key).distinct().count(),
        "notes": Note.select().count(),
        "payloads": Payload.select().count(),
    }
    return jsonify(data)


@app.route('/comments')
def input_comments():
    return app.send_static_file('comments.html')


@app.route('/notes')
def input_notes():
    return app.send_static_file('notes.html')


@app.route('/payload')
def input_payload():
    return app.send_static_file('payload.html')


@app.route('/echo/test')
def input_echo():
    return app.send_static_file('echo_test.html')


###########################
#   STATIC FILES
###########################


@app.route('/static/echo.js')
def static_echo_js():
    return app.send_static_file('echo.js')


@app.route('/static/echo.css')
def static_echo_css():
    return app.send_static_file('echo.css')


###########################
#   COMMENTS
###########################


@app.route('/comments/<domain>/keys')
def get_comment_keys(domain):
    comments = (
        Comment
        .select(Comment.key)
        .where(Comment.domain == domain)
        .distinct()
    )
    return jsonify([c.key for c in comments])


@app.route('/comments/<domain>/<key>')
def get_comments_by_key(domain, key):
    comments = (
        Comment
        .select()
        .where(Comment.domain == domain and Comment.key == key)
        .order_by(Comment.created_at.desc())
    )
    return jsonify([c.to_dict() for c in comments])


@app.route('/comments/<domain>/<key>', methods=['POST'])
def create_comment_by_key(domain, key):
    comment = Comment.create(
        domain=domain,
        key=key,
        name=request.form['name'],
        text=request.form['text'],
    )
    return decide_redirect(request, jsonify(comment.to_dict()))


@app.route('/delete/comment/<domain>/<key>/<id>')  # GET for easy teaching
def delete_comment(domain, key, id):
    comment = Comment.get(Comment.id == id)
    if comment.domain == domain and comment.key == key:
        comment.delete_instance()
    return decide_redirect(request, jsonify(comment.to_dict()))


###########################
#   NOTES
###########################


@app.route('/notes/<domain>/keys')
def get_note_keys(domain):
    notes = (
        Note
        .select(Note.key)
        .where(Note.domain == domain)
        .distinct()
    )
    return jsonify([c.key for c in notes])


@app.route('/notes/<domain>/<key>')
def get_notes_by_key(domain, key):
    notes = (
        Note
        .select()
        .where(Note.domain == domain and Note.key == key)
        .order_by(Note.created_at.desc())
    )
    return jsonify([c.to_dict() for c in notes])


@app.route('/notes/<domain>/<key>', methods=['POST'])
def create_note_by_key(domain, key):
    note = Note.create(
        domain=domain,
        key=key,
        data=json.dumps(get_complete_form_data(request)),
    )
    return decide_redirect(request, jsonify(note.to_dict()))


@app.route('/delete/note/<domain>/<key>/<id>')  # GET for easy teaching
def delete_note(domain, key, id):
    note = Note.get(Note.id == id)
    if note.domain == domain and note.key == key:
        note.delete_instance()
    return decide_redirect(request, jsonify(note.to_dict()))


###########################
#   PAYLOAD
###########################


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
    return decide_redirect(request, jsonify(payload.to_dict()))


###########################
#   ECHO
###########################


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


@app.route('/echo', methods=['POST'])
def post_echo():
    data = get_complete_form_data(request)
    cache_bust = gen_nonce()
    return echo_html % (
        json.dumps(data),
        cache_bust,
        cache_bust,
    )


###########################
#   MAIN
###########################


if __name__ == '__main__':
    with open('server.pid', 'wt') as f:
        f.write(str(os.getpid()))
    app.run(host='0.0.0.0', port=os.environ['POSTBOARD_PORT'])
