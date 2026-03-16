#!/usr/bin/env bash
# Build and start the container in foreground (shows logs)
cd "$(dirname "$0")/.."
docker compose up --build
