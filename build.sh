#!/bin/sh

VERSION=$(git log -1 --pretty=%h)
IMAGE="jeremyqzt/ribbonparser:$VERSION"

if [ -z "$1" ]
  then
    echo "Native build\n"
    docker build -t jeremyqzt/ribbonparser -f docker/Dockerfile .
    exit 0
fi

echo "Buildx build\n"
eval "docker buildx build --push --platform=linux/arm64,linux/amd64 -f Docker/Dockerfile -t jeremyqzt/ribbonparser:$VERSION ."

IMAGE="jeremyqzt/ribbonparser:$VERSION" envsubst < k8s/ribbonparser.yaml | kubectl apply -f -