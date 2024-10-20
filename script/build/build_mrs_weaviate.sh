#!/bin/bash
. ../mrs.config

docker pull semitechnologies/weaviate:${MRS_WEAVIATE_TAG}
docker tag semitechnologies/weaviate:${MRS_WEAVIATE_TAG} ${MRS_WEAVIATE_CONTAINER_NAME}:${MRS_WEAVIATE_TAG}
