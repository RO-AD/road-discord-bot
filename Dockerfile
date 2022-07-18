FROM ubuntu:18.04

RUN apt-get update
RUN apt-get install -y \
	vim net-tools git curl wget \
	python3 python3-pip python3-dev

COPY ./requirements.txt /requirements.txt
RUN python3 -m pip install -r /requirements.txt





ENTRYPOINT tail -f /dev/null

