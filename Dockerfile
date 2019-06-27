FROM python:3.6.8-stretch

RUN apt-get install tzdata && \
        cp /usr/share/zoneinfo/Asia/Seoul /etc/localtime && \
        echo "Asia/Seoul" > /etc/timezone

RUN apt-get install gcc

RUN pip install -U setuptools

COPY . /ionian

WORKDIR /ionian

RUN python setup.py install

ENTRYPOINT ["python", "main.py"]