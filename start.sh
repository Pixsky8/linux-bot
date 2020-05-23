#!/bin/sh

docker run --memory="512m" --memory-swap="4m" --pids-limit 20 -v $(pwd)/data:/data linux-bot
