#!/bin/bash
. ../mrs.config

echo "IMAGE NAME: ${MRS_BACKEND_API_CONTAINER_NAME}:${MRS_BACKEND_API_TAG}"
echo "NETWORK: ${MRS_NETWORK}"

docker run -d \
	--rm \
	--name ${MRS_BACKEND_API_CONTAINER_NAME}  \
	--network ${MRS_NETWORK}  \
	-p 8080:8080 \
	-e "PROFILE=dev" \
	${MRS_BACKEND_API_CONTAINER_NAME}:${MRS_BACKEND_API_TAG}
