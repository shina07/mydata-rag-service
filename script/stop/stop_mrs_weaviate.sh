#!/bin/bash
. ../mrs.config

docker stop ${MRS_WEAVIATE_CONTAINER_NAME}
