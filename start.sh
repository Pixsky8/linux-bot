#!/bin/sh

docker run -i -t --memory="1024m" --memory-swap="0m" --pids-limit 20 -v $(pwd)/data:/data linux-bot
