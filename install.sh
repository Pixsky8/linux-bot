#!/bin/sh

mkdir data
docker build -t linux-bot .
sh start.sh
