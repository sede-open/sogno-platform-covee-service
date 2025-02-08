FROM ubuntu:18.04
FROM python:3.11.2

LABEL author="Edoardo De Din ededin@eonerc.rwth-aachen.de"

RUN apt-get update -y \
    && apt-get install build-essential -y \
    && apt install python3-pip -y \
    && apt-get install python3-venv -y \
    && apt-get install sudo -y 

# ENV VIRTUAL_ENV=/opt/venv
# RUN python3 -m virtualenv --python=/usr/bin/python3 $VIRTUAL_ENV
# ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# COPY covee-powerflow/setup/requirements_docker.txt .
# RUN pip3 install -r requirements_docker.txt