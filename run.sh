#!/bin/zsh

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check if Docker is installed
if ! command_exists docker; then
    echo "Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command_exists docker-compose; then
    echo "Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Function to display usage instructions
usage() {
    echo "Usage: $0 [development|production]"
    exit 1
}

# Check if the environment argument is provided
if [ -z "$1" ]; then
    usage
fi

ENVIRONMENT=$1

# Set the ENV_FILE based on the provided environment
if [ "$ENVIRONMENT" = "development" ]; then
    export ENV_FILE=.env.development
elif [ "$ENVIRONMENT" = "production" ]; then
    export ENV_FILE=.env.production
else
    usage
fi

# Build and run the Docker Compose setup
docker-compose up --build
