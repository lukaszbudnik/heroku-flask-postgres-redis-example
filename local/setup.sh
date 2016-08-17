#!/bin/bash

BASEDIR=$(dirname "$0")
cd $BASEDIR/..

echo "Creating bin directory"

if [ ! -d "bin" ]; then
  mkdir bin
fi

echo "Mocking start-pgbouncer-stunnel"

cp $BASEDIR/start-pgbouncer-stunnel bin

echo "Building migrator.go"

go build -o bin/heroku-flask-postgres-redis-example

echo "Starting redis docker container"

docker run -P --name hfpr-redis -d redis
sleep 5

echo "Starting postgres docker container"

docker run -P --name hfpr-postgres -d postgres
sleep 5

docker_ip=`docker-machine ip default`
redis_port=`docker inspect --format='{{(index (index .NetworkSettings.Ports "6379/tcp") 0).HostPort}}' hfpr-redis`
postgres_port=`docker inspect --format='{{(index (index .NetworkSettings.Ports "5432/tcp") 0).HostPort}}' hfpr-postgres`

echo "Generating .env file"

cat > .env << EOF
DATABASE_URL=postgres://postgres@$docker_ip:$postgres_port?sslmode=disable
REDIS_URL=redis://$docker_ip:$redis_port
EOF

echo "All done. To start application locally run:"
echo "heroku local"
