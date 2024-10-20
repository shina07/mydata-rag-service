#!/bin/bash
. ../mrs.config

docker stop ${MRS_BACKEND_API_CONTAINER_NAME}
