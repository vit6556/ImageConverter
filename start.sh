#!/bin/bash

if test -f deploy/.env; 
then
    ENV_FILE=deploy/.env
else
    ENV_FILE=deploy/.env.sample
fi

docker-compose --env-file $ENV_FILE -f deploy/docker-compose.yml up -d --build