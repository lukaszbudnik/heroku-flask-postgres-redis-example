# heroku-flask-postgres-redis-example

## Deploying to heroku

Fork this repo and execute the following commands:

```bash
heroku create
heroku buildpacks:set heroku/python
heroku buildpacks:add --index 1 heroku/go
heroku buildpacks:add --index 2 https://github.com/heroku/heroku-buildpack-pgbouncer.git

heroku addons:create heroku-postgresql:hobby-dev
heroku addons:create heroku-redis:hobby-dev
heroku addons:create newrelic:wayne
heroku addons:create logentries:le_tryit

git push heroku master

heroku open
```

## Running locally

If you're running on MacOs with Go and docker-machine installed all you have to do is to execute the following commands:

```bash
local/setup.sh
heroku local
```

# License

Copyright 2016 Łukasz Budnik

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   <http://www.apache.org/licenses/LICENSE-2.0>

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

