#!/bin/bash

# Wait MySQL healthcheck to be healthy before starting other services
MYSQL_CONTAINER_NAME="mysql"
TIMEOUT=60
INTERVAL=5
ELAPSED=0

while [ "$ELAPSED" -lt "$TIMEOUT" ]; do
  HEALTH_STATUS=$(docker inspect --format='{{json .State.Health.Status}}' $MYSQL_CONTAINER_NAME 2>/dev/null)

  if [ "$HEALTH_STATUS" == "\"healthy\"" ]; then
    echo "MySQL container is healthy. Proceeding to start other services."
    docker-compose up -d backend frontend
    exit 0
  fi

  echo "Waiting for MySQL to become healthy... ($ELAPSED/$TIMEOUT seconds elapsed)"
  sleep $INTERVAL
  ELAPSED=$((ELAPSED + INTERVAL))
done

if [ "$ELAPSED" -ge "$TIMEOUT" ]; then
  echo "Timeout reached. MySQL container did not become healthy."
  exit 1
fi