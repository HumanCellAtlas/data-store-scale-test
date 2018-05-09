FROM ubuntu:17.10

LABEL maintainer tsmith12@ucsc.edu

RUN apt-get -y update
ADD requirements.txt ./
RUN apt-get -y install \
        libevent-dev \
        git \
        python3.6-dev \
        python3.6 \
        python3-pip && \
        python3.6 -m pip install --requirement requirements.txt
COPY ./run.py /run.py

EXPOSE 8089
EXPOSE 5557
EXPOSE 5558

ENTRYPOINT ["python3.6", "-u", "/run.py"]