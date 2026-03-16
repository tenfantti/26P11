#!/usr/bin/env bash
# Build and start the container in background
cd "$(dirname "$0")/.."
docker compose up --build -d
