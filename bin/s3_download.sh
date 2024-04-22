#!/usr/bin/env bash

# User Minio Vars
HOST="s3.example.com"
USERNAME="<access_key>"
PASSWORD="<secret_key>"
BUCKET="<bucket_name>"
FILE="folder/file123_name.xml"
MINIO_PATH="/${BUCKET}/${FILE}"
OUT_FILE="./file123_name.xml"

# Static Vars
DATE=$(date -R --utc)
CONTENT_TYPE='application/zstd'
SIG_STRING="GET\n\n${CONTENT_TYPE}\n${DATE}\n${MINIO_PATH}"
SIGNATURE="$(echo -en "${SIG_STRING}" | openssl sha1 -hmac "${PASSWORD}" -binary | base64)"

curl -k -v \
    -o "${OUT_FILE}" \
    -H "Host: $HOST" \
    -H "Date: ${DATE}" \
    -H "Content-Type: ${CONTENT_TYPE}" \
    -H "Authorization: AWS ${USERNAME}:${SIGNATURE}" \
    "https://$HOST${MINIO_PATH}"

# curl -k -v -x http://proxy.example.com:8080 \
#     -o "${OUT_FILE}" \
#     -H "Host: $HOST" \
#     -H "Date: ${DATE}" \
#     -H "Content-Type: ${CONTENT_TYPE}" \
#     -H "Authorization: AWS ${USERNAME}:${SIGNATURE}" \
#     "https://$HOST${MINIO_PATH}"
