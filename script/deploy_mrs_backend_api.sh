#!/bin/bash
. ./mrs.config

DOCKER_BUILDKIT=1 docker build --target=runtime -t ${MRS_BACKEND_API_CONTAINER_NAME}:${MRS_BACKEND_API_TAG} -f ../mrs-backend-api/Dockerfile ..

docker stop ${MRS_BACKEND_API_CONTAINER_NAME}

docker run -d \
	--rm \
	--name ${MRS_BACKEND_API_CONTAINER_NAME}  \
	--network ${MRS_NETWORK}  \
	-p 8080:8080 \
	-e "PROFILE=dev" \
	${MRS_BACKEND_API_CONTAINER_NAME}:${MRS_BACKEND_API_TAG}
