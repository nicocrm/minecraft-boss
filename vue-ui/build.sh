#!/bin/sh

docker build -t build-vue .
docker run -v `pwd`/dist:/dist --rm build-vue cp -v -a /build/dist/. /dist
