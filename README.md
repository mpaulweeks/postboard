# postboard
Simple comment service for demos

- [Flask](http://flask.pocoo.org/)
- [Peewee](http://docs.peewee-orm.com/en/latest/)

## Web UI

- [Comments](http://postboard.mpaulweeks.com/comments)
- [Payloads](http://postboard.mpaulweeks.com/payload)

## Install
```
.install/setup_venv.sh
.install/create_db.sh

.bash/bg_postboard.sh

...

.bash/kill_server.sh
```

See `install/nginx.conf`

## Tooling

To quickly dump tables and see contents:
```
echo 'select * from payload;' | sqlite3 postboard.db
echo 'select * from comment;' | sqlite3 postboard.db
```

## todo
- Open up CORS to github domain
- Pre-sort GET result to be newest first
