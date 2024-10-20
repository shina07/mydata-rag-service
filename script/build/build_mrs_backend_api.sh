#!/bin/bash
. ../mrs.config

DOCKER_BUILDKIT=1 docker build --target=runtime -t ${MRS_BACKEND_API_CONTAINER_NAME}:${MRS_BACKEND_API_TAG} -f ../../mrs-backend-api/Dockerfile ../..
