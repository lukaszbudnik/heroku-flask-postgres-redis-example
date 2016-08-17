web: bin/heroku-flask-postgres-redis-example & bin/start-pgbouncer-stunnel newrelic-admin run-program gunicorn web:app --log-file -
worker: newrelic-admin run-program python worker.py
