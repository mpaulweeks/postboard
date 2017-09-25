# postboard
Simple comment service for demos

- [Flask](http://flask.pocoo.org/)
- [Peewee](http://docs.peewee-orm.com/en/latest/)

## Install
```
.bash/setup_venv.sh
.bash/create_db.sh
.bash/bg_postboard.sh

...

.bash/kill_server.sh
```

## todo
- Open up CORS to github domain
- Healthcheck returns total number of rows, maybe db size?
- Pre-sort GET result to be newest first
