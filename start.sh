#!/bin/bash
app="flask-api"
docker build -t ${app} .
docker run -d -p 127.0.0.1:5000:5000 \
  --name=${app} \
  -v $PWD:/app ${app}