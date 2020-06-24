FROM ubuntu:latest
MAINTAINER Edoardo De Din ededin@eonerc.rwth-aachen.de

RUN apt-get update && apt-get upgrade -y \ 
  --no-install-recommends python3 python3-virtualenv

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m virtualenv --python=/usr/bin/python3 $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY powerflow/setup/requirements_docker.txt .
RUN pip install -r requirements_docker.txt