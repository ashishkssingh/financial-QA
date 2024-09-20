# Set environment variables from .env
include .env

# Build the Docker image using Docker Compose
build:
	docker-compose build --no-cache

# Run the Docker image using Docker Compose
run:
	docker-compose up