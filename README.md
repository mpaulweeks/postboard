# postboard
Simple comment service for demos

- [Flask](http://flask.pocoo.org/)
- [Peewee](http://docs.peewee-orm.com/en/latest/)

## Install
```
.install/setup_venv.sh
.install/create_db.sh

.bash/bg_postboard.sh

...

.bash/kill_server.sh
```

See `install/nginx.conf`

## todo
- Open up CORS to github domain
- Healthcheck returns total number of rows, maybe db size?
- Pre-sort GET result to be newest first
