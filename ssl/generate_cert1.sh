#!/bin/bash

# Certificate Authority
openssl req -new -x509 -days 360 -keyout ca.key \
	-subj "/C=NL/ST=Drenthe/L=Assen/O=Hanze/CN=192.168.0.103" \
    -extensions v3_ca \
	-out ca.crt

# Server 
openssl req -newkey rsa:2048 -nodes -keyout server.key -subj "/C=NL/ST=Drenthe/L=Assen/O=Hanze/CN=192.168.0.102" \
    -out server.csr
openssl x509 -req -extfile <(printf "subjectAltName=IP:127.0.0.1,IP:192.168.0.102") \
	-days 360 -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial \
	-out server.crt

# Client
openssl req -newkey rsa:2048 -nodes -keyout client.key -subj "/C=NL/ST=Drenthe/L=Assen/O=Hanze/CN=192.168.0.7" \
    -out client.csr
openssl x509 -req -extfile <(printf "subjectAltName=IP:127.0.0.1,IP:192.168.0.7") \
	-days 360 -in client.csr -CA ca.crt -CAkey ca.key -CAcreateserial \
	-out client.crt
