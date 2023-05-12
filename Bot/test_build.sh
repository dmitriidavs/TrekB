#!/bin/bash

# TODO before running: chmod +x test_build.sh

IMAGE_NAME=$(sudo docker images --format '{{.Repository}}:{{.Tag}}' --no-trunc | sort -r | awk 'NR==1{print $1}')
CNTNR_NAME=$(sudo docker ps -ql --format "{{.Names}}")

sudo docker system prune -af
sudo docker volume prune -f
sudo docker compose down
sudo docker rmi ${IMAGE_NAME}
sudo docker compose up -d
sudo docker logs -f ${CNTNR_NAME}