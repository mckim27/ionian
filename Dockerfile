FROM python:3.6.8-alpine3.9

COPY . /ionian

WORKDIR /ionian

RUN python setup.py install

ENTRYPOINT ["python", "main.py"]