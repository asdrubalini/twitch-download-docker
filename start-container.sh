export TWITCH_USERNAME=$1
export COMPOSE_PROJECT_NAME=$1
docker-compose up -d --build
