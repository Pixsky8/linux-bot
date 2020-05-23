FROM debian:buster
# install packages
RUN apt update &&\
    apt install -y man wget curl git ssh ed\
        python3.7 python3-pip\
        neofetch toilet\
        libcaca0 caca-utils libcaca-dev\
        gcc gdb valgrind make cmake\
        ocaml opam m4 bubblewrap

RUN wget https://sh.rustup.rs
RUN sh index.html -y
RUN rm index.html

# add python scripts
COPY . /app/
WORKDIR /app

# install python dep
RUN pip3 install discord

# security measures
RUN chmod a-rwx config/
RUN chmod a-rwx config/settings.json
RUN useradd -u 4242 quarantedeux
RUN chmod a-rx $(which yes)

# store /data
VOLUME [ "/data" ]

# store home for future sessions
RUN ln -s /data/home /home/quarantedeux

# on server start
CMD python3.7 src/bot.py
