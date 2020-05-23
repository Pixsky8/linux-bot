FROM debian:buster
# install python
RUN apt update &&\
    apt install python3.7 python3-pip -y

# add python scripts
ADD . /app/
WORKDIR /app

# install python dep
RUN pip3 install discord

# security measures
RUN chmod a-rwx config/
RUN chmod a-rwx config/settings.json
RUN useradd -u 4242 quarantedeux

# store /data
VOLUME [ "/data" ]


# on server start
CMD python3.7 src/bot.py
