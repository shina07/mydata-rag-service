#!/bin/bash
. ../mrs.config

echo "${NETWORK}"
echo "${REGISTRY}"

docker run -d \
	--rm \
	--name mrs-backend-api \
	-p 8080:8080 \
	-e "PROFILE=dev" \
        --network ${NETWORK} \	
	mrs-backend-api:latest

