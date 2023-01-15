#!/bin/sh

if [ -z "$1" ]
  then
    echo "Native build\n"
    docker build -t jeremyqzt/ribbonparser -f docker/Dockerfile .
    exit 0
fi

echo "Buildx build\n"
docker buildx build --push --platform=linux/arm64,linux/amd64 -f Docker/Dockerfile -t jeremyqzt/ribbonparser .
