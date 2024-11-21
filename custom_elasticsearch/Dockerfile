# Dockerfile
FROM docker.elastic.co/elasticsearch/elasticsearch:8.15.3

COPY --chmod=755 entrypoint.sh /usr/local/bin/entrypoint.sh

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
