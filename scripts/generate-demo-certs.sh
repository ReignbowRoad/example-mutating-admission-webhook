#!/bin/bash

# Script Parameters
HOST=$1
PASWORD=$2

# Certificate Subject
COUNTRY="GB"
STATE="Tyne and Wear"
LOCALITY="Newcastle Upon Tyne"
ORGANIZATION="Digital Wanderlust"
ORGANIZATION_UNIT="Platform Engineering"

usage() {
    echo "Usage: $0 --host <hostname> --password <password>"
    exit 1
}

# Parse options
while [[ $# -gt 0 ]]; do
    case "$1" in
        --host)
            HOST="$2"
            shift 2
            ;;
        --password)
            PASSWORD="$2"
            shift 2
            ;;
        *)
            echo "Error: Unknown option $1"
            usage
            ;;
    esac
done

# Check if required options are provided
if [[ -z $HOST ]]; then
    echo "HOST is required via '--host' parameter"
    usage
fi

if [[ -z $PASSWORD ]]; then
    echo "PASSWORD is required via the '--password' parameter"
    usage
fi

# Generate Self-Signed Root Certificates
openssl req \
   -x509 \
   -sha256 \
   -days 3650 \
   -newkey rsa:4096 \
   -keyout rootCA.key \
   -out rootCA.crt \
   -subj "/C=${COUNTRY}/ST=${STATE}/L=${LOCALITY}/O=${ORGANIZATION}/OU=${ORGANIZATION_UNIT}/CN=Root CA" \
   -passout pass:$PASSWORD

# Generate Private Key for Server certificate
openssl req \
   -new \
   -newkey rsa:4096 \
   -keyout tls.key \
   -out tls.csr \
   -nodes \
   -sha256 \
   -subj "/C=${COUNTRY}/ST=${STATE}/L=${LOCALITY}/O=${ORGANIZATION}/OU=${ORGANIZATION_UNIT}/CN=${HOST}" 

# Regenerate the ext file
echo "authorityKeyIdentifier=keyid,issuer" >> tls.ext
echo "basicConstraints=CA:FALSE" >> tls.ext
echo "subjectAltName = @alt_names" >> tls.ext
echo "[alt_names]" >> tls.ext
echo "DNS.1 = $HOST" >> tls.ext

# Generate Certificate Signing Request and generate private Key
openssl x509 \
   -req \
   -CA rootCA.crt \
   -CAkey rootCA.key \
   -in tls.csr \
   -out tls.crt \
   -days 365 \
   -CAcreateserial \
   -extfile tls.ext \
   -sha256 \
   -passin pass:$PASSWORD

# Clean Up
rm -rf tls.ext tls.csr rootCA.srl