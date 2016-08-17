#!/bin/bash

for i in `seq 1 100`;
do
  url=`heroku info | grep 'Web URL' | awk -F ": " '{print $2}' | xargs`
  curl $url
done
