#!/bin/sh

mkdir -p data/home
docker build -t linux-bot .
sh start.sh
