#!/bin/bash
. ../mrs.config

echo "IMAGE NAME: ${MRS_WEAVIATE_CONTAINER_NAME}:${MRS_WEAVIATE_TAG}"
echo "NETWORK: ${MRS_NETWORK}"

docker run -d \
    --rm \
    --name ${MRS_WEAVIATE_CONTAINER_NAME} \
    --network ${MRS_NETWORK}  \
    -p 7070:8080 \
    -p 50051:50051 \
    -e "PROFILE=dev" \
    -e "QUERY_DEFAULTS_LIMIT=25" \
    -e "AUTHENTICATION_ANANYMOUS_ACCESS_ENABLED=true" \
    -e "PERSISTENCE_DATA_PATH=/var/lib/weaviate" \
    -e "DEFAULT_VECTORIZER_MODULE=none" \
    -e "ENABLE_API_BASED_MODULES=true" \
    -e "CLUSTER_HOSTNAME=mrs-weaviate-master" \
    -v ${MRS_DATA}/${MRS_WEAVIATE_CONTAINER_NAME}:/var/lib/weaviate \
    ${MRS_WEAVIATE_CONTAINER_NAME}:${MRS_WEAVIATE_TAG}
