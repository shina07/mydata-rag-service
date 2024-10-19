#!/bin/bash
. mrs.config

DOCKER_BUILDKIT=1 docker build --target=runtime -t ${REGISTRY}/mrs-backend-api:latest -f ../../mrs-backend-api/Dockerfile ../..
docker restart mrs-backend-api
