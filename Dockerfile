FROM ubuntu:18.04
MAINTAINER g0pher <mail@jseung.me>

RUN apt-get update
RUN apt-get install -y \
	sudo vim net-tools iputils-ping git curl wget openssh-server \
	python3 python3-pip python3-dev \
	locales language-pack-ko

RUN update-locale LANG=ko_KR.UTF-8

# Setup SSH
RUN sed -ri 's/UsePAM yes/#UsePAM yes/g' /etc/ssh/sshd_config
RUN sed -ri 's/#ListenAddress/ListenAddress/g' /etc/ssh/sshd_config
RUN sed -ri 's/#Port/Port/g' /etc/ssh/sshd_config

# Setup user
RUN useradd -m road
RUN chsh -s /bin/bash road
RUN echo "root:root" | chpasswd
RUN echo "road:road123" | chpasswd
RUN mkdir /home/road/.ssh \
	&& chown road:road /home/road/.ssh \
	&& chmod 700 /home/road/.ssh
RUN echo 'road ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

USER road
WORKDIR /home/road

# Setup lang ko.UTF-8
ENV LANGUAGE=ko_KR.UTF-8
ENV LANG=ko_KR.UTF-8
ENV LC_ALL=ko_KR.UTF-8

# Install python lib
ENV PYTHONIOENCODING=utf-8
COPY ./requirements.txt /requirements.txt
RUN python3 -m pip install -r /requirements.txt


ENTRYPOINT tail -f /dev/null

