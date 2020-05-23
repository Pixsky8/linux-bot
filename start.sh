#!/bin/sh

docker run --pids-limit 20 -v $(pwd)/data:/data linux-bot
