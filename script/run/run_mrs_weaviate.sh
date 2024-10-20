#!/bin/bash
. ../mrs.config

echo "IMAGE NAME: ${MRS_WEAVIATE_CONTAINER_NAME}:${MRS_WEAVIATE_TAG}"
echo "NETWORK: ${MRS_NETWORK}"

docker run -d \
    --rm \
    --name ${MRS_WEAVIATE_CONTAINER_NAME} \
    --network ${MRS_NETWORK}  \
    -p 7070:8080 \
    -e "PROFILE=dev" \
    ${MRS_WEAVIATE_CONTAINER_NAME}:${MRS_WEAVIATE_TAG}
