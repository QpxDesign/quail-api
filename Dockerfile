# syntax=docker/dockerfile:1
FROM python:3.8-slim-buster
FROM nvidia/cuda:11.0
RUN apt-get update && apt-get install -y cuda-toolkit-11.0

WORKDIR /python-docker

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
