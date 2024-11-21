#!/bin/bash
cp /run/secrets/elasticsearch_password /usr/share/elasticsearch/config/elasticsearch_password
chmod 0400 /usr/share/elasticsearch/config/elasticsearch_password
export ELASTIC_PASSWORD_FILE=/usr/share/elasticsearch/config/elasticsearch_password
exec /usr/local/bin/docker-entrypoint.sh
